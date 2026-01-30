"""
Enhanced components for VTT system modernization.

This module contains enhanced versions of existing VTT components that provide
improved functionality while maintaining backward compatibility.
"""

from .fallback_manager import EnhancedFallbackManager
# from .mcp_interface import MCPInterface  # TODO: Implement in future tasks
# from .performance_monitor import PerformanceMonitor  # TODO: Implement in future tasks

__all__ = [
    'EnhancedFallbackManager',
    # 'MCPInterface',
    # 'PerformanceMonitor'
]