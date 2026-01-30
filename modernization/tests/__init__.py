"""
Test infrastructure for VTT modernization.

This module provides the testing framework setup, including Hypothesis
configuration and pytest integration for property-based testing.
"""

# Configure Hypothesis settings for VTT testing
from hypothesis import settings, Verbosity
import os

# Default Hypothesis settings for VTT modernization
settings.register_profile("vtt_default", 
    max_examples=100,
    deadline=10000,  # 10 seconds
    verbosity=Verbosity.normal
)

settings.register_profile("vtt_ci", 
    max_examples=50,
    deadline=5000,  # 5 seconds
    verbosity=Verbosity.quiet
)

settings.register_profile("vtt_thorough", 
    max_examples=1000,
    deadline=60000,  # 60 seconds
    verbosity=Verbosity.verbose
)

# Load profile based on environment
profile = os.getenv('VTT_TEST_PROFILE', 'vtt_default')
settings.load_profile(profile)

__all__ = []