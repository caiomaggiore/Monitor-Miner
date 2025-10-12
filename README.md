# Monitor Miner ESP32 v3.0

Sistema de monitoramento inteligente para sala de mineração de Bitcoin.

## 🏗️ Arquitetura v3.0 - Servidores Síncronos

### ⚡ Descoberta Importante

**Problema**: Microdot + asyncio causa **CRASH FATAL** no ESP32
- Modo AP: Erro -203 (todas portas)
- Modo STA: abort() crash
  
**Solução**: Servidores HTTP síncronos (socket puro) em ambos modos

```
boot.py (70 linhas)
   ├─ WiFi configurado? → Conecta STA → import main.py (Async)
   └─ Não configurado? → Ativa AP → import setup.py (Sync)
```

### 📂 Estrutura

```
esp32/
├── boot.py              # Boot mínimo - verifica e direciona
├── main.py              # Roteador - decide setup vs dashboard
├── setup.py             # Modo AP - Servidor HTTP síncrono
├── dashboard.py         # Modo STA - Servidor HTTP síncrono
├── microdot.py          # (não usado - mantido para referência)
│
├── web/
│   ├── setup.html       # Site Survey (standalone, sem CDN)
│   ├── setup.css        # (opcional - setup.html tem inline)
│   ├── setup.js         # (opcional - setup.html tem inline)
│   └── index.html       # Dashboard
│
└── data/
    ├── config.json      # Configuração WiFi salva
    └── sensors.json     # Dados dos sensores
```

---

## 🚀 Modos de Operação

### **Modo AP (Setup) - Servidor Síncrono**

**Quando:** Primeira vez ou falha na conexão WiFi  
**Servidor:** Socket HTTP puro (síncrono)  
**Performance:** Básica (1 requisição por vez - suficiente)  
**Uso:** Temporário (configuração inicial)

**Como usar:**
1. Conecte ao WiFi: `MonitorMiner_Setup` (sem senha)
2. Acesse: `http://192.168.4.1:8080`
3. Use Site Survey para escolher rede
4. Digite senha e conecte
5. ESP32 reinicia automaticamente
6. Entra em Modo STA ✅

---

### **Modo STA (Dashboard) - Servidor Síncrono**

**Quando:** WiFi configurado e conectado  
**Servidor:** Socket HTTP puro (síncrono)  
**Performance:** Básica mas estável (1 requisição por vez)  
**Uso:** Permanente (operação normal 24/7)

**Como usar:**
1. ESP32 conecta automaticamente ao WiFi
2. Acesse pelo IP: `http://[IP]:8080`
3. Dashboard atualiza dados a cada 5s
4. Controle sensores/relés em tempo real

---

## 📡 APIs Disponíveis

### **Setup (Modo AP - Síncrono)**

#### `GET /`
Serve página `setup.html` (Site Survey)

#### `GET /api/scan`
Escaneia redes WiFi disponíveis.

**Resposta:**
```json
{
  "success": true,
  "networks": [
    {"ssid": "MinhaRede", "rssi": -45, "security": "WPA2-PSK"}
  ],
  "count": 1
}
```

#### `POST /api/connect`
Conecta ao WiFi e reinicia.

**Body:**
```json
{"ssid": "MinhaRede", "password": "senha123"}
```

**Resposta:**
```json
{
  "success": true,
  "ip": "192.168.1.100",
  "message": "Conectado! Reiniciando..."
}
```

---

### **Dashboard (Modo STA - Async)**

#### `GET /`
Serve página `index.html` (Dashboard)

#### `GET /api/sensors`
Retorna dados dos sensores (async).

**Resposta:**
```json
{
  "success": true,
  "data": {
    "temperature": 25.5,
    "humidity": 60.0,
    "miners": {"total": 10, "online": 8, "offline": 2},
    "power": {"consumption": 15.2, "status": "normal"}
  }
}
```

#### `GET /api/status`
Status do sistema (async).

#### `GET /api/config`
Configurações (senha oculta).

---

## 🔄 Fluxo Completo

```
ESP32 Liga
   ↓
[boot.py] Verifica config.json
   ├─ WiFi configurado?
   │   ├─ SIM → Conecta STA
   │   │   ├─ ✅ Conectou → import main.py
   │   │   │                  └→ Dashboard Async
   │   │   │
   │   │   └─ ❌ Falhou → Ativa AP
   │   │                  └→ import setup.py
   │   │                       └→ Site Survey Sync
   │   │
   │   └─ NÃO → Ativa AP
   │            └→ import setup.py
   │                 └→ Site Survey Sync
   │
   └─ Usuário configura WiFi
         └→ Salva config
              └→ Reinicia ESP32
                   └→ Boot → STA → main.py ✅
```

---

## 💻 Detalhes Técnicos

### Por que Híbrido?

**Setup (AP):**
- ✅ Uso único/raro (configuração inicial)
- ✅ 1 usuário por vez
- ✅ Não precisa alta performance
- ✅ Socket síncrono FUNCIONA
- ✅ Código simples e estável

**Dashboard (STA):**
- ✅ Uso contínuo 24/7
- ✅ Múltiplos acessos possíveis
- ✅ Sensores em paralelo
- ✅ Updates real-time
- ✅ Asyncio permite tasks paralelas

### Comparação de Código

**Antes (v2.0):**
```
boot.py: 220 linhas (complexo)
main.py: 494 linhas (misturado)
Total: 714 linhas
```

**Agora (v3.0):**
```
boot.py: 70 linhas (simples)
setup.py: 250 linhas (foco AP)
main.py: 140 linhas (foco STA)
Total: 460 linhas
```

**Redução**: 35% de código mais organizado!

---

## 🧪 Teste de Validação

Criei `test_server_simple.py` que prova:
- ✅ Socket bind funciona em AP
- ❌ Microdot/asyncio falha em AP (erro -203)

**Conclusão**: Servidor híbrido é a solução correta!

---

## 🎨 Interface

Mesma interface linda para ambos modos:
- **Setup**: Site Survey responsivo com FontAwesome
- **Dashboard**: Cards de dados com atualização automática

Design seguindo preferências:
- Montserrat para títulos (UPPERCASE)
- Roboto para texto
- Botões redondos
- Espaçamento moderado

---

## 🌐 Upload para ESP32

```bash
# Na pasta raiz do projeto
python start.py
# [1] Upload Completo
```

Arquivos enviados:
- boot.py, setup.py, main.py, microdot.py
- web/setup.html, web/index.html
- data/config.json, data/sensors.json

---

## 🎯 Próximas Features

- [ ] Integração sensores reais (DHT22)
- [ ] Controle de relés (ventilação)
- [ ] Leitura de mineradoras via API
- [ ] Sistema de alertas
- [ ] WebSocket no main.py (STA)

---

**Versão:** 3.0.0  
**Data:** 12/10/2025  
**Autor:** Caio Maggiore  
**Status:** ✅ Arquitetura Híbrida Implementada
