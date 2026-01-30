"""
Audio data models for VTT modernization.

This module defines enhanced audio data structures and processing contexts
for the modernized VTT system.
"""

import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import time

logger = logging.getLogger(__name__)


class AudioFormat(Enum):
    """Supported audio formats."""
    WAV = "wav"
    MP3 = "mp3"
    FLAC = "flac"
    OGG = "ogg"
    M4A = "m4a"


class ProcessingMode(Enum):
    """Audio processing modes."""
    REAL_TIME = "real_time"
    BATCH = "batch"
    STREAMING = "streaming"
    OFFLINE = "offline"


class QualityLevel(Enum):
    """Quality levels for processing."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ULTRA = "ultra"


@dataclass
class AudioMetadata:
    """Metadata for audio data."""
    duration: float
    format: AudioFormat
    bit_depth: int
    encoding: str
    source: str = "unknown"
    timestamp: float = field(default_factory=time.time)
    language_hint: Optional[str] = None
    speaker_count: Optional[int] = None
    noise_level: Optional[float] = None
    
    def validate(self) -> List[str]:
        """Validate audio metadata."""
        errors = []
        
        if self.duration <= 0:
            errors.append("AudioMetadata.duration must be positive")
        
        if not isinstance(self.format, AudioFormat):
            errors.append("AudioMetadata.format must be AudioFormat enum")
        
        if self.bit_depth not in [8, 16, 24, 32]:
            errors.append("AudioMetadata.bit_depth must be 8, 16, 24, or 32")
        
        if self.speaker_count is not None and self.speaker_count <= 0:
            errors.append("AudioMetadata.speaker_count must be positive if specified")
        
        if self.noise_level is not None and not 0.0 <= self.noise_level <= 1.0:
            errors.append("AudioMetadata.noise_level must be between 0.0 and 1.0 if specified")
        
        return errors


@dataclass
class QualityMetrics:
    """Quality requirements and metrics."""
    target_accuracy: float = 0.95
    min_confidence: float = 0.7
    max_latency: float = 5.0  # seconds
    quality_level: QualityLevel = QualityLevel.MEDIUM
    noise_tolerance: float = 0.1
    
    def validate(self) -> List[str]:
        """Validate quality metrics."""
        errors = []
        
        if not 0.0 <= self.target_accuracy <= 1.0:
            errors.append("QualityMetrics.target_accuracy must be between 0.0 and 1.0")
        
        if not 0.0 <= self.min_confidence <= 1.0:
            errors.append("QualityMetrics.min_confidence must be between 0.0 and 1.0")
        
        if self.max_latency <= 0:
            errors.append("QualityMetrics.max_latency must be positive")
        
        if not isinstance(self.quality_level, QualityLevel):
            errors.append("QualityMetrics.quality_level must be QualityLevel enum")
        
        if not 0.0 <= self.noise_tolerance <= 1.0:
            errors.append("QualityMetrics.noise_tolerance must be between 0.0 and 1.0")
        
        return errors


@dataclass
class PerformanceConstraints:
    """Performance constraints for processing."""
    max_memory_mb: int = 1024
    max_cpu_cores: int = 4
    max_processing_time: float = 30.0  # seconds
    priority: int = 1  # 1=high, 2=medium, 3=low
    allow_gpu: bool = True
    
    def validate(self) -> List[str]:
        """Validate performance constraints."""
        errors = []
        
        if self.max_memory_mb <= 0:
            errors.append("PerformanceConstraints.max_memory_mb must be positive")
        
        if self.max_cpu_cores <= 0:
            errors.append("PerformanceConstraints.max_cpu_cores must be positive")
        
        if self.max_processing_time <= 0:
            errors.append("PerformanceConstraints.max_processing_time must be positive")
        
        if self.priority not in [1, 2, 3]:
            errors.append("PerformanceConstraints.priority must be 1, 2, or 3")
        
        if not isinstance(self.allow_gpu, bool):
            errors.append("PerformanceConstraints.allow_gpu must be boolean")
        
        return errors


@dataclass
class FallbackStrategy:
    """Strategy for engine fallback."""
    enabled: bool = True
    max_attempts: int = 3
    timeout_multiplier: float = 1.5
    quality_degradation_allowed: bool = True
    preferred_engines: List[str] = field(default_factory=list)
    
    def validate(self) -> List[str]:
        """Validate fallback strategy."""
        errors = []
        
        if not isinstance(self.enabled, bool):
            errors.append("FallbackStrategy.enabled must be boolean")
        
        if self.max_attempts <= 0:
            errors.append("FallbackStrategy.max_attempts must be positive")
        
        if self.timeout_multiplier <= 0:
            errors.append("FallbackStrategy.timeout_multiplier must be positive")
        
        if not isinstance(self.quality_degradation_allowed, bool):
            errors.append("FallbackStrategy.quality_degradation_allowed must be boolean")
        
        if not isinstance(self.preferred_engines, list):
            errors.append("FallbackStrategy.preferred_engines must be list")
        
        return errors


@dataclass
class ProcessingContext:
    """Context for audio processing operations."""
    mode: ProcessingMode
    quality_requirements: QualityMetrics
    performance_constraints: PerformanceConstraints
    fallback_strategy: FallbackStrategy
    session_id: str = field(default_factory=lambda: f"session_{int(time.time())}")
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self) -> List[str]:
        """Validate processing context."""
        errors = []
        
        if not isinstance(self.mode, ProcessingMode):
            errors.append("ProcessingContext.mode must be ProcessingMode enum")
        
        if not isinstance(self.session_id, str):
            errors.append("ProcessingContext.session_id must be string")
        
        if not isinstance(self.user_preferences, dict):
            errors.append("ProcessingContext.user_preferences must be dictionary")
        
        # Validate nested objects
        errors.extend(self.quality_requirements.validate())
        errors.extend(self.performance_constraints.validate())
        errors.extend(self.fallback_strategy.validate())
        
        return errors
    
    def is_real_time(self) -> bool:
        """Check if processing is real-time."""
        return self.mode in [ProcessingMode.REAL_TIME, ProcessingMode.STREAMING]
    
    def get_timeout(self) -> float:
        """Get processing timeout based on context."""
        base_timeout = self.performance_constraints.max_processing_time
        
        if self.is_real_time():
            return min(base_timeout, self.quality_requirements.max_latency)
        
        return base_timeout


@dataclass
class EnhancedAudioData:
    """Enhanced audio data container with metadata and context."""
    samples: np.ndarray
    sample_rate: int
    channels: int
    metadata: AudioMetadata
    processing_context: ProcessingContext
    
    def __post_init__(self):
        """Validate audio data after initialization."""
        validation_errors = self.validate()
        if validation_errors:
            logger.warning(f"Audio data validation warnings: {validation_errors}")
    
    def validate(self) -> List[str]:
        """Validate enhanced audio data."""
        errors = []
        
        # Validate samples
        if not isinstance(self.samples, np.ndarray):
            errors.append("EnhancedAudioData.samples must be numpy array")
        elif self.samples.size == 0:
            errors.append("EnhancedAudioData.samples cannot be empty")
        elif not np.isfinite(self.samples).all():
            errors.append("EnhancedAudioData.samples contains non-finite values")
        
        # Validate sample rate
        if not isinstance(self.sample_rate, int) or self.sample_rate <= 0:
            errors.append("EnhancedAudioData.sample_rate must be positive integer")
        elif self.sample_rate < 8000 or self.sample_rate > 192000:
            errors.append("EnhancedAudioData.sample_rate should be between 8000 and 192000 Hz")
        
        # Validate channels
        if not isinstance(self.channels, int) or self.channels <= 0:
            errors.append("EnhancedAudioData.channels must be positive integer")
        elif self.channels > 8:
            errors.append("EnhancedAudioData.channels should not exceed 8")
        
        # Validate shape consistency
        if isinstance(self.samples, np.ndarray):
            if self.channels == 1:
                if self.samples.ndim != 1:
                    errors.append("Mono audio should have 1D samples array")
            else:
                if self.samples.ndim != 2 or self.samples.shape[1] != self.channels:
                    errors.append(f"Multi-channel audio should have shape (samples, {self.channels})")
        
        # Validate nested objects
        errors.extend(self.metadata.validate())
        errors.extend(self.processing_context.validate())
        
        return errors
    
    def get_duration(self) -> float:
        """Get audio duration in seconds."""
        if isinstance(self.samples, np.ndarray) and self.samples.size > 0:
            if self.channels == 1:
                return len(self.samples) / self.sample_rate
            else:
                return self.samples.shape[0] / self.sample_rate
        return 0.0
    
    def get_rms_level(self) -> float:
        """Get RMS level of audio."""
        if not isinstance(self.samples, np.ndarray) or self.samples.size == 0:
            return 0.0
        
        return float(np.sqrt(np.mean(self.samples ** 2)))
    
    def is_silent(self, threshold: float = 0.001) -> bool:
        """Check if audio is silent."""
        return self.get_rms_level() < threshold
    
    def get_peak_level(self) -> float:
        """Get peak level of audio."""
        if not isinstance(self.samples, np.ndarray) or self.samples.size == 0:
            return 0.0
        
        return float(np.max(np.abs(self.samples)))
    
    def is_clipped(self, threshold: float = 0.99) -> bool:
        """Check if audio is clipped."""
        return self.get_peak_level() >= threshold
    
    def to_mono(self) -> 'EnhancedAudioData':
        """Convert to mono audio."""
        if self.channels == 1:
            return self
        
        # Convert to mono by averaging channels
        mono_samples = np.mean(self.samples, axis=1)
        
        # Update metadata
        new_metadata = AudioMetadata(
            duration=self.metadata.duration,
            format=self.metadata.format,
            bit_depth=self.metadata.bit_depth,
            encoding=self.metadata.encoding,
            source=f"{self.metadata.source}_mono",
            timestamp=self.metadata.timestamp,
            language_hint=self.metadata.language_hint,
            speaker_count=self.metadata.speaker_count,
            noise_level=self.metadata.noise_level
        )
        
        return EnhancedAudioData(
            samples=mono_samples,
            sample_rate=self.sample_rate,
            channels=1,
            metadata=new_metadata,
            processing_context=self.processing_context
        )
    
    def resample(self, target_sample_rate: int) -> 'EnhancedAudioData':
        """Resample audio to target sample rate."""
        if self.sample_rate == target_sample_rate:
            return self
        
        # Simple resampling (in production, would use proper resampling)
        ratio = target_sample_rate / self.sample_rate
        
        if self.channels == 1:
            new_length = int(len(self.samples) * ratio)
            resampled = np.interp(
                np.linspace(0, len(self.samples) - 1, new_length),
                np.arange(len(self.samples)),
                self.samples
            )
        else:
            new_length = int(self.samples.shape[0] * ratio)
            resampled = np.zeros((new_length, self.channels))
            for ch in range(self.channels):
                resampled[:, ch] = np.interp(
                    np.linspace(0, self.samples.shape[0] - 1, new_length),
                    np.arange(self.samples.shape[0]),
                    self.samples[:, ch]
                )
        
        # Update metadata
        new_duration = self.metadata.duration * (target_sample_rate / self.sample_rate)
        new_metadata = AudioMetadata(
            duration=new_duration,
            format=self.metadata.format,
            bit_depth=self.metadata.bit_depth,
            encoding=self.metadata.encoding,
            source=f"{self.metadata.source}_resampled",
            timestamp=self.metadata.timestamp,
            language_hint=self.metadata.language_hint,
            speaker_count=self.metadata.speaker_count,
            noise_level=self.metadata.noise_level
        )
        
        return EnhancedAudioData(
            samples=resampled.astype(self.samples.dtype),
            sample_rate=target_sample_rate,
            channels=self.channels,
            metadata=new_metadata,
            processing_context=self.processing_context
        )


@dataclass
class TranscriptionMetadata:
    """Metadata for transcription results."""
    engine_version: str
    model_name: str
    language_detected: Optional[str] = None
    confidence_scores: List[float] = field(default_factory=list)
    word_timestamps: List[Dict[str, Any]] = field(default_factory=list)
    speaker_labels: List[str] = field(default_factory=list)
    processing_stats: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self) -> List[str]:
        """Validate transcription metadata."""
        errors = []
        
        if not isinstance(self.engine_version, str):
            errors.append("TranscriptionMetadata.engine_version must be string")
        
        if not isinstance(self.model_name, str):
            errors.append("TranscriptionMetadata.model_name must be string")
        
        if self.language_detected is not None and not isinstance(self.language_detected, str):
            errors.append("TranscriptionMetadata.language_detected must be string or None")
        
        if not isinstance(self.confidence_scores, list):
            errors.append("TranscriptionMetadata.confidence_scores must be list")
        elif not all(isinstance(score, (int, float)) and 0.0 <= score <= 1.0 
                    for score in self.confidence_scores):
            errors.append("TranscriptionMetadata.confidence_scores must contain values between 0.0 and 1.0")
        
        if not isinstance(self.word_timestamps, list):
            errors.append("TranscriptionMetadata.word_timestamps must be list")
        
        if not isinstance(self.speaker_labels, list):
            errors.append("TranscriptionMetadata.speaker_labels must be list")
        
        if not isinstance(self.processing_stats, dict):
            errors.append("TranscriptionMetadata.processing_stats must be dictionary")
        
        return errors


@dataclass
class TranscriptionResult:
    """Enhanced transcription result with comprehensive metadata."""
    text: str
    confidence: float
    engine_used: str
    processing_time: float
    metadata: TranscriptionMetadata
    properties_validated: List[str] = field(default_factory=list)
    quality_score: Optional[float] = None
    error_message: Optional[str] = None
    success: bool = True
    
    def __post_init__(self):
        """Validate transcription result after initialization."""
        validation_errors = self.validate()
        if validation_errors:
            logger.warning(f"Transcription result validation warnings: {validation_errors}")
    
    def validate(self) -> List[str]:
        """Validate transcription result."""
        errors = []
        
        if not isinstance(self.text, str):
            errors.append("TranscriptionResult.text must be string")
        
        if not isinstance(self.confidence, (int, float)) or not 0.0 <= self.confidence <= 1.0:
            errors.append("TranscriptionResult.confidence must be between 0.0 and 1.0")
        
        if not isinstance(self.engine_used, str):
            errors.append("TranscriptionResult.engine_used must be string")
        
        if not isinstance(self.processing_time, (int, float)) or self.processing_time < 0:
            errors.append("TranscriptionResult.processing_time must be non-negative")
        
        if not isinstance(self.properties_validated, list):
            errors.append("TranscriptionResult.properties_validated must be list")
        
        if self.quality_score is not None:
            if not isinstance(self.quality_score, (int, float)) or not 0.0 <= self.quality_score <= 1.0:
                errors.append("TranscriptionResult.quality_score must be between 0.0 and 1.0 or None")
        
        if self.error_message is not None and not isinstance(self.error_message, str):
            errors.append("TranscriptionResult.error_message must be string or None")
        
        if not isinstance(self.success, bool):
            errors.append("TranscriptionResult.success must be boolean")
        
        # Validate nested metadata
        errors.extend(self.metadata.validate())
        
        return errors
    
    def is_high_quality(self, threshold: float = 0.8) -> bool:
        """Check if transcription is high quality."""
        return self.confidence >= threshold and (
            self.quality_score is None or self.quality_score >= threshold
        )
    
    def get_word_count(self) -> int:
        """Get word count of transcription."""
        return len(self.text.split()) if self.text else 0
    
    def get_average_confidence(self) -> float:
        """Get average confidence from word-level scores."""
        if self.metadata.confidence_scores:
            return sum(self.metadata.confidence_scores) / len(self.metadata.confidence_scores)
        return self.confidence
    
    def has_speaker_info(self) -> bool:
        """Check if result includes speaker information."""
        return bool(self.metadata.speaker_labels)
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        stats = self.metadata.processing_stats.copy()
        stats.update({
            'text_length': len(self.text),
            'word_count': self.get_word_count(),
            'processing_time': self.processing_time,
            'confidence': self.confidence,
            'success': self.success
        })
        return stats