# 📱 Captive Portal - Como Funciona

## 🎯 O que é Captive Portal?

É aquele sistema que quando você conecta no WiFi de um **aeroporto, hotel ou Starbucks**, o navegador **abre automaticamente** uma página!

---

## ✅ Implementado no Monitor Miner!

### **Como Funciona:**

1. **Usuário conecta** no WiFi `MonitorMiner_Setup`
2. **Sistema operacional testa** conectividade (tenta acessar google.com, microsoft.com, etc)
3. **ESP32 responde** que TODOS os domínios apontam para `192.168.4.1`
4. **Sistema detecta** que é um Captive Portal
5. **Navegador abre automaticamente** `http://192.168.4.1:8080`

---

## 🔧 Componentes

### 1. **Servidor DNS (Porta 53)**
```python
# Responde a TODAS as requisições DNS com 192.168.4.1
google.com → 192.168.4.1
facebook.com → 192.168.4.1
qualquer-site.com → 192.168.4.1
```

### 2. **Servidor Web (Porta 8080)**
```python
# Serve a página Hello World
http://192.168.4.1:8080 → Página do Monitor Miner
```

---

## 📋 Status da Implementação

### ✅ **O que está funcionando:**
- Access Point (WiFi)
- DHCP (distribuição de IP)
- Servidor Web (porta 8080)
- APIs (/test, /api/status)

### 🔄 **Em implementação:**
- Captive Portal DNS
- Redirecionamento automático

---

## 🚀 Como Testar

### **1. Conecte no WiFi:**
```
SSID: MonitorMiner_Setup
Senha: (sem senha)
```

### **2. Aguarde 2-3 segundos**

### **3. O que deve acontecer:**

**Android/iOS:**
- Notificação: "Entrar na rede"
- Ao clicar, abre a página automaticamente

**Windows:**
- Notificação: "Ação necessária"
- Ao clicar, abre navegador

**Se não abrir automaticamente:**
- Abra navegador manualmente
- Digite: `http://192.168.4.1:8080`
- Ou: `http://192.168.4.1:8080/test`

---

## 💡 Alternativa: Porta 80

Se quiser que funcione **sem :8080** no endereço:

```python
# No main.py, trocar:
port = 8080  # Porta atual

# Por:
port = 80  # Porta HTTP padrão
```

**Vantagem:**
- `http://192.168.4.1` (sem precisar :8080)
- Mais compatível com Captive Portal

**Desvantagem:**
- Windows pode bloquear porta 80

---

## 🧪 Teste Manual

### **No celular/computador conectado:**

```bash
# Teste 1: DNS está funcionando?
ping google.com
# Deve responder de 192.168.4.1

# Teste 2: Servidor respondendo?
curl http://192.168.4.1:8080/test
# Deve retornar JSON

# Teste 3: Página Hello World?
# Abra navegador: http://192.168.4.1:8080
```

---

## 📊 Logs Esperados

```
[BOOT] AP ATIVO!
[BOOT] SSID: MonitorMiner_Setup
[BOOT] IP: 192.168.4.1
[DNS] Captive Portal será ativado após servidor web
[BOOT] Boot completo!
[MAIN] === Monitor Miner v2.0 ===
[MAIN] Modo: AP (Configuração)
[MAIN] Aguardando 2 segundos...
[MAIN] Iniciando Captive Portal...
[DNS] ✅ Captive Portal ativo (porta 53)
[MAIN] ✅ Captive Portal: navegador abrirá automaticamente!
[MAIN] Iniciando servidor HTTP na porta 8080...
Starting async server on 0.0.0.0:8080...
```

---

## ⚠️ Troubleshooting

### Navegador não abre automaticamente

**Causa:** Alguns dispositivos não detectam Captive Portal na porta 8080

**Solução 1:** Trocar para porta 80
**Solução 2:** Abrir manualmente: `http://192.168.4.1:8080`

### DNS não funciona

**Teste:**
```python
# No REPL:
>>> import socket
>>> s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
>>> s.bind(('', 53))
>>> print("DNS porta 53 OK!")
```

---

## 🔍 Próximos Testes

Execute e monitore:
```bash
python start.py
# [8] Monitor de Logs
```

Depois conecte no WiFi `MonitorMiner_Setup` e veja se navegador abre!

---

**Última atualização:** 12/10/2025

