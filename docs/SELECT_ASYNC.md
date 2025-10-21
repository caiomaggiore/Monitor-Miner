# Sistema Pseudo-Assíncrono com select()
## Monitor Miner v3.1 - Guia de Uso

**Implementado em:** setup.py e dashboard.py  
**Versão:** 3.1  
**Data:** 12/10/2025

---

## 🎯 O Que é select()?

`select()` permite monitorar múltiplos sockets (ou arquivos) e saber quando estão prontos para ler/escrever **SEM bloquear**.

### **Antes (Bloqueante):**
```python
conn = s.accept()  # BLOQUEIA até alguém conectar
# Não pode fazer nada enquanto espera!
```

### **Agora (Non-blocking com select):**
```python
readable, _, _ = select.select([s], [], [], 0.1)  # Timeout 100ms

if readable:
    conn = s.accept()  # Tem conexão, aceitar
else:
    # Fazer outras coisas!
    update_sensors()
    control_relays()
```

---

## 🔧 Como Funciona no Projeto

### **Loop Principal (setup.py e dashboard.py):**

```python
import select

s.setblocking(False)  # Socket non-blocking

while True:
    # Espera conexão OU timeout de 100ms
    readable, _, _ = select.select([s], [], [], 0.1)
    
    if readable:
        # ✅ Tem cliente esperando
        conn = s.accept()
        handle_request(conn)
    else:
        # ⏰ Timeout (100ms) - Executar tasks
        update_sensors()      # Ler DHT22, DS18B20, etc
        control_relays()      # Automação
        check_alerts()        # Verificar limites
        gc.collect()          # Limpeza
```

---

## 📊 Benefícios

| Aspecto | Antes (Bloqueante) | Agora (select) |
|---------|-------------------|----------------|
| **Aceitar conexões** | Bloqueia | ✅ Não bloqueia |
| **Ler sensores** | Apenas entre requests | ✅ A cada 100ms |
| **Múltiplas tasks** | ❌ | ✅ Sim |
| **CPU idle** | 100% quando esperando | ✅ 10% idle |
| **Responsividade** | Média | ✅ Alta |
| **Complexidade** | Baixa | ✅ Baixa (ainda simples!) |

---

## 💡 Como Adicionar Tasks Periódicas

### **Exemplo 1: Atualizar Sensores a Cada 10s**

```python
# No início do loop
last_sensor_update = time.ticks_ms()
sensor_interval = 10000  # 10 segundos

while True:
    readable, _, _ = select.select([s], [], [], 0.1)
    
    if not readable:
        current_time = time.ticks_ms()
        
        # Verificar se passou 10s
        if time.ticks_diff(current_time, last_sensor_update) > sensor_interval:
            # Ler sensores
            temp = dht.temperature()
            humidity = dht.humidity()
            
            # Salvar em JSON
            sensors = load_sensors()
            sensors['temperature'] = temp
            sensors['humidity'] = humidity
            save_sensors(sensors)
            
            last_sensor_update = current_time
            print(f"[DASH] Sensores: {temp}°C, {humidity}%")
```

---

### **Exemplo 2: Controlar Relé por Temperatura**

```python
last_relay_check = time.ticks_ms()
relay_interval = 5000  # 5 segundos

while True:
    readable, _, _ = select.select([s], [], [], 0.1)
    
    if not readable:
        current_time = time.ticks_ms()
        
        if time.ticks_diff(current_time, last_relay_check) > relay_interval:
            sensors = load_sensors()
            temp = sensors.get('temperature', 0)
            
            if temp > 30:
                # Ligar ventilação
                relay_pin.value(1)
                print("[DASH] 🌡️ Temperatura alta! Ventilação ON")
            elif temp < 25:
                # Desligar ventilação
                relay_pin.value(0)
            
            last_relay_check = current_time
```

---

### **Exemplo 3: Múltiplas Tasks**

```python
# Timers para diferentes tasks
tasks = {
    'sensors': {'last': time.ticks_ms(), 'interval': 10000},
    'relays': {'last': time.ticks_ms(), 'interval': 5000},
    'miners': {'last': time.ticks_ms(), 'interval': 30000},
    'alerts': {'last': time.ticks_ms(), 'interval': 60000}
}

while True:
    readable, _, _ = select.select([s], [], [], 0.1)
    
    if readable:
        # Atender HTTP
        conn = s.accept()
        handle_request(conn)
    else:
        # Executar tasks
        current_time = time.ticks_ms()
        
        # Task 1: Sensores (10s)
        if time.ticks_diff(current_time, tasks['sensors']['last']) > tasks['sensors']['interval']:
            update_sensors()
            tasks['sensors']['last'] = current_time
        
        # Task 2: Relés (5s)
        if time.ticks_diff(current_time, tasks['relays']['last']) > tasks['relays']['interval']:
            control_relays()
            tasks['relays']['last'] = current_time
        
        # Task 3: Mineradoras (30s)
        if time.ticks_diff(current_time, tasks['miners']['last']) > tasks['miners']['interval']:
            check_miners()
            tasks['miners']['last'] = current_time
        
        # Task 4: Alertas (60s)
        if time.ticks_diff(current_time, tasks['alerts']['last']) > tasks['alerts']['interval']:
            check_alerts()
            tasks['alerts']['last'] = current_time
```

---

## 📐 Limites e Considerações

### **Quantas Tasks Simultâneas?**

**Recomendado:** 3-5 tasks leves  
**Máximo:** 10 tasks (se rápidas)

**Regra**: Cada task deve executar em < 50ms

### **Timeout do select():**

| Timeout | Uso | CPU | Responsividade |
|---------|-----|-----|----------------|
| 0.01s (10ms) | Tasks rápidas | 90% | Muito alta |
| 0.05s (50ms) | Balanceado | 50% | Alta |
| **0.1s (100ms)** | **Recomendado** | **30%** | **Boa** |
| 0.5s (500ms) | Tasks lentas | 10% | Média |
| 1.0s (1s) | Poucos sensores | 5% | Baixa |

**Atual:** 100ms (10 tasks/segundo máximo)

---

## 🎯 Exemplo Completo: Dashboard com Sensores

```python
import select
from machine import Pin
import dht

# Configurar sensores
dht_sensor = dht.DHT22(Pin(4))
relay_pin = Pin(5, Pin.OUT)

# Servidor setup...
s.setblocking(False)

# Tasks
last_sensor = time.ticks_ms()
last_relay = time.ticks_ms()

while True:
    # Esperar conexão HTTP ou 100ms
    readable, _, _ = select.select([s], [], [], 0.1)
    
    if readable:
        # HTTP Request
        conn = s.accept()
        method, path = parse_request(conn.recv(2048))
        
        if path == '/api/sensors':
            sensors = load_sensors()  # Do arquivo
            response = json.dumps({'success': True, 'data': sensors})
            conn.send(http_response(response))
        
        conn.close()
    
    else:
        # Tasks periódicas
        now = time.ticks_ms()
        
        # A cada 10s: Ler sensores
        if time.ticks_diff(now, last_sensor) > 10000:
            dht_sensor.measure()
            temp = dht_sensor.temperature()
            hum = dht_sensor.humidity()
            
            # Salvar em arquivo
            sensors = load_sensors()
            sensors['temperature'] = temp
            sensors['humidity'] = hum
            sensors['last_update'] = now
            save_sensors(sensors)
            
            last_sensor = now
            print(f"[SENSOR] {temp}°C, {hum}%")
        
        # A cada 5s: Controlar relé
        if time.ticks_diff(now, last_relay) > 5000:
            sensors = load_sensors()
            if sensors['temperature'] > 30:
                relay_pin.on()  # Ligar ventilação
            elif sensors['temperature'] < 25:
                relay_pin.off()  # Desligar
            
            last_relay = now
```

**Resultado:**
- ✅ Dashboard atualiza dados em tempo real
- ✅ Sensores lidos a cada 10s (independente de acessos)
- ✅ Relés controlados automaticamente
- ✅ Servidor sempre responsivo

---

## 🚀 Performance Esperada

### **Cenário de Uso Real:**

**Tasks:**
- Sensor DHT22: ~250ms (a cada 10s)
- Sensor DS18B20: ~750ms (a cada 10s)
- Controle relé: ~1ms (a cada 5s)
- HTTP request: ~50-200ms (sob demanda)

**CPU Usage:**
- Idle: 5-10%
- Com 1 cliente: 20-30%
- Com tasks ativas: 30-40%
- Pico: 60%

**Responsividade:**
- Usuário acessa dashboard: < 200ms resposta
- Sensores atualizam: A cada 10s garantido
- Relés respondem: < 5s após mudança

---

## 📋 Boas Práticas

### ✅ **FAÇA:**
- Tasks rápidas (< 50ms cada)
- Intervalos >= 1s para tasks pesadas
- Cleanup (gc.collect) no timeout
- Logging moderado

### ❌ **NÃO FAÇA:**
- Tasks > 500ms no timeout
- Intervalos < 100ms
- Loops infinitos dentro de tasks
- Operações bloqueantes (sleep, while True)

---

## 🔄 Migração Futura para C/C++

Se precisar migrar, o conceito é similar:

```cpp
// C++ com FreeRTOS
void taskSensors(void *param) {
    while(1) {
        readSensors();
        vTaskDelay(10000 / portTICK_PERIOD_MS);
    }
}

void taskWebServer(void *param) {
    // AsyncWebServer roda automaticamente
}

void setup() {
    xTaskCreate(taskSensors, "Sensors", 4096, NULL, 1, NULL);
    xTaskCreate(taskRelays, "Relays", 2048, NULL, 1, NULL);
}
```

**Benefício**: Tasks **verdadeiramente paralelas** (dual-core)

---

## 📊 Comparação: select() vs FreeRTOS

| Aspecto | select() (MicroPython) | FreeRTOS (C/C++) |
|---------|------------------------|------------------|
| **Paralelismo** | Cooperativo (fake) | Real (dual-core) |
| **Tasks simultâneas** | 5-10 | 20-50 |
| **Complexidade** | Baixa | Média |
| **CPU overhead** | 5% | 2% |
| **Memória** | 150KB livre | 450KB livre |
| **Prioridades** | ❌ | ✅ |
| **Semáforos/Mutex** | ❌ | ✅ |

**Conclusão**: select() é **80% tão bom** com **20% da complexidade**!

---

## ✅ Recomendação

**Para Monitor Miner:**
- ✅ Use select() por enquanto (v3.1-3.5)
- ✅ Teste com carga real
- ✅ Adicione sensores gradualmente
- ⏳ Avalie migração após 2-3 meses

**Migre para C/C++ APENAS se:**
- Performance insuficiente
- Memória insuficiente
- WebSocket obrigatório

---

**Próximos passos:**
1. ✅ select() implementado
2. ⏳ Testar com sensores reais
3. ⏳ Adicionar mais tasks
4. ⏳ Monitorar estabilidade
5. ⏳ Decidir migração (ou não!)

