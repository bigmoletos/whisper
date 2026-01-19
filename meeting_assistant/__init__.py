"""
Meeting Assistant - Module de transcription et résumé de réunions
Capture audio système invisible avec traitement par batch pour réunions longues
"""

__version__ = "1.0.0"
__author__ = "Meeting Assistant"

from .session.meeting_session import MeetingSession

__all__ = ["MeetingSession"]
