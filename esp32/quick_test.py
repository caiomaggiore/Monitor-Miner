# ============================================================================
# QUICK TEST - Monitor Miner v4.0
# ============================================================================
# Teste rápido para verificar se a arquitetura v4.0 funciona
# ============================================================================

print("[QUICK] 🚀 Teste rápido da arquitetura v4.0...")

try:
    # Teste 1: Core modules
    print("\n[QUICK] 1. Testando core modules...")
    from core.http_server import HTTPServer
    from core.router import Router
    from core.response import json_response
    print("✅ Core modules OK")
    
    # Teste 2: Services
    print("\n[QUICK] 2. Testando services...")
    from services.system_monitor import system_monitor
    from services.data_store import data_store
    print("✅ Services OK")
    
    # Teste 3: Controllers
    print("\n[QUICK] 3. Testando controllers...")
    from controllers.dashboard_controller import dashboard_controller
    from controllers.config_controller import config_controller
    print("✅ Controllers OK")
    
    # Teste 4: Main app
    print("\n[QUICK] 4. Testando main app...")
    from main import MonitorMinerApp
    print("✅ Main app OK")
    
    # Teste 5: Criar instância
    print("\n[QUICK] 5. Testando criação de instância...")
    app = MonitorMinerApp()
    print("✅ Instância criada OK")
    
    print("\n[QUICK] ✅ Todos os testes passaram!")
    print("[QUICK] 🎉 Arquitetura v4.0 pronta para uso!")
    
except Exception as e:
    print(f"\n[QUICK] ❌ Erro: {e}")
    print(f"[QUICK] Tipo: {type(e).__name__}")
    import sys
    sys.print_exception(e)
