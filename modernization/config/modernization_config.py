"""
Configuration schemas for VTT System Modernization

This module defines configuration data classes and validation schemas
for all modernization features and components.
"""

import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from pathlib import Path
import json
from enum import Enum

logger = logging.getLogger(__name__)


class LogLevel(Enum):
    """Logging levels for configuration."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class TestingFramework(Enum):
    """Supported testing frameworks."""
    HYPOTHESIS = "hypothesis"
    PYTEST = "pytest"
    UNITTEST = "unittest"


@dataclass
class SpecConfig:
    """Configuration for spec compliance features."""
    requirements_validation: bool = True
    ears_pattern_enforcement: bool = True
    property_generation: bool = True
    task_breakdown_automation: bool = True
    incose_quality_rules: bool = True
    traceability_matrix: bool = True
    
    def validate(self) -> List[str]:
        """Validate spec configuration."""
        errors = []
        
        # All boolean fields should be valid
        bool_fields = [
            'requirements_validation', 'ears_pattern_enforcement',
            'property_generation', 'task_breakdown_automation',
            'incose_quality_rules', 'traceability_matrix'
        ]
        
        for field_name in bool_fields:
            value = getattr(self, field_name)
            if not isinstance(value, bool):
                errors.append(f"SpecConfig.{field_name} must be boolean, got {type(value)}")
        
        return errors


@dataclass
class CodeWhispererConfig:
    """Configuration for Amazon CodeWhisperer."""
    enabled: bool = True
    language_preferences: List[str] = field(default_factory=lambda: ['python', 'javascript', 'typescript'])
    suggestion_threshold: float = 0.7
    auto_accept_threshold: float = 0.9
    context_window_size: int = 1000
    max_suggestions: int = 5
    
    def validate(self) -> List[str]:
        """Validate CodeWhisperer configuration."""
        errors = []
        
        if not isinstance(self.enabled, bool):
            errors.append("CodeWhispererConfig.enabled must be boolean")
        
        if not isinstance(self.language_preferences, list):
            errors.append("CodeWhispererConfig.language_preferences must be list")
        elif not all(isinstance(lang, str) for lang in self.language_preferences):
            errors.append("CodeWhispererConfig.language_preferences must contain only strings")
        
        if not 0.0 <= self.suggestion_threshold <= 1.0:
            errors.append("CodeWhispererConfig.suggestion_threshold must be between 0.0 and 1.0")
        
        if not 0.0 <= self.auto_accept_threshold <= 1.0:
            errors.append("CodeWhispererConfig.auto_accept_threshold must be between 0.0 and 1.0")
        
        if not isinstance(self.context_window_size, int) or self.context_window_size <= 0:
            errors.append("CodeWhispererConfig.context_window_size must be positive integer")
        
        if not isinstance(self.max_suggestions, int) or self.max_suggestions <= 0:
            errors.append("CodeWhispererConfig.max_suggestions must be positive integer")
        
        return errors


@dataclass
class AgentConfig:
    """Configuration for autonomous agents."""
    enabled: bool = True
    agent_types: List[str] = field(default_factory=lambda: ['code_review', 'performance_optimization'])
    schedule_interval: int = 3600  # seconds
    max_concurrent_agents: int = 2
    timeout_seconds: int = 300
    
    def validate(self) -> List[str]:
        """Validate agent configuration."""
        errors = []
        
        if not isinstance(self.enabled, bool):
            errors.append("AgentConfig.enabled must be boolean")
        
        if not isinstance(self.agent_types, list):
            errors.append("AgentConfig.agent_types must be list")
        
        valid_agent_types = ['code_review', 'performance_optimization', 'security_audit', 'documentation', 'testing']
        for agent_type in self.agent_types:
            if agent_type not in valid_agent_types:
                errors.append(f"Invalid agent type: {agent_type}. Valid types: {valid_agent_types}")
        
        if not isinstance(self.schedule_interval, int) or self.schedule_interval <= 0:
            errors.append("AgentConfig.schedule_interval must be positive integer")
        
        if not isinstance(self.max_concurrent_agents, int) or self.max_concurrent_agents <= 0:
            errors.append("AgentConfig.max_concurrent_agents must be positive integer")
        
        if not isinstance(self.timeout_seconds, int) or self.timeout_seconds <= 0:
            errors.append("AgentConfig.timeout_seconds must be positive integer")
        
        return errors


@dataclass
class AmazonConfig:
    """Configuration for Amazon integration features."""
    codewhisperer_enabled: bool = True
    codewhisperer: CodeWhispererConfig = field(default_factory=CodeWhispererConfig)
    openrewrite_recipes: List[str] = field(default_factory=list)
    autonomous_agents: AgentConfig = field(default_factory=AgentConfig)
    formal_verification: bool = False
    aws_region: str = "us-east-1"
    credentials_profile: Optional[str] = None
    
    def validate(self) -> List[str]:
        """Validate Amazon configuration."""
        errors = []
        
        if not isinstance(self.codewhisperer_enabled, bool):
            errors.append("AmazonConfig.codewhisperer_enabled must be boolean")
        
        if not isinstance(self.formal_verification, bool):
            errors.append("AmazonConfig.formal_verification must be boolean")
        
        if not isinstance(self.aws_region, str):
            errors.append("AmazonConfig.aws_region must be string")
        
        if self.credentials_profile is not None and not isinstance(self.credentials_profile, str):
            errors.append("AmazonConfig.credentials_profile must be string or None")
        
        # Validate nested configurations
        errors.extend(self.codewhisperer.validate())
        errors.extend(self.autonomous_agents.validate())
        
        return errors


@dataclass
class HypothesisConfig:
    """Configuration for Hypothesis property testing."""
    max_examples: int = 100
    deadline: int = 10000  # milliseconds
    verbosity: str = "normal"  # normal, verbose, quiet
    database_file: Optional[str] = None
    suppress_health_check: List[str] = field(default_factory=list)
    
    def validate(self) -> List[str]:
        """Validate Hypothesis configuration."""
        errors = []
        
        if not isinstance(self.max_examples, int) or self.max_examples <= 0:
            errors.append("HypothesisConfig.max_examples must be positive integer")
        
        if not isinstance(self.deadline, int) or self.deadline <= 0:
            errors.append("HypothesisConfig.deadline must be positive integer")
        
        valid_verbosity = ['normal', 'verbose', 'quiet']
        if self.verbosity not in valid_verbosity:
            errors.append(f"HypothesisConfig.verbosity must be one of: {valid_verbosity}")
        
        if self.database_file is not None and not isinstance(self.database_file, str):
            errors.append("HypothesisConfig.database_file must be string or None")
        
        if not isinstance(self.suppress_health_check, list):
            errors.append("HypothesisConfig.suppress_health_check must be list")
        
        return errors


@dataclass
class PropertyTestConfig:
    """Configuration for property-based testing."""
    hypothesis_iterations: int = 100
    testing_framework: TestingFramework = TestingFramework.HYPOTHESIS
    hypothesis: HypothesisConfig = field(default_factory=HypothesisConfig)
    audio_test_patterns: List[str] = field(default_factory=lambda: ['valid_audio', 'invalid_audio', 'edge_case_audio'])
    round_trip_testing: bool = True
    invariant_checking: bool = True
    metamorphic_testing: bool = True
    error_handling_testing: bool = True
    coverage_threshold: float = 0.8
    
    def validate(self) -> List[str]:
        """Validate property test configuration."""
        errors = []
        
        if not isinstance(self.hypothesis_iterations, int) or self.hypothesis_iterations <= 0:
            errors.append("PropertyTestConfig.hypothesis_iterations must be positive integer")
        
        if not isinstance(self.testing_framework, TestingFramework):
            errors.append("PropertyTestConfig.testing_framework must be TestingFramework enum")
        
        if not isinstance(self.audio_test_patterns, list):
            errors.append("PropertyTestConfig.audio_test_patterns must be list")
        
        bool_fields = ['round_trip_testing', 'invariant_checking', 'metamorphic_testing', 'error_handling_testing']
        for field_name in bool_fields:
            value = getattr(self, field_name)
            if not isinstance(value, bool):
                errors.append(f"PropertyTestConfig.{field_name} must be boolean")
        
        if not 0.0 <= self.coverage_threshold <= 1.0:
            errors.append("PropertyTestConfig.coverage_threshold must be between 0.0 and 1.0")
        
        # Validate nested configuration
        errors.extend(self.hypothesis.validate())
        
        return errors


@dataclass
class MonitoringConfig:
    """Configuration for performance monitoring."""
    enabled: bool = True
    metrics_collection_interval: int = 60  # seconds
    health_check_interval: int = 300  # seconds
    log_level: LogLevel = LogLevel.INFO
    log_file: Optional[str] = None
    metrics_retention_days: int = 30
    alert_thresholds: Dict[str, float] = field(default_factory=lambda: {
        'cpu_usage': 0.8,
        'memory_usage': 0.9,
        'error_rate': 0.1,
        'latency_p95': 5.0
    })
    
    def validate(self) -> List[str]:
        """Validate monitoring configuration."""
        errors = []
        
        if not isinstance(self.enabled, bool):
            errors.append("MonitoringConfig.enabled must be boolean")
        
        if not isinstance(self.metrics_collection_interval, int) or self.metrics_collection_interval <= 0:
            errors.append("MonitoringConfig.metrics_collection_interval must be positive integer")
        
        if not isinstance(self.health_check_interval, int) or self.health_check_interval <= 0:
            errors.append("MonitoringConfig.health_check_interval must be positive integer")
        
        if not isinstance(self.log_level, LogLevel):
            errors.append("MonitoringConfig.log_level must be LogLevel enum")
        
        if self.log_file is not None and not isinstance(self.log_file, str):
            errors.append("MonitoringConfig.log_file must be string or None")
        
        if not isinstance(self.metrics_retention_days, int) or self.metrics_retention_days <= 0:
            errors.append("MonitoringConfig.metrics_retention_days must be positive integer")
        
        if not isinstance(self.alert_thresholds, dict):
            errors.append("MonitoringConfig.alert_thresholds must be dictionary")
        else:
            for key, value in self.alert_thresholds.items():
                if not isinstance(key, str):
                    errors.append(f"MonitoringConfig.alert_thresholds key '{key}' must be string")
                if not isinstance(value, (int, float)):
                    errors.append(f"MonitoringConfig.alert_thresholds['{key}'] must be numeric")
        
        return errors


@dataclass
class CompatibilityConfig:
    """Configuration for legacy compatibility."""
    maintain_api_compatibility: bool = True
    legacy_config_support: bool = True
    migration_mode: bool = False
    rollback_enabled: bool = True
    backup_before_changes: bool = True
    compatibility_checks: List[str] = field(default_factory=lambda: ['api', 'config', 'data_format'])
    
    def validate(self) -> List[str]:
        """Validate compatibility configuration."""
        errors = []
        
        bool_fields = [
            'maintain_api_compatibility', 'legacy_config_support', 
            'migration_mode', 'rollback_enabled', 'backup_before_changes'
        ]
        
        for field_name in bool_fields:
            value = getattr(self, field_name)
            if not isinstance(value, bool):
                errors.append(f"CompatibilityConfig.{field_name} must be boolean")
        
        if not isinstance(self.compatibility_checks, list):
            errors.append("CompatibilityConfig.compatibility_checks must be list")
        
        valid_checks = ['api', 'config', 'data_format', 'behavior', 'performance']
        for check in self.compatibility_checks:
            if check not in valid_checks:
                errors.append(f"Invalid compatibility check: {check}. Valid checks: {valid_checks}")
        
        return errors


@dataclass
class ModernizationConfig:
    """Main configuration for VTT system modernization."""
    spec_compliance: SpecConfig = field(default_factory=SpecConfig)
    amazon_integration: AmazonConfig = field(default_factory=AmazonConfig)
    property_testing: PropertyTestConfig = field(default_factory=PropertyTestConfig)
    performance_monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    legacy_compatibility: CompatibilityConfig = field(default_factory=CompatibilityConfig)
    
    # Global settings
    enabled: bool = True
    debug_mode: bool = False
    config_version: str = "1.0.0"
    
    def validate(self) -> List[str]:
        """
        Validate the complete modernization configuration.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Validate global settings
        if not isinstance(self.enabled, bool):
            errors.append("ModernizationConfig.enabled must be boolean")
        
        if not isinstance(self.debug_mode, bool):
            errors.append("ModernizationConfig.debug_mode must be boolean")
        
        if not isinstance(self.config_version, str):
            errors.append("ModernizationConfig.config_version must be string")
        
        # Validate nested configurations
        errors.extend(self.spec_compliance.validate())
        errors.extend(self.amazon_integration.validate())
        errors.extend(self.property_testing.validate())
        errors.extend(self.performance_monitoring.validate())
        errors.extend(self.legacy_compatibility.validate())
        
        return errors
    
    def is_valid(self) -> bool:
        """
        Check if configuration is valid.
        
        Returns:
            True if configuration is valid
        """
        return len(self.validate()) == 0
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'ModernizationConfig':
        """
        Create configuration from dictionary.
        
        Args:
            config_dict: Configuration dictionary
            
        Returns:
            ModernizationConfig instance
        """
        try:
            # Extract nested configurations
            spec_config = SpecConfig(**config_dict.get('spec_compliance', {}))
            
            amazon_dict = config_dict.get('amazon_integration', {})
            codewhisperer_config = CodeWhispererConfig(**amazon_dict.get('codewhisperer', {}))
            agent_config = AgentConfig(**amazon_dict.get('autonomous_agents', {}))
            amazon_config = AmazonConfig(
                codewhisperer=codewhisperer_config,
                autonomous_agents=agent_config,
                **{k: v for k, v in amazon_dict.items() if k not in ['codewhisperer', 'autonomous_agents']}
            )
            
            property_dict = config_dict.get('property_testing', {})
            hypothesis_config = HypothesisConfig(**property_dict.get('hypothesis', {}))
            property_config = PropertyTestConfig(
                hypothesis=hypothesis_config,
                **{k: v for k, v in property_dict.items() if k != 'hypothesis'}
            )
            
            monitoring_config = MonitoringConfig(**config_dict.get('performance_monitoring', {}))
            compatibility_config = CompatibilityConfig(**config_dict.get('legacy_compatibility', {}))
            
            # Create main configuration
            return cls(
                spec_compliance=spec_config,
                amazon_integration=amazon_config,
                property_testing=property_config,
                performance_monitoring=monitoring_config,
                legacy_compatibility=compatibility_config,
                **{k: v for k, v in config_dict.items() 
                   if k not in ['spec_compliance', 'amazon_integration', 'property_testing', 
                               'performance_monitoring', 'legacy_compatibility']}
            )
            
        except Exception as e:
            logger.error(f"Error creating configuration from dict: {e}", exc_info=True)
            # Return default configuration as fallback
            return cls()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Configuration as dictionary
        """
        return {
            'enabled': self.enabled,
            'debug_mode': self.debug_mode,
            'config_version': self.config_version,
            'spec_compliance': {
                'requirements_validation': self.spec_compliance.requirements_validation,
                'ears_pattern_enforcement': self.spec_compliance.ears_pattern_enforcement,
                'property_generation': self.spec_compliance.property_generation,
                'task_breakdown_automation': self.spec_compliance.task_breakdown_automation,
                'incose_quality_rules': self.spec_compliance.incose_quality_rules,
                'traceability_matrix': self.spec_compliance.traceability_matrix
            },
            'amazon_integration': {
                'codewhisperer_enabled': self.amazon_integration.codewhisperer_enabled,
                'formal_verification': self.amazon_integration.formal_verification,
                'aws_region': self.amazon_integration.aws_region,
                'credentials_profile': self.amazon_integration.credentials_profile,
                'codewhisperer': {
                    'enabled': self.amazon_integration.codewhisperer.enabled,
                    'language_preferences': self.amazon_integration.codewhisperer.language_preferences,
                    'suggestion_threshold': self.amazon_integration.codewhisperer.suggestion_threshold,
                    'auto_accept_threshold': self.amazon_integration.codewhisperer.auto_accept_threshold,
                    'context_window_size': self.amazon_integration.codewhisperer.context_window_size,
                    'max_suggestions': self.amazon_integration.codewhisperer.max_suggestions
                },
                'autonomous_agents': {
                    'enabled': self.amazon_integration.autonomous_agents.enabled,
                    'agent_types': self.amazon_integration.autonomous_agents.agent_types,
                    'schedule_interval': self.amazon_integration.autonomous_agents.schedule_interval,
                    'max_concurrent_agents': self.amazon_integration.autonomous_agents.max_concurrent_agents,
                    'timeout_seconds': self.amazon_integration.autonomous_agents.timeout_seconds
                }
            },
            'property_testing': {
                'hypothesis_iterations': self.property_testing.hypothesis_iterations,
                'testing_framework': self.property_testing.testing_framework.value,
                'audio_test_patterns': self.property_testing.audio_test_patterns,
                'round_trip_testing': self.property_testing.round_trip_testing,
                'invariant_checking': self.property_testing.invariant_checking,
                'metamorphic_testing': self.property_testing.metamorphic_testing,
                'error_handling_testing': self.property_testing.error_handling_testing,
                'coverage_threshold': self.property_testing.coverage_threshold,
                'hypothesis': {
                    'max_examples': self.property_testing.hypothesis.max_examples,
                    'deadline': self.property_testing.hypothesis.deadline,
                    'verbosity': self.property_testing.hypothesis.verbosity,
                    'database_file': self.property_testing.hypothesis.database_file,
                    'suppress_health_check': self.property_testing.hypothesis.suppress_health_check
                }
            },
            'performance_monitoring': {
                'enabled': self.performance_monitoring.enabled,
                'metrics_collection_interval': self.performance_monitoring.metrics_collection_interval,
                'health_check_interval': self.performance_monitoring.health_check_interval,
                'log_level': self.performance_monitoring.log_level.value,
                'log_file': self.performance_monitoring.log_file,
                'metrics_retention_days': self.performance_monitoring.metrics_retention_days,
                'alert_thresholds': self.performance_monitoring.alert_thresholds
            },
            'legacy_compatibility': {
                'maintain_api_compatibility': self.legacy_compatibility.maintain_api_compatibility,
                'legacy_config_support': self.legacy_compatibility.legacy_config_support,
                'migration_mode': self.legacy_compatibility.migration_mode,
                'rollback_enabled': self.legacy_compatibility.rollback_enabled,
                'backup_before_changes': self.legacy_compatibility.backup_before_changes,
                'compatibility_checks': self.legacy_compatibility.compatibility_checks
            }
        }
    
    @classmethod
    def load_from_file(cls, config_path: Union[str, Path]) -> 'ModernizationConfig':
        """
        Load configuration from JSON file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            ModernizationConfig instance
        """
        config_path = Path(config_path)
        
        try:
            if not config_path.exists():
                logger.warning(f"Configuration file not found: {config_path}, using defaults")
                return cls()
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
            
            config = cls.from_dict(config_dict)
            
            # Validate loaded configuration
            validation_errors = config.validate()
            if validation_errors:
                logger.warning(f"Configuration validation errors: {validation_errors}")
            
            logger.info(f"Configuration loaded from: {config_path}")
            return config
            
        except Exception as e:
            logger.error(f"Error loading configuration from {config_path}: {e}", exc_info=True)
            return cls()
    
    def save_to_file(self, config_path: Union[str, Path]) -> bool:
        """
        Save configuration to JSON file.
        
        Args:
            config_path: Path to save configuration file
            
        Returns:
            True if saved successfully
        """
        config_path = Path(config_path)
        
        try:
            # Create directory if it doesn't exist
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert to dictionary and save
            config_dict = self.to_dict()
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Configuration saved to: {config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving configuration to {config_path}: {e}", exc_info=True)
            return False