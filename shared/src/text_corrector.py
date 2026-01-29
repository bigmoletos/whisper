"""
Module de correction orthographique et grammaticale post-transcription
Utilise un LLM pour corriger les erreurs de Whisper
"""

import logging
import json
import os
from typing import Optional, Dict, Any
import requests

logger = logging.getLogger(__name__)


class TextCorrector:
    """
    Corrige l'orthographe, la grammaire et la ponctuation du texte transcrit
    Supporte Ollama (local) et OpenAI/Anthropic (API)
    """

    def __init__(
        self,
        backend: str = "ollama",
        ollama_url: str = "http://localhost:11434",
        ollama_model: str = "llama3.2",
        openai_api_key: Optional[str] = None,
        openai_model: str = "gpt-4o-mini",
        anthropic_api_key: Optional[str] = None,
        anthropic_model: str = "claude-3-haiku-20240307",
        enabled: bool = True
    ):
        """
        Initialise le correcteur de texte

        Args:
            backend: "ollama", "openai", ou "anthropic"
            ollama_url: URL de l'instance Ollama (pour backend local)
            ollama_model: Modèle Ollama à utiliser (llama3.2, mistral, etc.)
            openai_api_key: Clé API OpenAI (optionnel)
            openai_model: Modèle OpenAI à utiliser
            anthropic_api_key: Clé API Anthropic (optionnel)
            anthropic_model: Modèle Anthropic à utiliser
            enabled: Active/désactive la correction (pour tests)
        """
        self.backend = backend
        self.enabled = enabled

        # Configuration Ollama
        self.ollama_url = ollama_url
        self.ollama_model = ollama_model

        # Configuration OpenAI
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.openai_model = openai_model

        # Configuration Anthropic
        self.anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        self.anthropic_model = anthropic_model

        # Prompt système pour la correction
        self.system_prompt = """Tu es un expert en langue française chargé de corriger les erreurs d'une transcription vocale automatique.

Ta mission :
1. Corriger TOUTES les fautes d'orthographe
2. Corriger TOUTES les fautes de grammaire
3. Améliorer la ponctuation (virgules, points, etc.)
4. Corriger les homophones mal transcrits (ex: "c'est" vs "ses", "a" vs "à")
5. Corriger les noms propres (personnes, entreprises, technologies)
6. Conserver le sens et le style du locuteur
7. Ne PAS ajouter de contenu qui n'était pas dans le texte original
8. Ne PAS résumer ou reformuler

Réponds UNIQUEMENT avec le texte corrigé, sans commentaires ni explications."""

        if not self.enabled:
            logger.info("Correction de texte DÉSACTIVÉE")
        else:
            logger.info(f"Correction de texte initialisée avec backend: {backend}")
            if backend == "ollama":
                self._check_ollama_availability()

    def _check_ollama_availability(self) -> bool:
        """Vérifie si Ollama est accessible"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m.get("name", "") for m in models]

                if self.ollama_model not in model_names:
                    logger.warning(
                        f"Modèle '{self.ollama_model}' non trouvé dans Ollama. "
                        f"Modèles disponibles: {model_names}"
                    )
                    logger.warning(f"Pour installer: ollama pull {self.ollama_model}")
                    return False

                logger.info(f"Ollama disponible avec modèle: {self.ollama_model}")
                return True
            else:
                logger.warning(f"Ollama non accessible (statut: {response.status_code})")
                return False

        except Exception as e:
            logger.warning(f"Ollama non disponible: {e}")
            logger.warning("Pour installer Ollama: https://ollama.ai/download")
            return False

    def correct_text(self, text: str, context: Optional[str] = None) -> str:
        """
        Corrige le texte transcrit

        Args:
            text: Texte brut de la transcription
            context: Contexte additionnel (vocabulaire technique, etc.)

        Returns:
            Texte corrigé
        """
        if not self.enabled:
            return text

        if not text or len(text.strip()) == 0:
            return text

        try:
            logger.info(f"Correction de texte ({len(text)} caractères)...")

            # Construire le prompt utilisateur
            user_prompt = f"Texte à corriger:\n\n{text}"

            if context:
                user_prompt = f"Contexte: {context}\n\n{user_prompt}"

            # Appeler le backend approprié
            if self.backend == "ollama":
                corrected = self._correct_with_ollama(user_prompt)
            elif self.backend == "openai":
                corrected = self._correct_with_openai(user_prompt)
            elif self.backend == "anthropic":
                corrected = self._correct_with_anthropic(user_prompt)
            else:
                logger.error(f"Backend inconnu: {self.backend}")
                return text

            if corrected and len(corrected.strip()) > 0:
                logger.info(f"Texte corrigé avec succès ({len(corrected)} caractères)")
                logger.debug(f"Avant: {text[:100]}...")
                logger.debug(f"Après: {corrected[:100]}...")
                return corrected.strip()
            else:
                logger.warning("Correction vide, retour du texte original")
                return text

        except Exception as e:
            logger.error(f"Erreur lors de la correction: {e}", exc_info=True)
            # En cas d'erreur, retourner le texte original
            return text

    def _correct_with_ollama(self, user_prompt: str) -> str:
        """Correction avec Ollama (local)"""
        try:
            payload = {
                "model": self.ollama_model,
                "prompt": f"{self.system_prompt}\n\n{user_prompt}",
                "stream": False,
                "options": {
                    "temperature": 0.1,  # Très déterministe
                    "top_p": 0.9,
                    "num_predict": 2000  # Limite de tokens
                }
            }

            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                logger.error(f"Erreur Ollama: {response.status_code} - {response.text}")
                return ""

        except Exception as e:
            logger.error(f"Erreur lors de la correction avec Ollama: {e}")
            return ""

    def _correct_with_openai(self, user_prompt: str) -> str:
        """Correction avec OpenAI API"""
        if not self.openai_api_key:
            logger.error("Clé API OpenAI non configurée")
            return ""

        try:
            import openai

            client = openai.OpenAI(api_key=self.openai_api_key)

            response = client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )

            return response.choices[0].message.content.strip()

        except ImportError:
            logger.error("Module openai non installé: pip install openai")
            return ""
        except Exception as e:
            logger.error(f"Erreur lors de la correction avec OpenAI: {e}")
            return ""

    def _correct_with_anthropic(self, user_prompt: str) -> str:
        """Correction avec Anthropic API (Claude)"""
        if not self.anthropic_api_key:
            logger.error("Clé API Anthropic non configurée")
            return ""

        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.anthropic_api_key)

            response = client.messages.create(
                model=self.anthropic_model,
                max_tokens=2000,
                temperature=0.1,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            return response.content[0].text.strip()

        except ImportError:
            logger.error("Module anthropic non installé: pip install anthropic")
            return ""
        except Exception as e:
            logger.error(f"Erreur lors de la correction avec Anthropic: {e}")
            return ""

    def batch_correct(self, texts: list[str]) -> list[str]:
        """
        Corrige plusieurs textes en batch

        Args:
            texts: Liste de textes à corriger

        Returns:
            Liste de textes corrigés
        """
        if not self.enabled:
            return texts

        corrected_texts = []
        for i, text in enumerate(texts):
            logger.info(f"Correction du texte {i+1}/{len(texts)}...")
            corrected = self.correct_text(text)
            corrected_texts.append(corrected)

        return corrected_texts


def load_corrector_from_config(config: Dict[str, Any]) -> Optional[TextCorrector]:
    """
    Charge le correcteur depuis la configuration

    Args:
        config: Configuration du service

    Returns:
        Instance de TextCorrector ou None si désactivé
    """
    correction_config = config.get("text_correction", {})

    if not correction_config.get("enabled", False):
        logger.info("Correction de texte désactivée dans la configuration")
        return None

    backend = correction_config.get("backend", "ollama")

    # Configuration selon le backend
    kwargs = {
        "backend": backend,
        "enabled": True
    }

    if backend == "ollama":
        kwargs.update({
            "ollama_url": correction_config.get("ollama", {}).get("url", "http://localhost:11434"),
            "ollama_model": correction_config.get("ollama", {}).get("model", "llama3.2")
        })
    elif backend == "openai":
        kwargs.update({
            "openai_api_key": correction_config.get("openai", {}).get("api_key"),
            "openai_model": correction_config.get("openai", {}).get("model", "gpt-4o-mini")
        })
    elif backend == "anthropic":
        kwargs.update({
            "anthropic_api_key": correction_config.get("anthropic", {}).get("api_key"),
            "anthropic_model": correction_config.get("anthropic", {}).get("model", "claude-3-haiku-20240307")
        })

    return TextCorrector(**kwargs)
