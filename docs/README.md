# 🔥 Monitor Miner v2.0

Sistema de monitoramento e controle para mineração baseado em ESP32 + MicroPython com arquitetura API REST moderna.

## ✨ Características

### Frontend
- 🎨 **CSS Customizado Ultra-Leve** (~8KB) - Substitui Bootstrap
- 📱 **100% Responsivo** - Mobile e Desktop
- ⚡ **SPA** - Single Page Application sem recarregar
- 🔄 **Atualização em Tempo Real** - AJAX a cada 5s
- 🎯 **Interface Moderna** - Design elegante e intuitivo

### Backend
- 🐍 **Python (MicroPython)** - Código limpo e eficiente
- 🌐 **API REST** - Endpoints JSON
- 📊 **Sensores** - DHT22, DHT11, 4x Corrente (ACS712)
- 🔌 **4 Relés** - Controle individual
- 💾 **JSON Database** - Persistência de dados
- 📝 **Sistema de Logs** - Estruturado e rotacionável

## 📁 Estrutura do Projeto

```
Monitor-Miner/
├── main.py                 # Backend API REST
├── boot.py                 # Inicialização e WiFi
├── hardware/               # Módulos de hardware
│   ├── sensors.py          # Gerencia sensores
│   └── relays.py           # Controla relés
├── services/               # Serviços
│   ├── logger.py           # Sistema de logs
│   └── database.py         # JSON database
├── data/                   # Banco de dados JSON
│   ├── config.json         # Configurações
│   └── logs.json           # Logs do sistema
└── web/                    # Frontend estático
    ├── index.html          # SPA
    ├── css/
    │   └── style.css       # CSS customizado (8KB)
    └── js/
        ├── api.js          # Cliente API
        ├── app.js          # Aplicação principal
        ├── utils.js        # Utilitários
        └── components/     # Componentes
            ├── dashboard.js
            ├── sensors.js
            ├── relays.js
            ├── settings.js
            └── system.js
```

## 🚀 Instalação

### 1. Requisitos

**Hardware:**
- ESP32 (qualquer modelo)
- DHT22 + DHT11
- 4x Sensores ACS712
- Módulo Relé 4 canais
- Fonte 5V/2A

**Software:**
- Python 3.8+
- mpremote: `pip install mpremote`
- Firmware MicroPython v1.22+

### 2. Configurar WiFi

```bash
# Copiar exemplo
cp config.example.py config.py

# Editar com suas credenciais
# WIFI_SSID = "SuaRede"
# WIFI_PASSWORD = "SuaSenha"
```

### 3. Upload para ESP32

```bash
# Conectar ESP32 via USB

# Via Pymakr (Cursor/VSCode)
Ctrl+Shift+P → "Pymakr: Upload Project"

# Ou via mpremote
python -m mpremote connect COM3 fs cp -r . :
```

### 4. Acessar Interface

1. Abrir monitor serial para ver IP
2. Acessar: `http://IP_DO_ESP32`
3. Pronto! 🎉

## 📡 API REST

### Sensores

```bash
GET /api/sensors              # Todos os sensores
GET /api/sensors/temperature  # Temperaturas
GET /api/sensors/humidity     # Umidades
GET /api/sensors/current      # Correntes
```

### Relés

```bash
GET  /api/relays              # Estado de todos
GET  /api/relays/0            # Estado do relé 0
POST /api/relays/0            # Controlar relé
     {"action": "on|off|toggle"}
```

### Configuração

```bash
GET  /api/config              # Configuração completa
POST /api/config              # Atualizar config
GET  /api/config/wifi         # Config WiFi
POST /api/config/wifi         # Atualizar WiFi
```

### Sistema

```bash
GET  /api/system/status       # Status do sistema
GET  /api/system/logs         # Logs recentes
GET  /api/system/ping         # Teste de conexão
POST /api/system/restart      # Reiniciar
```

## 🔌 Hardware (Pinout)

| Componente | Pino GPIO |
|------------|-----------|
| DHT22      | GPIO 23   |
| DHT11      | GPIO 22   |
| Relé 1     | GPIO 25   |
| Relé 2     | GPIO 26   |
| Relé 3     | GPIO 32   |
| Relé 4     | GPIO 27   |
| Corrente 1 | GPIO 34   |
| Corrente 2 | GPIO 35   |
| Corrente 3 | GPIO 36   |
| Corrente 4 | GPIO 39   |

## 🎨 Interface

### Páginas Disponíveis

- **Dashboard** - Visão geral do sistema
- **Sensores** - Detalhes dos sensores
- **Relés** - Controle individual
- **Configurações** - WiFi e automação
- **Sistema** - Status e logs

### Responsividade

- **Mobile** (< 768px) - 1 coluna
- **Tablet** (768px+) - 2 colunas
- **Desktop** (1024px+) - 4 colunas

## ⚡ Otimizações

### Frontend
- CSS customizado: **8KB** (vs 150KB Bootstrap)
- Sem jQuery - JavaScript puro
- Componentes modulares
- Cache de assets

### Backend
- Async/await - Não bloqueante
- Garbage collection automático
- JSON database (sem SQL)
- Logs com rotação automática

## 🔒 Segurança

- ✅ Configurações sensíveis em arquivo separado
- ✅ `.gitignore` protege credenciais
- ✅ Validação de inputs
- ⏳ Autenticação (em desenvolvimento)
- ⏳ HTTPS (planejado)

## 📊 Performance

| Métrica | Valor |
|---------|-------|
| Memória RAM livre | ~100KB |
| Tamanho total | ~150KB |
| Latência API | < 100ms |
| Atualização frontend | 5s |
| CSS | 8KB |

## 🐛 Troubleshooting

### ESP32 não conecta ao WiFi
1. Verificar SSID/senha em `config.py`
2. WiFi deve ser 2.4GHz (não 5GHz)
3. Aproximar ESP32 do roteador

### Interface não carrega
1. Verificar IP do ESP32 no monitor serial
2. ESP32 e PC na mesma rede
3. Testar: `curl http://IP_DO_ESP32/api/system/ping`

### Sensores retornam "--"
1. Verificar conexões físicas
2. Alimentação 3.3V ou 5V conforme sensor
3. Pinos GPIO corretos

## 📝 Licença

MIT License - Livre para usar e modificar

## 👨‍💻 Autor

Monitor Miner v2.0 - 2025

---

**Desenvolvido com ❤️ para a comunidade de mineração**

