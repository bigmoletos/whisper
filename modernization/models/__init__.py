"""
Data models for VTT modernization.

This module contains data models and type definitions used throughout
the modernization infrastructure.
"""

from .audio_models import EnhancedAudioData, ProcessingContext, TranscriptionResult
from .property_models import TranscriptionProperty, PropertyType

__all__ = [
    'EnhancedAudioData',
    'ProcessingContext', 
    'TranscriptionResult',
    'TranscriptionProperty',
    'PropertyType'
]