# Monitor Miner v2.0 - ESP32

Sistema de monitoramento para mineração de Bitcoin rodando em ESP32 com MicroPython.

## 📋 Estrutura

```
/
├── boot.py          # Inicialização WiFi AP
├── main.py          # Servidor web + APIs
├── web/
│   └── index.html   # Interface web
└── microdot.py      # Framework web
```

## 🚀 Como Usar

### 1. Instalar MicroPython no ESP32

```bash
esptool --chip esp32 --port COM5 erase_flash
esptool --chip esp32 --port COM5 write_flash -z 0x1000 firmware.bin
```

### 2. Copiar Microdot

Baixe do GitHub: [Microdot](https://github.com/miguelgrinberg/microdot)

Arquivo: `src/microdot/microdot.py`

### 3. Upload dos Arquivos

Use Thonny ou mpremote:

```bash
mpremote connect COM5 fs cp boot.py :boot.py
mpremote connect COM5 fs cp main.py :main.py
mpremote connect COM5 fs mkdir :web
mpremote connect COM5 fs cp web/index.html :web/index.html
mpremote connect COM5 fs cp microdot.py :microdot.py
```

### 4. Reiniciar ESP32

```bash
mpremote connect COM5 reset
```

## 📱 Acesso

1. **Conecte WiFi:** `MonitorMiner_Setup` (sem senha)
2. **Aguarde** receber IP (192.168.4.x)
3. **Navegador:** `http://192.168.4.1:8080`

## 🔧 APIs Disponíveis

- `GET /` - Página principal (Hello World)
- `GET /test` - Teste de API (JSON)
- `GET /api/status` - Status do sistema

## 📊 Requisitos

- **ESP32** (qualquer modelo)
- **MicroPython** v1.20+
- **Microdot** (incluído)
- **Memória:** ~128KB livre mínimo

## 🎯 Características

- ✅ WiFi Access Point com DHCP
- ✅ Servidor web HTTP (porta 8080)
- ✅ APIs REST
- ✅ Interface web responsiva
- ✅ Modo de configuração
- ❌ Captive Portal (removido por instabilidade)

## 📝 Logs

Boot em 7 passos:
1. Desligar interfaces
2. Limpar memória
3. Estabilização WiFi
4. Ativar AP
5. Configurar rede
6. Configurar SSID
7. Verificar

## 🔄 Versões

- **v2.0** - Versão simplificada e estável
- **v1.x** - Versão complexa (deprecated)

## 📚 Licença

MIT

## 👤 Autor

Monitor Miner Team

