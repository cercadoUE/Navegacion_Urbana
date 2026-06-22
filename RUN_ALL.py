"""
Script todo-en-uno: instala dependencias y ejecuta la demo.
"""

import subprocess
import sys

print("=" * 65)
print("  Navegación Urbana con Caminos más Cortos")
print("  Grupo E — ADA 2026 — Universidad ESAN")
print("=" * 65)

print("\n[1/2] Instalando dependencias...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

print("\n[2/2] Ejecutando demo...")
print()
subprocess.check_call([sys.executable, "demo.py"])
