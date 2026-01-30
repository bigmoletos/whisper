"""
Configuration management for VTT modernization.

This module provides configuration schemas and validation for modernization features.
"""

from .modernization_config import ModernizationConfig, SpecConfig, AmazonConfig, PropertyTestConfig

__all__ = [
    'ModernizationConfig',
    'SpecConfig', 
    'AmazonConfig',
    'PropertyTestConfig'
]