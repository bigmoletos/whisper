"""
Script de test pour identifier les codes de touches
Utile pour configurer des raccourcis avec des caractères spéciaux
"""

import keyboard
import sys

print("=" * 60)
print("Test de détection de raccourci clavier")
print("=" * 60)
print()
print("Instructions:")
print("1. Appuyez sur votre raccourci (ex: AltGr + ¤)")
print("2. Les informations de la touche seront affichées")
print("3. Appuyez sur ESC pour quitter")
print()
print("-" * 60)

def on_key_press(event):
    """Affiche les informations sur la touche pressée"""
    print(f"\nTouche détectée:")
    print(f"  - Nom: {event.name}")
    print(f"  - Code de scan: {event.scan_code}")
    print(f"  - Caractère: {repr(event.char) if event.char else 'Aucun'}")
    print(f"  - Événement: {event.event_type}")

    # Vérifier les modificateurs
    modifiers = []
    if keyboard.is_pressed('ctrl'):
        modifiers.append('ctrl')
    if keyboard.is_pressed('shift'):
        modifiers.append('shift')
    if keyboard.is_pressed('alt'):
        modifiers.append('alt')
    if keyboard.is_pressed('right alt'):
        modifiers.append('right alt')
    if keyboard.is_pressed('windows'):
        modifiers.append('win')

    if modifiers:
        print(f"  - Modificateurs actifs: {', '.join(modifiers)}")
        hotkey_string = '+'.join(sorted(modifiers) + [event.name])
        print(f"  - Chaîne de raccourci suggérée: {hotkey_string}")
        print(f"\n  → Configuration JSON suggérée:")
        print(f'    {{"modifiers": {modifiers}, "key": "{event.name}"}}')

    print("-" * 60)

def on_hotkey_test():
    """Teste si le raccourci AltGr+¤ fonctionne"""
    print("\n✓ Raccourci AltGr+¤ détecté avec succès!")
    print("  Le raccourci fonctionne correctement.")
    print("-" * 60)

# Enregistrer les callbacks
keyboard.on_press(on_key_press)

# Tester le raccourci AltGr+¤
print("\nTest du raccourci AltGr+¤...")
try:
    keyboard.add_hotkey('right alt+¤', on_hotkey_test)
    print("  Raccourci 'right alt+¤' enregistré")
except Exception as e:
    print(f"  ⚠ Impossible d'enregistrer 'right alt+¤': {e}")
    print("  Essayez avec 'right alt+4' (sur clavier AZERTY)")
    try:
        keyboard.add_hotkey('right alt+4', on_hotkey_test)
        print("  ✓ Raccourci 'right alt+4' enregistré")
    except Exception as e2:
        print(f"  ⚠ Impossible d'enregistrer 'right alt+4': {e2}")

print("\nAppuyez sur ESC pour quitter...")
print()

try:
    keyboard.wait('esc')
except KeyboardInterrupt:
    pass

print("\nTest terminé.")
keyboard.unhook_all()
