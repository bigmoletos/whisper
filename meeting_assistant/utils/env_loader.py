"""
Utilitaire pour charger les variables d'environnement depuis un fichier .env
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict

logger = logging.getLogger(__name__)


def load_env_file(env_file: str) -> Dict[str, str]:
    """
    Charge les variables depuis un fichier .env

    Args:
        env_file: Chemin vers le fichier .env

    Returns:
        Dictionnaire des variables chargées
    """
    loaded = {}
    env_path = Path(env_file).expanduser()

    if not env_path.exists():
        logger.warning(f"Fichier .env non trouvé: {env_path}")
        return loaded

    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # Ignorer les lignes vides et les commentaires
                if not line or line.startswith("#"):
                    continue

                # Parser KEY=VALUE
                if "=" in line:
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip()

                    # Enlever les guillemets si présents
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]

                    if key:
                        os.environ[key] = value
                        loaded[key] = value
                        logger.debug(f"Variable chargée: {key}")

        logger.info(f"Fichier .env chargé: {len(loaded)} variables depuis {env_path}")

    except Exception as e:
        logger.error(f"Erreur lecture fichier .env: {e}")

    return loaded


def get_env_var(var_name: str, env_file: Optional[str] = None) -> Optional[str]:
    """
    Récupère une variable d'environnement, en chargeant le fichier .env si spécifié

    Args:
        var_name: Nom de la variable
        env_file: Fichier .env optionnel à charger

    Returns:
        Valeur de la variable ou None
    """
    # Charger le fichier .env si spécifié
    if env_file:
        load_env_file(env_file)

    # Récupérer la variable
    value = os.environ.get(var_name)

    if value:
        logger.debug(f"Variable {var_name} trouvée")
    else:
        logger.warning(f"Variable {var_name} non trouvée")

    return value
