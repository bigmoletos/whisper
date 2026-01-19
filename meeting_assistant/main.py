"""
Meeting Assistant - Point d'entrée principal
Module de transcription et résumé de réunions Teams/Zoom/etc.

Usage:
    python -m meeting_assistant start --name "Ma Réunion"
    python -m meeting_assistant list
    python -m meeting_assistant status
    python -m meeting_assistant resume --session <id>
"""

import sys
import os

# Ajouter le chemin parent pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meeting_assistant.ui.cli_interface import main

if __name__ == "__main__":
    main()
