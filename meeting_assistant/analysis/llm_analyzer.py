"""
Interface multi-backend pour l'analyse LLM
Supporte Ollama (local), OpenAI et Anthropic Claude
"""

import json
import logging
import os
import time
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Imports conditionnels
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


@dataclass
class LLMResponse:
    """Réponse d'un LLM"""
    text: str
    model: str
    backend: str
    tokens_used: int = 0
    processing_time: float = 0.0
    success: bool = True
    error: Optional[str] = None


class LLMBackend(ABC):
    """Interface abstraite pour un backend LLM"""

    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """Génère une réponse"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Vérifie si le backend est disponible"""
        pass


class OllamaBackend(LLMBackend):
    """Backend Ollama pour LLM local"""

    def __init__(
        self,
        host: str = "http://localhost:11434",
        model: str = "llama3.2",
        timeout: int = 120
    ):
        self.host = host.rstrip("/")
        self.model = model
        self.timeout = timeout

    def is_available(self) -> bool:
        """Vérifie si Ollama est accessible"""
        if not REQUESTS_AVAILABLE:
            return False
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """Génère une réponse via Ollama"""
        start_time = time.time()

        if not REQUESTS_AVAILABLE:
            return LLMResponse(
                text="",
                model=self.model,
                backend="ollama",
                success=False,
                error="requests library not available"
            )

        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 2048
                }
            }

            if system_prompt:
                payload["system"] = system_prompt

            response = requests.post(
                f"{self.host}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()

            result = response.json()
            text = result.get("response", "")
            processing_time = time.time() - start_time

            return LLMResponse(
                text=text,
                model=self.model,
                backend="ollama",
                tokens_used=result.get("eval_count", 0),
                processing_time=processing_time,
                success=True
            )

        except requests.exceptions.Timeout:
            return LLMResponse(
                text="",
                model=self.model,
                backend="ollama",
                processing_time=time.time() - start_time,
                success=False,
                error="Timeout lors de la génération"
            )
        except Exception as e:
            logger.error(f"Erreur Ollama: {e}")
            return LLMResponse(
                text="",
                model=self.model,
                backend="ollama",
                processing_time=time.time() - start_time,
                success=False,
                error=str(e)
            )


class OpenAIBackend(LLMBackend):
    """Backend OpenAI"""

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        api_key: Optional[str] = None,
        timeout: int = 60
    ):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.timeout = timeout
        self._client = None

    def _get_client(self):
        """Obtient le client OpenAI"""
        if self._client is None and OPENAI_AVAILABLE and self.api_key:
            self._client = openai.OpenAI(api_key=self.api_key, timeout=self.timeout)
        return self._client

    def is_available(self) -> bool:
        """Vérifie si OpenAI est configuré"""
        return OPENAI_AVAILABLE and bool(self.api_key)

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """Génère une réponse via OpenAI"""
        start_time = time.time()

        client = self._get_client()
        if not client:
            return LLMResponse(
                text="",
                model=self.model,
                backend="openai",
                success=False,
                error="OpenAI not configured (missing API key or library)"
            )

        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=2048
            )

            text = response.choices[0].message.content
            tokens = response.usage.total_tokens if response.usage else 0
            processing_time = time.time() - start_time

            return LLMResponse(
                text=text,
                model=self.model,
                backend="openai",
                tokens_used=tokens,
                processing_time=processing_time,
                success=True
            )

        except Exception as e:
            logger.error(f"Erreur OpenAI: {e}")
            return LLMResponse(
                text="",
                model=self.model,
                backend="openai",
                processing_time=time.time() - start_time,
                success=False,
                error=str(e)
            )


class AnthropicBackend(LLMBackend):
    """Backend Anthropic Claude"""

    def __init__(
        self,
        model: str = "claude-3-haiku-20240307",
        api_key: Optional[str] = None,
        timeout: int = 60
    ):
        self.model = model
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.timeout = timeout
        self._client = None

    def _get_client(self):
        """Obtient le client Anthropic"""
        if self._client is None and ANTHROPIC_AVAILABLE and self.api_key:
            self._client = anthropic.Anthropic(api_key=self.api_key)
        return self._client

    def is_available(self) -> bool:
        """Vérifie si Anthropic est configuré"""
        return ANTHROPIC_AVAILABLE and bool(self.api_key)

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """Génère une réponse via Anthropic"""
        start_time = time.time()

        client = self._get_client()
        if not client:
            return LLMResponse(
                text="",
                model=self.model,
                backend="anthropic",
                success=False,
                error="Anthropic not configured (missing API key or library)"
            )

        try:
            kwargs = {
                "model": self.model,
                "max_tokens": 2048,
                "messages": [{"role": "user", "content": prompt}]
            }

            if system_prompt:
                kwargs["system"] = system_prompt

            response = client.messages.create(**kwargs)

            text = response.content[0].text
            tokens = response.usage.input_tokens + response.usage.output_tokens
            processing_time = time.time() - start_time

            return LLMResponse(
                text=text,
                model=self.model,
                backend="anthropic",
                tokens_used=tokens,
                processing_time=processing_time,
                success=True
            )

        except Exception as e:
            logger.error(f"Erreur Anthropic: {e}")
            return LLMResponse(
                text="",
                model=self.model,
                backend="anthropic",
                processing_time=time.time() - start_time,
                success=False,
                error=str(e)
            )


class LLMAnalyzer:
    """
    Analyseur LLM avec support multi-backend
    Utilise Ollama par défaut, avec fallback vers OpenAI/Anthropic
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialise l'analyseur LLM

        Args:
            config: Configuration avec les paramètres des backends
        """
        self.config = config
        self.backends: Dict[str, LLMBackend] = {}
        self.primary_backend: Optional[str] = None

        # Initialiser les backends
        self._init_backends()

        logger.info(f"LLMAnalyzer initialisé avec backend primaire: {self.primary_backend}")

    def _init_backends(self) -> None:
        """Initialise les backends configurés"""
        analysis_config = self.config.get("analysis", {})
        primary = analysis_config.get("llm_backend", "ollama")

        # Ollama
        ollama_config = analysis_config.get("ollama", {})
        self.backends["ollama"] = OllamaBackend(
            host=ollama_config.get("host", "http://localhost:11434"),
            model=ollama_config.get("model", "llama3.2")
        )

        # OpenAI
        openai_config = analysis_config.get("openai", {})
        api_key_env = openai_config.get("api_key_env", "OPENAI_API_KEY")
        self.backends["openai"] = OpenAIBackend(
            model=openai_config.get("model", "gpt-4o-mini"),
            api_key=os.getenv(api_key_env)
        )

        # Anthropic
        anthropic_config = analysis_config.get("anthropic", {})
        api_key_env = anthropic_config.get("api_key_env", "ANTHROPIC_API_KEY")
        self.backends["anthropic"] = AnthropicBackend(
            model=anthropic_config.get("model", "claude-3-haiku-20240307"),
            api_key=os.getenv(api_key_env)
        )

        # Déterminer le backend primaire
        if primary in self.backends and self.backends[primary].is_available():
            self.primary_backend = primary
        else:
            # Fallback: trouver un backend disponible
            for name, backend in self.backends.items():
                if backend.is_available():
                    self.primary_backend = name
                    logger.warning(f"Backend {primary} non disponible, utilisation de {name}")
                    break

        if not self.primary_backend:
            logger.error("Aucun backend LLM disponible!")

    def analyze(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        backend: Optional[str] = None
    ) -> LLMResponse:
        """
        Analyse avec le LLM

        Args:
            prompt: Prompt utilisateur
            system_prompt: Prompt système optionnel
            backend: Backend spécifique à utiliser (None = primaire)

        Returns:
            LLMResponse avec le résultat
        """
        backend_name = backend or self.primary_backend

        if not backend_name or backend_name not in self.backends:
            return LLMResponse(
                text="",
                model="none",
                backend="none",
                success=False,
                error="No LLM backend available"
            )

        llm_backend = self.backends[backend_name]

        # Essayer le backend primaire
        response = llm_backend.generate(prompt, system_prompt)

        # Si échec, essayer les fallbacks
        if not response.success and backend is None:
            for name, fb_backend in self.backends.items():
                if name != backend_name and fb_backend.is_available():
                    logger.warning(f"Fallback vers {name}")
                    response = fb_backend.generate(prompt, system_prompt)
                    if response.success:
                        break

        return response

    def get_available_backends(self) -> Dict[str, bool]:
        """Retourne les backends disponibles"""
        return {name: backend.is_available() for name, backend in self.backends.items()}

    def get_primary_backend(self) -> Optional[str]:
        """Retourne le nom du backend primaire"""
        return self.primary_backend


# Prompts système pour l'analyse de réunions
SYSTEM_PROMPTS = {
    "intermediate_summary": """Tu es un assistant spécialisé dans le résumé de réunions.
Tu reçois un extrait de transcription d'une réunion en cours.
Génère un résumé concis qui capture:
- Les sujets principaux discutés
- Les décisions prises
- Les actions identifiées
- Les points importants

Réponds en français de manière structurée et concise.""",

    "final_synthesis": """Tu es un assistant spécialisé dans la synthèse de réunions.
Tu reçois plusieurs résumés intermédiaires d'une même réunion.
Génère un rapport final complet qui inclut:
- Un résumé exécutif (2-3 phrases)
- Les points clés (liste)
- Les highlights importants
- Les actions à suivre avec responsables si mentionnés
- Les décisions prises

Réponds en français avec un format structuré.""",

    "extract_actions": """Tu es un assistant spécialisé dans l'extraction d'actions.
Analyse le texte et extrais toutes les actions à faire.
Pour chaque action, identifie si possible:
- L'action elle-même
- Le responsable assigné
- La deadline mentionnée

Réponds en JSON avec le format:
{"actions": [{"action": "...", "assignee": "...", "deadline": "..."}]}"""
}
