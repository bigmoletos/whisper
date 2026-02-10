"""
Post-transcription word replacement module.
Fixes recurring Whisper phonetic misrecognitions using regex patterns.

To add a new replacement:
    Add an entry to REPLACEMENTS dict below.
    Key: regex pattern (case-insensitive by default)
    Value: correct replacement string
"""

import re
import logging
from typing import Dict

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────
# REPLACEMENTS DICTIONARY
# Add new entries here as Whisper misrecognitions are discovered.
# Format: r"regex pattern": "correct text"
# All patterns are applied case-insensitive.
# ──────────────────────────────────────────────────────────────

REPLACEMENTS: Dict[str, str] = {

    # === Graph databases ===
    r"\bFalcor\s*DB\b": "FalkorDB",
    r"\bFalcor\s*D\.?B\.?\b": "FalkorDB",
    r"\bFalcore?\s*DB\b": "FalkorDB",
    r"\bles mêmes graphes?\b": "Memgraph",
    r"\bMême graphe?\b": "Memgraph",
    r"\bmême graphe?\b": "Memgraph",
    r"\bMem graphe?\b": "Memgraph",

    # === Graph query languages ===
    r"\bcipher\b": "Cypher",
    r"\bCipher\b": "Cypher",
    r"\bopen cipher\b": "openCypher",
    r"\bOpen Cipher\b": "openCypher",

    # === AST ===
    r"\bun haste\b": "un AST",
    r"\bun aste\b": "un AST",
    r"\bl'haste\b": "l'AST",
    r"\bl'aste\b": "l'AST",
    r"\bun A\.S\.T\.\b": "un AST",
}


def apply_replacements(text: str,
                       extra: Dict[str, str] | None = None) -> str:
    """
    Apply word replacements to fix Whisper phonetic errors.

    Args:
        text: Raw transcribed text from Whisper.
        extra: Optional additional replacements (from config).
               Merged on top of built-in REPLACEMENTS.

    Returns:
        Corrected text.
    """
    if not text:
        return text

    all_replacements = {**REPLACEMENTS}
    if extra:
        all_replacements.update(extra)

    original = text
    for pattern, replacement in all_replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    if text != original:
        logger.info(
            f"Word replacements applied: '{original}' -> '{text}'"
        )

    return text
