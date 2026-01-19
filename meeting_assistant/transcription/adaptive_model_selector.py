"""
Sélection adaptative du modèle Whisper en fonction de la mémoire disponible
Bascule automatiquement entre small et medium selon les ressources système
"""

import logging
import psutil
from typing import Tuple, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ModelSize(Enum):
    """Tailles de modèles Whisper disponibles"""
    TINY = "tiny"
    BASE = "base"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


@dataclass
class ModelRequirements:
    """Configuration mémoire requise pour chaque modèle"""
    name: str
    ram_required_gb: float  # RAM minimum requise
    ram_recommended_gb: float  # RAM recommandée pour performance optimale
    vram_required_gb: float  # VRAM si GPU


# Exigences mémoire par modèle (valeurs approximatives pour int8)
MODEL_REQUIREMENTS: Dict[str, ModelRequirements] = {
    "tiny": ModelRequirements("tiny", 1.0, 2.0, 1.0),
    "base": ModelRequirements("base", 1.5, 2.5, 1.0),
    "small": ModelRequirements("small", 2.5, 4.0, 2.0),
    "medium": ModelRequirements("medium", 5.0, 8.0, 5.0),
    "large": ModelRequirements("large", 10.0, 16.0, 10.0),
    "large-v2": ModelRequirements("large-v2", 10.0, 16.0, 10.0),
    "large-v3": ModelRequirements("large-v3", 10.0, 16.0, 10.0),
}


class AdaptiveModelSelector:
    """
    Sélectionne automatiquement le meilleur modèle Whisper
    en fonction de la mémoire disponible
    """

    def __init__(
        self,
        preferred_model: str = "medium",
        fallback_model: str = "small",
        min_free_memory_gb: float = 2.0,
        safety_margin: float = 1.2
    ):
        """
        Initialise le sélecteur adaptatif

        Args:
            preferred_model: Modèle préféré si assez de mémoire
            fallback_model: Modèle de repli si mémoire insuffisante
            min_free_memory_gb: Mémoire minimum à garder libre
            safety_margin: Multiplicateur de sécurité pour les besoins mémoire
        """
        self.preferred_model = preferred_model
        self.fallback_model = fallback_model
        self.min_free_memory_gb = min_free_memory_gb
        self.safety_margin = safety_margin

        self._current_model: Optional[str] = None
        self._selection_reason: str = ""
        self._memory_at_selection: Optional[Dict] = None

    def get_available_memory(self) -> Dict[str, float]:
        """
        Récupère les informations de mémoire système

        Returns:
            Dict avec total_gb, available_gb, used_percent
        """
        memory = psutil.virtual_memory()

        return {
            "total_gb": memory.total / (1024 ** 3),
            "available_gb": memory.available / (1024 ** 3),
            "used_gb": memory.used / (1024 ** 3),
            "used_percent": memory.percent,
            "free_gb": memory.free / (1024 ** 3)
        }

    def can_load_model(self, model_name: str) -> Tuple[bool, str]:
        """
        Vérifie si un modèle peut être chargé avec la mémoire disponible

        Args:
            model_name: Nom du modèle à vérifier

        Returns:
            Tuple (peut_charger, raison)
        """
        if model_name not in MODEL_REQUIREMENTS:
            return False, f"Modèle inconnu: {model_name}"

        requirements = MODEL_REQUIREMENTS[model_name]
        memory = self.get_available_memory()

        # Mémoire nécessaire avec marge de sécurité
        needed_gb = requirements.ram_required_gb * self.safety_margin

        # Mémoire qui doit rester libre après chargement
        must_remain_free = self.min_free_memory_gb

        # Mémoire totale nécessaire
        total_needed = needed_gb + must_remain_free

        available = memory["available_gb"]

        if available >= total_needed:
            return True, (
                f"Mémoire OK: {available:.1f} Go disponible, "
                f"{needed_gb:.1f} Go requis pour {model_name}"
            )
        else:
            return False, (
                f"Mémoire insuffisante: {available:.1f} Go disponible, "
                f"{total_needed:.1f} Go requis ({needed_gb:.1f} + {must_remain_free:.1f} libre)"
            )

    def select_model(self) -> Tuple[str, str]:
        """
        Sélectionne le meilleur modèle en fonction de la mémoire

        Returns:
            Tuple (model_name, raison_selection)
        """
        memory = self.get_available_memory()
        self._memory_at_selection = memory

        logger.info(
            f"Sélection adaptative du modèle - "
            f"Mémoire disponible: {memory['available_gb']:.1f} Go / "
            f"{memory['total_gb']:.1f} Go ({memory['used_percent']:.0f}% utilisé)"
        )

        # Essayer d'abord le modèle préféré
        can_load, reason = self.can_load_model(self.preferred_model)

        if can_load:
            self._current_model = self.preferred_model
            self._selection_reason = f"Modèle préféré sélectionné: {reason}"
            logger.info(f"✓ Modèle sélectionné: {self.preferred_model} - {reason}")
            return self.preferred_model, self._selection_reason

        # Sinon, utiliser le modèle de repli
        logger.warning(
            f"✗ {self.preferred_model} non disponible: {reason}"
        )

        can_load_fallback, fallback_reason = self.can_load_model(self.fallback_model)

        if can_load_fallback:
            self._current_model = self.fallback_model
            self._selection_reason = (
                f"Modèle de repli sélectionné ({self.preferred_model} indisponible): "
                f"{fallback_reason}"
            )
            logger.info(f"✓ Modèle de repli sélectionné: {self.fallback_model}")
            return self.fallback_model, self._selection_reason

        # Dernier recours: tiny
        logger.warning(f"✗ {self.fallback_model} non plus disponible: {fallback_reason}")

        self._current_model = "tiny"
        self._selection_reason = (
            f"Modèle minimal sélectionné (mémoire très limitée): "
            f"{memory['available_gb']:.1f} Go disponible"
        )
        logger.warning(f"⚠ Utilisation du modèle minimal 'tiny' par défaut")
        return "tiny", self._selection_reason

    def handle_memory_error(self) -> Optional[str]:
        """
        Gère une erreur de mémoire et suggère un modèle plus petit

        Returns:
            Nouveau modèle suggéré ou None si déjà au minimum
        """
        if self._current_model is None:
            return self.fallback_model

        # Ordre de dégradation (du plus gros au plus petit)
        downgrade_order = ["large-v3", "large-v2", "large", "medium", "small", "base", "tiny"]

        try:
            current_idx = downgrade_order.index(self._current_model)
            if current_idx < len(downgrade_order) - 1:
                new_model = downgrade_order[current_idx + 1]
                logger.warning(
                    f"Erreur mémoire détectée - Passage de '{self._current_model}' à '{new_model}'"
                )
                self._current_model = new_model
                return new_model
        except ValueError:
            # Modèle non trouvé dans la liste, essayer le fallback
            logger.warning(f"Modèle '{self._current_model}' non dans l'ordre de dégradation, utilisation du fallback")
            self._current_model = self.fallback_model
            return self.fallback_model

        logger.error("Déjà au modèle minimal, impossible de réduire davantage")
        return None

    def get_status(self) -> Dict[str, Any]:
        """
        Retourne le statut actuel du sélecteur

        Returns:
            Dict avec les informations de sélection
        """
        memory = self.get_available_memory()

        return {
            "current_model": self._current_model,
            "preferred_model": self.preferred_model,
            "fallback_model": self.fallback_model,
            "selection_reason": self._selection_reason,
            "memory_at_selection": self._memory_at_selection,
            "current_memory": memory,
            "model_requirements": {
                name: {
                    "ram_required_gb": req.ram_required_gb,
                    "ram_recommended_gb": req.ram_recommended_gb
                }
                for name, req in MODEL_REQUIREMENTS.items()
            }
        }

    @staticmethod
    def get_model_info(model_name: str) -> Optional[Dict[str, Any]]:
        """
        Retourne les informations sur un modèle

        Args:
            model_name: Nom du modèle

        Returns:
            Dict avec les informations ou None
        """
        if model_name not in MODEL_REQUIREMENTS:
            return None

        req = MODEL_REQUIREMENTS[model_name]
        return {
            "name": req.name,
            "ram_required_gb": req.ram_required_gb,
            "ram_recommended_gb": req.ram_recommended_gb,
            "vram_required_gb": req.vram_required_gb
        }


def select_optimal_model(
    preferred: str = "medium",
    fallback: str = "small"
) -> Tuple[str, str]:
    """
    Fonction utilitaire pour sélectionner le modèle optimal

    Args:
        preferred: Modèle préféré
        fallback: Modèle de repli

    Returns:
        Tuple (model_name, reason)
    """
    selector = AdaptiveModelSelector(
        preferred_model=preferred,
        fallback_model=fallback
    )
    return selector.select_model()
