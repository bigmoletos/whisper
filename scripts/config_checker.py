#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script pour vérifier et configurer faster-whisper dans config.json"""

import json
import sys
from pathlib import Path

def main():
    try:
        config_path = Path('config.json')

        if not config_path.exists():
            print('[ERREUR] config.json non trouvé')
            return 1

        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Vérifier l'engine
        current_engine = config.get('whisper', {}).get('engine', 'whisper')

        if current_engine != 'faster-whisper':
            print(f'[INFO] Engine actuel: {current_engine}')
            print('[INFO] Configuration de faster-whisper...')

            if 'whisper' not in config:
                config['whisper'] = {}

            config['whisper']['engine'] = 'faster-whisper'

            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            print('[OK] Configuration mise a jour pour faster-whisper')
        else:
            print('[OK] Configuration correcte (faster-whisper)')

        return 0

    except Exception as e:
        print(f'[ERREUR] {e}')
        return 1

if __name__ == '__main__':
    sys.exit(main())
