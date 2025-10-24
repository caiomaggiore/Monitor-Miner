# 🔥 Monitor Miner v4.0 - Arquitetura Modular

## 📋 Estrutura Oficial v4.0

```
esp32/
├── boot.py                    # ✅ Inicialização do sistema
├── main.py                    # ✅ Aplicação principal v4.0
├── VERSION.json               # ✅ Informações de versão
│
├── core/                      # ✅ Módulos fundamentais
│   ├── __init__.py
│   ├── http_server.py        # ✅ Servidor HTTP unificado
│   ├── router.py             # ✅ Sistema de roteamento
│   └── response.py           # ✅ Helpers HTTP
│
├── services/                  # ✅ Serviços independentes
│   ├── __init__.py
│   ├── system_monitor.py     # ✅ Monitor do sistema
│   └── data_store.py        # ✅ Acesso a dados JSON
│
├── controllers/               # ✅ Orquestradores
│   ├── __init__.py
│   ├── dashboard_controller.py
│   └── config_controller.py
│
├── data/                      # ✅ Dados e configurações
│   ├── config.json
│   ├── sensors_config.json
│   └── sensors.json
│
└── web/                       # ✅ Interface web
    ├── index.html
    ├── config.html
    ├── css/
    └── js/
        └── core/
            ├── components.js  # ✅ Componentes UI reutilizáveis
            └── dashboard.js   # ✅ Dashboard modular
```

## 🚀 Como Fazer Upload

### **Windows:**
```bash
# Execute o script automático
upload_v4.0.bat
```

### **Linux/Mac:**
```bash
# Torne o script executável
chmod +x upload_v4.0.sh

# Execute o script
./upload_v4.0.sh
```

### **Manual:**
```bash
# Upload arquivos principais
mpremote connect COM3 cp esp32/boot.py :
mpremote connect COM3 cp esp32/main.py :
mpremote connect COM3 cp esp32/VERSION.json :

# Upload core modules
mpremote connect COM3 cp -r esp32/core/ :

# Upload services
mpremote connect COM3 cp -r esp32/services/ :

# Upload controllers
mpremote connect COM3 cp -r esp32/controllers/ :

# Upload data
mpremote connect COM3 cp -r esp32/data/ :

# Upload web
mpremote connect COM3 cp -r esp32/web/ :
```

## 🌐 Acesso

Após o upload, acesse:

- **Dashboard:** `http://[IP_DO_ESP32]:8080`
- **Configuração:** `http://[IP_DO_ESP32]:8080/config`
- **API Status:** `http://[IP_DO_ESP32]:8080/api/status`
- **API Sensores:** `http://[IP_DO_ESP32]:8080/api/sensors`

## ✨ Características v4.0

- ✅ **Zero duplicação de código**
- ✅ **Services independentes e reutilizáveis**
- ✅ **Controllers como orquestradores**
- ✅ **UI components modulares**
- ✅ **Arquitetura escalável**
- ✅ **Cache inteligente de arquivos**
- ✅ **CORS automático**
- ✅ **Sistema de roteamento HTTP**

## 📊 APIs Disponíveis

### **Dashboard:**
- `GET /` - Página principal
- `GET /api/status` - Status do sistema
- `GET /api/sensors` - Dados dos sensores
- `GET /api/sensors/{id}` - Sensor específico

### **Configuração:**
- `GET /config` - Página de configuração
- `GET /api/config` - Configuração geral
- `POST /api/config` - Atualizar configuração
- `GET /api/sensors/config` - Configuração de sensores
- `POST /api/sensors` - Adicionar sensor
- `DELETE /api/sensors/{id}` - Remover sensor

## 🔧 Desenvolvimento

### **Adicionar novo Service:**
1. Criar arquivo em `services/novo_service.py`
2. Implementar classe com métodos independentes
3. Importar no controller necessário

### **Adicionar novo Controller:**
1. Criar arquivo em `controllers/novo_controller.py`
2. Implementar métodos de requisição
3. Adicionar rotas no `main.py`

### **Adicionar novo Componente UI:**
1. Criar função em `web/js/core/components.js`
2. Usar em `web/js/core/dashboard.js`
3. Reutilizar em outras páginas

## 🎯 Próximas Versões

- **v4.1.0:** Implementação de sensores reais
- **v4.2.0:** WebSocket para updates em tempo real
- **v5.0.0:** Interface mobile responsiva

---

**🎉 Monitor Miner v4.0 - Arquitetura Modular e Escalável!**
