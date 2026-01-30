#!/usr/bin/env python3
"""
Test simple de tkinter pour diagnostiquer les problèmes de pop-up
"""

print("🔧 Test de tkinter...")

try:
    import tkinter as tk
    print("✅ tkinter importé avec succès")
    
    # Test création fenêtre simple
    root = tk.Tk()
    root.title("Test VTT")
    root.geometry("200x100")
    
    label = tk.Label(root, text="Test pop-up VTT", font=("Arial", 12))
    label.pack(pady=20)
    
    print("✅ Fenêtre tkinter créée")
    print("📍 Fenêtre de test affichée pendant 3 secondes...")
    
    # Afficher pendant 3 secondes puis fermer
    root.after(3000, root.destroy)
    root.mainloop()
    
    print("✅ Test tkinter réussi !")
    
except ImportError as e:
    print(f"❌ tkinter non disponible: {e}")
    print("💡 Solution: Réinstallez Python avec tkinter inclus")
except Exception as e:
    print(f"❌ Erreur tkinter: {e}")
    print("💡 Vérifiez les permissions d'affichage")