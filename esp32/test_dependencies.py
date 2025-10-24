# ============================================================================
# TEST DEPENDENCIES - Monitor Miner v4.0
# ============================================================================
# Script para testar todas as dependências da arquitetura v4.0
# ============================================================================

print("[TEST] 🔍 Testando dependências da arquitetura v4.0...")

# Teste 1: Imports básicos do MicroPython
print("\n[TEST] 1. Imports básicos...")
try:
    import json
    print("✅ json")
except ImportError as e:
    print(f"❌ json: {e}")

try:
    import time
    print("✅ time")
except ImportError as e:
    print(f"❌ time: {e}")

try:
    import gc
    print("✅ gc")
except ImportError as e:
    print(f"❌ gc: {e}")

try:
    import socket
    print("✅ socket")
except ImportError as e:
    print(f"❌ socket: {e}")

try:
    from machine import WDT
    print("✅ machine.WDT")
except ImportError as e:
    print(f"❌ machine.WDT: {e}")

# Teste 2: Core modules
print("\n[TEST] 2. Core modules...")
try:
    from core.response import json_response
    print("✅ core.response")
except ImportError as e:
    print(f"❌ core.response: {e}")

try:
    from core.router import Router
    print("✅ core.router")
except ImportError as e:
    print(f"❌ core.router: {e}")

try:
    from core.http_server import HTTPServer
    print("✅ core.http_server")
except ImportError as e:
    print(f"❌ core.http_server: {e}")

# Teste 3: Services
print("\n[TEST] 3. Services...")
try:
    from services.system_monitor import system_monitor
    print("✅ services.system_monitor")
except ImportError as e:
    print(f"❌ services.system_monitor: {e}")

try:
    from services.data_store import data_store
    print("✅ services.data_store")
except ImportError as e:
    print(f"❌ services.data_store: {e}")

# Teste 4: Controllers
print("\n[TEST] 4. Controllers...")
try:
    from controllers.dashboard_controller import dashboard_controller
    print("✅ controllers.dashboard_controller")
except ImportError as e:
    print(f"❌ controllers.dashboard_controller: {e}")

try:
    from controllers.config_controller import config_controller
    print("✅ controllers.config_controller")
except ImportError as e:
    print(f"❌ controllers.config_controller: {e}")

# Teste 5: Main app
print("\n[TEST] 5. Main app...")
try:
    from main import MonitorMinerApp
    print("✅ main.MonitorMinerApp")
except ImportError as e:
    print(f"❌ main.MonitorMinerApp: {e}")

print("\n[TEST] ✅ Teste de dependências concluído!")
