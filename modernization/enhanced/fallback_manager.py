"""
Enhanced Fallback Manager for VTT System

This module provides an improved fallback system with better monitoring,
recovery mechanisms, and performance analytics for transcription engines.
"""

import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
import threading
from collections import deque
import numpy as np

logger = logging.getLogger(__name__)


class EngineStatus(Enum):
    """Status of transcription engines."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"
    RECOVERING = "recovering"
    DISABLED = "disabled"


class FallbackReason(Enum):
    """Reasons for fallback activation."""
    ENGINE_FAILURE = "engine_failure"
    PERFORMANCE_DEGRADATION = "performance_degradation"
    TIMEOUT = "timeout"
    QUALITY_THRESHOLD = "quality_threshold"
    RESOURCE_EXHAUSTION = "resource_exhaustion"


@dataclass
class EngineMetrics:
    """Performance metrics for a transcription engine."""
    engine_name: str
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_latency: float = 0.0
    average_quality: float = 0.0
    last_used: Optional[float] = None
    status: EngineStatus = EngineStatus.HEALTHY
    recent_latencies: deque = field(default_factory=lambda: deque(maxlen=100))
    recent_qualities: deque = field(default_factory=lambda: deque(maxlen=100))


@dataclass
class HealthStatus:
    """Overall health status of the fallback system."""
    healthy_engines: int
    degraded_engines: int
    failed_engines: int
    total_engines: int
    system_load: float
    memory_usage: float
    recommendations: List[str]


@dataclass
class TranscriptionEngine:
    """Represents a transcription engine."""
    name: str
    priority: int
    engine_callable: Callable
    config: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    max_retries: int = 3
    timeout_seconds: float = 30.0
    quality_threshold: float = 0.7


@dataclass
class AudioData:
    """Audio data container."""
    samples: np.ndarray
    sample_rate: int
    channels: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranscriptionResult:
    """Result of transcription operation."""
    text: str
    confidence: float
    engine_used: str
    processing_time: float
    quality_score: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    success: bool = True
    error_message: Optional[str] = None


class EnhancedFallbackManager:
    """
    Enhanced fallback manager for VTT transcription engines.
    
    Provides intelligent fallback decisions, real-time monitoring,
    automatic recovery, and detailed analytics for transcription engines.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Enhanced Fallback Manager.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.engines: Dict[str, TranscriptionEngine] = {}
        self.metrics: Dict[str, EngineMetrics] = {}
        self.fallback_history: List[Dict[str, Any]] = []
        
        # Configuration parameters
        self.max_fallback_attempts = self.config.get('max_fallback_attempts', 3)
        self.health_check_interval = self.config.get('health_check_interval', 60.0)
        self.performance_window = self.config.get('performance_window', 300.0)  # 5 minutes
        self.quality_threshold = self.config.get('quality_threshold', 0.7)
        self.latency_threshold = self.config.get('latency_threshold', 5.0)  # seconds
        
        # Monitoring thread
        self._monitoring_active = False
        self._monitoring_thread: Optional[threading.Thread] = None
        
        # Thread safety
        self._lock = threading.RLock()
        
        logger.info("Enhanced Fallback Manager initialized")
    
    def register_engine(self, engine: TranscriptionEngine, priority: int) -> None:
        """
        Register a transcription engine with the fallback manager.
        
        Args:
            engine: TranscriptionEngine to register
            priority: Priority level (lower numbers = higher priority)
        """
        with self._lock:
            engine.priority = priority
            self.engines[engine.name] = engine
            self.metrics[engine.name] = EngineMetrics(engine_name=engine.name)
            
            logger.info(f"Registered engine: {engine.name} with priority {priority}")
    
    def unregister_engine(self, engine_name: str) -> bool:
        """
        Unregister a transcription engine.
        
        Args:
            engine_name: Name of engine to unregister
            
        Returns:
            True if engine was unregistered successfully
        """
        with self._lock:
            if engine_name in self.engines:
                del self.engines[engine_name]
                del self.metrics[engine_name]
                logger.info(f"Unregistered engine: {engine_name}")
                return True
            
            logger.warning(f"Attempted to unregister unknown engine: {engine_name}")
            return False
    
    def attempt_transcription(self, audio: AudioData) -> TranscriptionResult:
        """
        Attempt transcription with automatic fallback.
        
        Args:
            audio: AudioData to transcribe
            
        Returns:
            TranscriptionResult with transcription and metadata
        """
        logger.debug("Starting transcription attempt with fallback")
        
        with self._lock:
            # Get sorted engines by priority and health
            available_engines = self._get_available_engines()
            
            if not available_engines:
                logger.error("No available engines for transcription")
                return TranscriptionResult(
                    text="",
                    confidence=0.0,
                    engine_used="none",
                    processing_time=0.0,
                    quality_score=0.0,
                    success=False,
                    error_message="No available transcription engines"
                )
            
            # Attempt transcription with each engine
            for attempt, engine in enumerate(available_engines):
                if attempt >= self.max_fallback_attempts:
                    logger.warning(f"Maximum fallback attempts ({self.max_fallback_attempts}) reached")
                    break
                
                try:
                    logger.debug(f"Attempting transcription with engine: {engine.name}")
                    result = self._transcribe_with_engine(engine, audio)
                    
                    if result.success:
                        self._update_engine_metrics(engine.name, result, True)
                        logger.info(f"Transcription successful with engine: {engine.name}")
                        return result
                    else:
                        self._update_engine_metrics(engine.name, result, False)
                        self._record_fallback_event(engine.name, FallbackReason.ENGINE_FAILURE, result.error_message)
                        
                except Exception as e:
                    logger.error(f"Engine {engine.name} failed: {e}", exc_info=True)
                    self._update_engine_status(engine.name, EngineStatus.FAILED)
                    self._record_fallback_event(engine.name, FallbackReason.ENGINE_FAILURE, str(e))
            
            # All engines failed
            logger.error("All transcription engines failed")
            return TranscriptionResult(
                text="",
                confidence=0.0,
                engine_used="none",
                processing_time=0.0,
                quality_score=0.0,
                success=False,
                error_message="All transcription engines failed"
            )
    
    def monitor_engine_health(self) -> HealthStatus:
        """
        Monitor the health of all registered engines.
        
        Returns:
            HealthStatus with current system health information
        """
        with self._lock:
            healthy_count = 0
            degraded_count = 0
            failed_count = 0
            recommendations = []
            
            for engine_name, metrics in self.metrics.items():
                if metrics.status == EngineStatus.HEALTHY:
                    healthy_count += 1
                elif metrics.status == EngineStatus.DEGRADED:
                    degraded_count += 1
                    recommendations.append(f"Engine {engine_name} is degraded - consider maintenance")
                elif metrics.status == EngineStatus.FAILED:
                    failed_count += 1
                    recommendations.append(f"Engine {engine_name} has failed - requires attention")
            
            total_engines = len(self.engines)
            
            # Calculate system metrics
            system_load = self._calculate_system_load()
            memory_usage = self._calculate_memory_usage()
            
            # Add system-level recommendations
            if system_load > 0.8:
                recommendations.append("High system load detected - consider load balancing")
            if memory_usage > 0.9:
                recommendations.append("High memory usage - consider memory optimization")
            if failed_count > total_engines // 2:
                recommendations.append("Critical: More than half of engines have failed")
            
            health_status = HealthStatus(
                healthy_engines=healthy_count,
                degraded_engines=degraded_count,
                failed_engines=failed_count,
                total_engines=total_engines,
                system_load=system_load,
                memory_usage=memory_usage,
                recommendations=recommendations
            )
            
            logger.debug(f"Health check: {healthy_count}/{total_engines} engines healthy")
            return health_status
    
    def trigger_fallback(self, failed_engine: str, reason: str) -> bool:
        """
        Manually trigger fallback from a specific engine.
        
        Args:
            failed_engine: Name of the failed engine
            reason: Reason for fallback
            
        Returns:
            True if fallback was triggered successfully
        """
        logger.warning(f"Manual fallback triggered for engine: {failed_engine}, reason: {reason}")
        
        with self._lock:
            if failed_engine in self.engines:
                self._update_engine_status(failed_engine, EngineStatus.FAILED)
                
                # Determine fallback reason enum
                fallback_reason = FallbackReason.ENGINE_FAILURE
                if 'performance' in reason.lower():
                    fallback_reason = FallbackReason.PERFORMANCE_DEGRADATION
                elif 'timeout' in reason.lower():
                    fallback_reason = FallbackReason.TIMEOUT
                elif 'quality' in reason.lower():
                    fallback_reason = FallbackReason.QUALITY_THRESHOLD
                
                self._record_fallback_event(failed_engine, fallback_reason, reason)
                return True
            
            logger.error(f"Cannot trigger fallback for unknown engine: {failed_engine}")
            return False
    
    def start_monitoring(self) -> None:
        """Start background health monitoring."""
        if self._monitoring_active:
            logger.warning("Monitoring already active")
            return
        
        self._monitoring_active = True
        self._monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self._monitoring_thread.start()
        
        logger.info("Background monitoring started")
    
    def stop_monitoring(self) -> None:
        """Stop background health monitoring."""
        if not self._monitoring_active:
            return
        
        self._monitoring_active = False
        if self._monitoring_thread:
            self._monitoring_thread.join(timeout=5.0)
        
        logger.info("Background monitoring stopped")
    
    def get_engine_metrics(self, engine_name: Optional[str] = None) -> Dict[str, EngineMetrics]:
        """
        Get performance metrics for engines.
        
        Args:
            engine_name: Specific engine name, or None for all engines
            
        Returns:
            Dictionary of engine metrics
        """
        with self._lock:
            if engine_name:
                return {engine_name: self.metrics.get(engine_name)} if engine_name in self.metrics else {}
            return self.metrics.copy()
    
    def get_fallback_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get fallback event history.
        
        Args:
            limit: Maximum number of events to return
            
        Returns:
            List of fallback events
        """
        with self._lock:
            history = self.fallback_history.copy()
            if limit:
                history = history[-limit:]
            return history
    
    def _get_available_engines(self) -> List[TranscriptionEngine]:
        """Get available engines sorted by priority and health."""
        available = []
        
        for engine in self.engines.values():
            if not engine.enabled:
                continue
            
            metrics = self.metrics[engine.name]
            if metrics.status in [EngineStatus.HEALTHY, EngineStatus.DEGRADED, EngineStatus.RECOVERING]:
                available.append(engine)
        
        # Sort by priority (lower number = higher priority) and then by health
        available.sort(key=lambda e: (e.priority, self._get_engine_health_score(e.name)))
        
        return available
    
    def _transcribe_with_engine(self, engine: TranscriptionEngine, audio: AudioData) -> TranscriptionResult:
        """Transcribe audio with a specific engine."""
        start_time = time.time()
        
        try:
            # Call the engine's transcription function
            result_text = engine.engine_callable(audio.samples, audio.sample_rate)
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Calculate quality score (mock implementation)
            quality_score = self._calculate_quality_score(result_text, audio)
            
            # Check if result meets quality threshold
            if quality_score < engine.quality_threshold:
                return TranscriptionResult(
                    text=result_text,
                    confidence=quality_score,
                    engine_used=engine.name,
                    processing_time=processing_time,
                    quality_score=quality_score,
                    success=False,
                    error_message=f"Quality score {quality_score} below threshold {engine.quality_threshold}"
                )
            
            return TranscriptionResult(
                text=result_text,
                confidence=quality_score,
                engine_used=engine.name,
                processing_time=processing_time,
                quality_score=quality_score,
                success=True
            )
            
        except Exception as e:
            end_time = time.time()
            processing_time = end_time - start_time
            
            return TranscriptionResult(
                text="",
                confidence=0.0,
                engine_used=engine.name,
                processing_time=processing_time,
                quality_score=0.0,
                success=False,
                error_message=str(e)
            )
    
    def _update_engine_metrics(self, engine_name: str, result: TranscriptionResult, success: bool) -> None:
        """Update performance metrics for an engine."""
        if engine_name not in self.metrics:
            return
        
        metrics = self.metrics[engine_name]
        metrics.total_requests += 1
        metrics.last_used = time.time()
        
        if success:
            metrics.successful_requests += 1
            metrics.recent_latencies.append(result.processing_time)
            metrics.recent_qualities.append(result.quality_score)
            
            # Update averages
            if metrics.recent_latencies:
                metrics.average_latency = sum(metrics.recent_latencies) / len(metrics.recent_latencies)
            if metrics.recent_qualities:
                metrics.average_quality = sum(metrics.recent_qualities) / len(metrics.recent_qualities)
            
            # Update status based on performance
            if metrics.average_latency > self.latency_threshold:
                metrics.status = EngineStatus.DEGRADED
            elif metrics.average_quality < self.quality_threshold:
                metrics.status = EngineStatus.DEGRADED
            else:
                metrics.status = EngineStatus.HEALTHY
        else:
            metrics.failed_requests += 1
            
            # Check failure rate
            failure_rate = metrics.failed_requests / metrics.total_requests
            if failure_rate > 0.5:
                metrics.status = EngineStatus.FAILED
            elif failure_rate > 0.2:
                metrics.status = EngineStatus.DEGRADED
    
    def _update_engine_status(self, engine_name: str, status: EngineStatus) -> None:
        """Update the status of an engine."""
        if engine_name in self.metrics:
            self.metrics[engine_name].status = status
            logger.debug(f"Engine {engine_name} status updated to: {status.value}")
    
    def _record_fallback_event(self, engine_name: str, reason: FallbackReason, details: str) -> None:
        """Record a fallback event for analytics."""
        event = {
            'timestamp': time.time(),
            'engine_name': engine_name,
            'reason': reason.value,
            'details': details
        }
        
        self.fallback_history.append(event)
        
        # Keep history limited
        if len(self.fallback_history) > 1000:
            self.fallback_history = self.fallback_history[-500:]
        
        logger.info(f"Fallback event recorded: {engine_name} - {reason.value}")
    
    def _get_engine_health_score(self, engine_name: str) -> float:
        """Calculate health score for an engine (0.0 = worst, 1.0 = best)."""
        if engine_name not in self.metrics:
            return 0.0
        
        metrics = self.metrics[engine_name]
        
        if metrics.total_requests == 0:
            return 0.5  # Neutral score for unused engines
        
        success_rate = metrics.successful_requests / metrics.total_requests
        latency_score = max(0.0, 1.0 - (metrics.average_latency / self.latency_threshold))
        quality_score = metrics.average_quality
        
        # Weighted average
        health_score = (success_rate * 0.4) + (latency_score * 0.3) + (quality_score * 0.3)
        
        return health_score
    
    def _calculate_quality_score(self, text: str, audio: AudioData) -> float:
        """Calculate quality score for transcription result."""
        # Mock implementation - would use actual quality metrics
        if not text:
            return 0.0
        
        # Simple heuristics
        score = 0.8  # Base score
        
        # Penalize very short results for long audio
        audio_duration = len(audio.samples) / audio.sample_rate
        if audio_duration > 1.0 and len(text) < 10:
            score -= 0.3
        
        # Reward reasonable text length
        if 10 <= len(text) <= 1000:
            score += 0.1
        
        return min(1.0, max(0.0, score))
    
    def _calculate_system_load(self) -> float:
        """Calculate current system load."""
        # Mock implementation - would use actual system metrics
        import random
        return random.uniform(0.1, 0.9)
    
    def _calculate_memory_usage(self) -> float:
        """Calculate current memory usage."""
        # Mock implementation - would use actual memory metrics
        import random
        return random.uniform(0.2, 0.8)
    
    def _monitoring_loop(self) -> None:
        """Background monitoring loop."""
        while self._monitoring_active:
            try:
                # Perform health checks
                health_status = self.monitor_engine_health()
                
                # Log health status periodically
                if health_status.failed_engines > 0 or health_status.degraded_engines > 0:
                    logger.warning(f"Health check: {health_status.healthy_engines} healthy, "
                                 f"{health_status.degraded_engines} degraded, "
                                 f"{health_status.failed_engines} failed")
                
                # Sleep until next check
                time.sleep(self.health_check_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}", exc_info=True)
                time.sleep(self.health_check_interval)