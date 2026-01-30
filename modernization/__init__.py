"""
VTT System Modernization Package

This package contains the modernization infrastructure for the VTT (Voice-to-Text Tools) system,
implementing spec compliance, Amazon integrations, and property-based testing frameworks.

The modernization follows a non-invasive wrapper pattern that enhances existing functionality
while maintaining full backward compatibility.
"""

__version__ = "1.0.0"
__author__ = "VTT Modernization Team"

# Core modernization components
from .core.spec_compliance import SpecComplianceModule
# from .core.amazon_integration import AmazonIntegrationLayer  # TODO: Implement in future tasks
# from .core.property_testing import PropertyTestFramework  # TODO: Fix hypothesis dependency
# from .core.modernization_engine import ModernizationEngine  # TODO: Implement in future tasks

# Enhanced components
from .enhanced.fallback_manager import EnhancedFallbackManager
# from .enhanced.mcp_interface import MCPInterface  # TODO: Implement in future tasks
# from .enhanced.performance_monitor import PerformanceMonitor  # TODO: Implement in future tasks

# Configuration and data models
from .config.modernization_config import ModernizationConfig
from .models.audio_models import EnhancedAudioData, ProcessingContext, TranscriptionResult
from .models.property_models import TranscriptionProperty, PropertyType

__all__ = [
    # Core components
    'SpecComplianceModule',
    # 'AmazonIntegrationLayer', 
    # 'PropertyTestFramework',
    # 'ModernizationEngine',
    
    # Enhanced components
    'EnhancedFallbackManager',
    # 'MCPInterface',
    # 'PerformanceMonitor',
    
    # Configuration and models
    'ModernizationConfig',
    'EnhancedAudioData',
    'ProcessingContext',
    'TranscriptionResult',
    'TranscriptionProperty',
    'PropertyType'
]