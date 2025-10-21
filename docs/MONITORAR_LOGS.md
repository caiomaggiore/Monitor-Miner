# 📺 Como Monitorar Logs da ESP32

## 🎯 Formas de Ver os Logs

### 1. **Monitor de Logs (Recomendado)** ⭐
```bash
python start.py
# Escolha [8] - Monitor de Logs
```

**O que faz:**
- Reinicia a ESP32
- Abre o console
- Mostra TODOS os logs da inicialização
- Fica escutando continuamente

**Saída esperada:**
```
ESP32 Reiniciando...
MicroPython v1.21.0 on 2023-10-05; ESP32 module with ESP32
Type "help()" for more information.

>>> [BOOT] Iniciando Monitor Miner v2.0
[BOOT] Carregando configurações...
[WIFI] Conectando em 'SuaRede'...
[WIFI] Conectado! IP: 192.168.1.100
[WEB] Servidor iniciado na porta 80
[INFO] Sistema pronto!
```

---

### 2. **REPL Interativo + Soft Reset**
```bash
python start.py
# Escolha [7] - REPL Interativo
```

**No REPL:**
```python
# Pressione Ctrl+D para soft reset
# Ou digite:
import machine
machine.soft_reset()

# Você verá todos os logs do main.py!
```

**Comandos úteis no REPL:**
```python
# Ver status
import main
main.show_status()

# Ver configuração
import config
print(config.WIFI_SSID)

# Reiniciar
import machine
machine.reset()  # Hard reset
machine.soft_reset()  # Soft reset (melhor para debug)

# Ver memória
import gc
gc.mem_free()

# Listar arquivos
import os
os.listdir('/')
```

---

### 3. **Reset Físico + REPL**
```bash
# 1. Abra o REPL
python start.py
# Escolha [7]

# 2. Pressione botão RESET na ESP32
# 3. Veja os logs aparecerem!
```

---

## 🔧 Comandos Úteis no REPL

### Controle
```python
# Soft reset (recomendado)
Ctrl+D

# Interromper execução
Ctrl+C

# Sair do REPL
Ctrl+]
```

### Debug
```python
# Ver exceções
import sys
sys.print_exception(e)

# Ver trace
import traceback
traceback.print_exc()

# Ver variáveis globais
globals()

# Ver help de módulo
help(main)
```

### Sistema
```python
# Info do sistema
import sys
print(sys.implementation)
print(sys.platform)

# Espaço
import os
os.statvfs('/')

# Memória
import gc
print(f"RAM livre: {gc.mem_free()} bytes")
gc.collect()  # Liberar memória
```

---

## 💡 Dicas para Debug

### 1. **Adicione Prints Estratégicos**
```python
# No seu código
print("[INFO] Iniciando...")
print(f"[DEBUG] Valor: {variavel}")
print("[ERROR] Algo deu errado!")
```

### 2. **Use Try/Except com Logs**
```python
try:
    # Seu código
    conectar_wifi()
except Exception as e:
    print(f"[ERROR] WiFi falhou: {e}")
    import sys
    sys.print_exception(e)
```

### 3. **Logger Estruturado**
```python
# Criar função de log
def log(level, msg):
    print(f"[{level}] {msg}")

log("INFO", "Iniciando sistema")
log("ERROR", "Falha na conexão")
```

### 4. **Status Periódico**
```python
import time

while True:
    print(f"[STATUS] Sistema OK - Memória: {gc.mem_free()}")
    time.sleep(60)  # A cada 1 minuto
```

---

## 🎯 Workflows Comuns

### Desenvolvimento
```bash
# 1. Fazer mudanças no código
# 2. Upload
python start.py  # [1] Upload Completo

# 3. Ver logs
python start.py  # [8] Monitor de Logs

# 4. Se tiver erro, debug no REPL
python start.py  # [7] REPL
>>> import main
>>> # Testar funções manualmente
```

### Debug de Erro
```bash
# 1. Abrir monitor
python start.py  # [8] Monitor de Logs

# 2. Ver onde parou
# Olhar último log antes do erro

# 3. Ir para REPL
Ctrl+]  # Sair do monitor
python start.py  # [7] REPL

# 4. Testar manualmente
>>> import services.wifi
>>> services.wifi.connect()
# Ver erro específico
```

### Monitoramento Contínuo
```bash
# Deixar rodando
python start.py  # [8] Monitor de Logs

# Console ficará aberto mostrando:
# - Conexões
# - Requests HTTP
# - Erros
# - Status
```

---

## 📊 Exemplo de Log Completo

```
🔄 Reiniciando ESP32...
Connected to MicroPython at COM5
Use Ctrl-] to exit this shell

MPY: soft reboot
[BOOT] ==========================================
[BOOT] Monitor Miner v2.0
[BOOT] ==========================================
[BOOT] Carregando configurações...
[CONFIG] WiFi SSID: MinhaRede
[CONFIG] IP Fixo: False
[BOOT] Inicializando hardware...
[HW] DHT22 no pino 23: OK
[HW] DHT11 no pino 22: OK
[HW] Relés: [25, 26, 32, 27]: OK
[BOOT] Conectando WiFi...
[WIFI] Tentando conectar em 'MinhaRede'...
[WIFI] Conectado!
[WIFI] IP: 192.168.1.100
[WIFI] Gateway: 192.168.1.1
[WEB] Iniciando servidor web...
[WEB] Servidor rodando na porta 80
[INFO] ==========================================
[INFO] Sistema pronto!
[INFO] Acesse: http://192.168.1.100
[INFO] ==========================================
[SENSOR] Temperatura: 25.5°C
[SENSOR] Umidade: 65%
[HTTP] GET / - 200
[HTTP] GET /api/status - 200
```

---

## 🚨 Problemas Comuns

### Não vejo logs
```python
# Verifique se há prints no código
# Se não houver, adicione:
print("[INFO] Iniciando...")
```

### Logs param no meio
```python
# Pode ser loop infinito ou erro
# Pressione Ctrl+C para interromper
# Depois Ctrl+D para reiniciar
```

### Console congela
```python
# Ctrl+C para interromper
# Se não funcionar:
# - Feche o terminal
# - Abra novamente
# - Ou pressione botão RESET físico
```

---

## 📚 Referências

- [MicroPython REPL](https://docs.micropython.org/en/latest/esp32/tutorial/repl.html)
- [mpremote docs](https://docs.micropython.org/en/latest/reference/mpremote.html)

---

**Dica:** Use sempre o **Monitor de Logs ([8])** para ver a inicialização completa! 🎯

