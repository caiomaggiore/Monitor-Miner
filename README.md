# 🔥 Monitor Miner ESP32 - v3.2.3

Sistema de monitoramento inteligente para mineração de Bitcoin com ESP32.

## 📊 Status Atual

**Versão:** v3.2.3 (Module Fix)  
**Branch:** `main` (estável) | `v4.0` (desenvolvimento)  
**Status:** ✅ Funcional e estável

---

## 🚀 Características v3.2.3

- ✅ **Servidor HTTP único** gerenciado pelo `main.py`
- ✅ **Arquitetura modular** - dashboard e config como módulos
- ✅ **Watchdog Timer** - proteção contra travamentos
- ✅ **Memory Optimizer** - gerenciamento inteligente de memória
- ✅ **System Monitor** - métricas reais de CPU, RAM, Flash
- ✅ **WiFi Setup** - portal de configuração automático
- ✅ **APIs REST** - endpoints para dashboard e configuração

---

## 📁 Estrutura do Projeto

```
esp32/
├── boot.py                     # Inicialização e modo de operação
├── main.py                     # Roteador HTTP (gerencia tudo)
├── dashboard.py                # Módulo dashboard (handlers)
├── config.py                   # Módulo configuração (handlers)
├── setup_wifi.py               # Setup WiFi (modo AP)
├── system_monitor_simple.py    # Monitor de sistema
├── memory_optimizer.py         # Otimizador de memória
├── VERSION.json                # Informações de versão
│
├── data/                       # Dados e configurações
│   ├── config.json             # Configuração WiFi
│   ├── sensors_config.json     # Configuração de sensores
│   └── sensors.json            # Dados dos sensores
│
└── web/                        # Interface Web
    ├── index.html              # Dashboard
    ├── config.html             # Configuração
    ├── setup_wifi.html         # Setup WiFi
    ├── css/                    # Estilos
    └── js/                     # JavaScript
```

---

## 🔧 Como Usar

### **1. Upload para ESP32**

```bash
# Instalar dependências
pip install mpremote

# Upload dos arquivos
mpremote connect COM3 cp -r esp32/* :
```

### **2. Primeira Inicialização**

1. ESP32 cria rede WiFi: `MonitorMiner_Setup`
2. Conecte-se a essa rede
3. Acesse: `http://192.168.4.1:8080`
4. Configure sua rede WiFi
5. ESP32 reinicia e conecta automaticamente

### **3. Uso Normal**

1. ESP32 conecta ao WiFi configurado
2. Acesse pelo IP: `http://[IP_DO_ESP32]:8080`
3. Dashboard mostra métricas em tempo real

---

## 🌐 APIs Disponíveis

### **Dashboard**
- `GET /` - Página principal
- `GET /api/sensors` - Dados dos sensores
- `GET /api/status` - Status do sistema

### **Configuração**
- `GET /config` - Página de configuração
- `GET /api/sensors/config` - Configuração de sensores
- `POST /api/sensors/add` - Adicionar sensor
- `POST /api/sensors/remove` - Remover sensor

### **Setup WiFi**
- `GET /` - Página de setup
- `GET /api/scan` - Escanear redes WiFi
- `POST /api/connect` - Conectar a rede WiFi

---

## 🛣️ Roadmap

### **v3.2.3** ✅ (Atual)
- Correção de bugs críticos
- Arquitetura modular básica
- Sistema estável para produção

### **v4.0** 🚧 (Em desenvolvimento - branch `v4.0`)
- Arquitetura completamente refatorada
- Services independentes (reutilizáveis)
- Controllers (orquestradores)
- Core modules (http_server, router)
- Componentes UI reutilizáveis
- Zero duplicação de código

---

## 📝 Changelog

### [3.2.3] - 2025-10-21
**Fixed:**
- OSError EADDRINUSE: Conflito de porta entre servidores
- SyntaxError em dashboard.py linha 66 (indentação except)
- Indentação incorreta em múltiplos blocos
- Função handle_config_request faltando em config.py

**Changed:**
- dashboard.py e config.py transformados em módulos
- Servidor HTTP único gerenciado pelo main.py
- Watchdog agora gerenciado apenas pelo main.py

---

## 🤝 Contribuindo

Este é um projeto em desenvolvimento ativo. Contribuições são bem-vindas!

### **Branches:**
- `main` - Versão estável (v3.2.3)
- `v4.0` - Desenvolvimento da próxima versão

---

## 📄 Licença

Proprietário - Todos os direitos reservados

---

## 👤 Autor

**Caio Maggiore**  
[GitHub](https://github.com/caiomaggiore)

---

**⭐ Se este projeto foi útil, considere dar uma estrela!**
