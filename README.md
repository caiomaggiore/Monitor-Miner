# Monitor Miner v2.0

Sistema de monitoramento e controle para mineração de Bitcoin usando ESP32.

## 📁 Estrutura do Projeto

```
Monitor Miner/
├── docs/                    # 📚 Documentação
│   ├── README.md           # Documentação principal
│   ├── GUIA_RAPIDO.md      # Guia rápido de uso
│   ├── CONFIGURAR_PORTA.md # Como configurar porta COM
│   └── COMPARACAO_V1_V2.md # Diferenças entre versões
│
├── esp32/                   # 🎯 CÓDIGO DO PROJETO PRINCIPAL
│   ├── main.py             # Código principal
│   ├── boot.py             # Boot do ESP32
│   ├── hardware/           # Módulos de hardware
│   ├── services/           # Serviços do sistema
│   ├── web/                # Interface web
│   └── data/               # Dados e logs
│
├── tools/                   # 🔧 Ferramentas de Desenvolvimento
│   ├── esp_manager.py      # ⭐ CLI de gerenciamento
│   ├── upload_esp32.py     # Upload completo
│   ├── test_esp32_simple.py # Teste de conexão
│   ├── diagnose_esp32.py   # Diagnóstico
│   └── ...outras ferramentas...
│
├── firmware/                # 📦 Firmware MicroPython
├── config.py                # ⚙️ Configuração (porta COM, etc)
└── .espignore               # 🚫 Arquivos ignorados no upload
```

## 🚀 Quick Start

### 1️⃣ Configurar Porta ESP32

Edite `config.py` e altere a porta COM:

```python
ESP32_PORT = "COM6"  # Sua porta aqui
```

### 2️⃣ Iniciar o ESP Manager (Recomendado)

```bash
python start.py
```

Ou diretamente:
```bash
python tools/esp_manager.py
```

Interface CLI com todas as funcionalidades:
- 📤 Upload completo e seletivo
- 🔍 Diagnóstico do sistema
- 💾 Verificar espaço e memória
- 🖥️ REPL interativo
- 🧹 Formatação e reset

### 3️⃣ Ou Usar Ferramentas Individuais

```bash
# Testar conexão
python tools/test_esp32_simple.py

# Diagnóstico
python tools/diagnose_esp32.py

# Upload rápido
python tools/simple_upload.py

# Upload completo
python tools/upload_esp32.py
```

## 📋 Workflow Recomendado

### Desenvolvimento
1. Use **ESP Manager** (`python tools/esp_manager.py`) para gestão geral
2. Use **Thonny** para debug e testes rápidos
3. Desenvolva código em `esp32/`

### Deploy
1. Teste localmente
2. Use ESP Manager → **Upload Completo** 
3. Monitore logs no REPL

## 🎯 Ferramentas Principais

### ESP Manager CLI ⭐
```bash
python tools/esp_manager.py
```
Interface completa de gerenciamento com:
- Upload completo da pasta `esp32/`
- Upload seletivo de arquivos
- Diagnóstico e monitoramento
- REPL integrado
- Controle de espaço

### Upload Rápido
```bash
python tools/simple_upload.py
```
Upload simples e direto dos arquivos essenciais.

### Teste de Conexão
```bash
python tools/test_esp32_simple.py
```
Testa conexão, MicroPython, filesystem e espaço.

### Diagnóstico
```bash
python tools/diagnose_esp32.py
```
Verifica MicroPython, arquivos e memória.

### Formatação
```bash
python tools/format_esp32_auto.py
```
Formata e reinstala MicroPython automaticamente.

## 📝 .espignore

Controla quais arquivos **NÃO** devem ser enviados para ESP32:

```gitignore
# Ferramentas
tools/
docs/
config.py

# Arquivos temporários
*.pyc
__pycache__/

# Veja .espignore para lista completa
```

Apenas o conteúdo de `esp32/` é enviado para a placa.

## ⚙️ Configuração

### config.py

```python
# Conexão ESP32
ESP32_PORT = "COM5"          # Porta COM
ESP32_BAUDRATE = 115200      # Baudrate

# WiFi
WIFI_SSID = "SuaRede"
WIFI_PASSWORD = "SuaSenha"

# Sensores
DHT22_PIN = 23
DHT11_PIN = 22

# Relés
RELAY_PINS = [25, 26, 32, 27]
```

## 🔧 Instalação de Dependências

```bash
# Instalar ferramentas Python
pip install mpremote esptool

# Verificar instalação
python tools/test_esp32_simple.py
```

## 📖 Documentação Completa

Consulte a pasta `docs/` para:
- **README.md** - Documentação principal do projeto
- **GUIA_RAPIDO.md** - Guia rápido de uso
- **CONFIGURAR_PORTA.md** - Como configurar porta COM
- **COMPARACAO_V1_V2.md** - Diferenças entre versões

## 🆘 Problemas Comuns

### ESP32 não conecta
1. Verifique porta no Device Manager
2. Edite `config.py` com a porta correta
3. Teste: `python tools/test_esp32_simple.py`

### Erro de upload
1. Use ESP Manager para diagnóstico
2. Verifique espaço disponível
3. Tente formatação se necessário

### Filesystem corrompido
```bash
python tools/format_esp32_auto.py
```

## 🎯 Próximos Passos

1. ✅ Configure a porta em `config.py`
2. ✅ Teste conexão com ESP32
3. ✅ Use ESP Manager para primeiro upload
4. 🚀 Comece a desenvolver em `esp32/`

## 📜 Licença

Monitor Miner v2.0 - Projeto de monitoramento para mineração de Bitcoin

---

**Dica:** Use `python tools/esp_manager.py` como sua ferramenta principal! 🚀

