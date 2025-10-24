"""
System Monitor Simples - Monitor Miner v3.2.2
Versão simplificada e compatível com MicroPython
"""

import gc
import time

# ============================================================================
# CONFIGURAÇÕES SIMPLES
# ============================================================================

# Histórico simples (lista ao invés de deque)
CPU_HISTORY_SIZE = 5
MEMORY_HISTORY_SIZE = 5

# Timestamps das medições
last_measurements = {
    'cpu': 0,
    'memory': 0,
    'flash': 0,
    'uptime_start': time.ticks_ms()
}

# Cache de valores
cached_values = {
    'cpu_percent': 0.0,
    'memory_free': 0,
    'memory_total': 0,
    'memory_percent': 0.0,
    'flash_free': 1024,
    'flash_total': 4096,
    'flash_percent': 75.0,
    'uptime_seconds': 0,
    'last_update': 0
}

# Históricos simples (listas)
cpu_history = []
memory_history = []

# ============================================================================
# FUNÇÕES SIMPLIFICADAS
# ============================================================================

def measure_cpu_usage():
    """
    Mede uso de CPU de forma simples
    """
    global last_measurements, cached_values
    
    current_time = time.ticks_ms()
    
    # Medir CPU apenas a cada 1 segundo
    if time.ticks_diff(current_time, last_measurements['cpu']) < 1000:
        return cached_values['cpu_percent']
    
    # Medição simples de CPU
    start_time = time.ticks_ms()
    
    # Loop simples
    for i in range(500):  # Menos iterações para MicroPython
        pass
    
    end_time = time.ticks_ms()
    execution_time = time.ticks_diff(end_time, start_time)
    
    # Calcular percentual simples
    if execution_time > 0:
        cpu_percent = min(100.0, execution_time * 5.0)  # Fator simplificado
    else:
        cpu_percent = 0.0
    
    # Adicionar ao histórico
    cpu_history.append(cpu_percent)
    
    # Manter apenas os últimos N valores
    if len(cpu_history) > CPU_HISTORY_SIZE:
        cpu_history.pop(0)  # Remove o primeiro
    
    # Média simples
    smoothed_cpu = sum(cpu_history) / len(cpu_history)
    
    cached_values['cpu_percent'] = round(smoothed_cpu, 1)
    last_measurements['cpu'] = current_time
    
    return cached_values['cpu_percent']

def measure_memory_usage():
    """
    Mede uso de memória de forma simples
    """
    global last_measurements, cached_values
    
    current_time = time.ticks_ms()
    
    # Medir memória apenas a cada 5 segundos
    if time.ticks_diff(current_time, last_measurements['memory']) < 5000:
        return {
            'free': cached_values['memory_free'],
            'total': cached_values['memory_total'],
            'percent': cached_values['memory_percent']
        }
    
    # Medição real de memória
    mem_free = gc.mem_free()
    mem_alloc = gc.mem_alloc()
    mem_total = mem_free + mem_alloc
    
    # Calcular percentual usado
    if mem_total > 0:
        mem_percent = (mem_alloc / mem_total) * 100
    else:
        mem_percent = 0.0
    
    # Adicionar ao histórico
    memory_history.append({
        'free': mem_free,
        'total': mem_total,
        'percent': mem_percent
    })
    
    # Manter apenas os últimos N valores
    if len(memory_history) > MEMORY_HISTORY_SIZE:
        memory_history.pop(0)  # Remove o primeiro
    
    # Média simples
    avg_free = sum(m['free'] for m in memory_history) / len(memory_history)
    avg_total = sum(m['total'] for m in memory_history) / len(memory_history)
    avg_percent = sum(m['percent'] for m in memory_history) / len(memory_history)
    
    cached_values['memory_free'] = int(avg_free)
    cached_values['memory_total'] = int(avg_total)
    cached_values['memory_percent'] = round(avg_percent, 1)
    
    last_measurements['memory'] = current_time
    
    return {
        'free': cached_values['memory_free'],
        'total': cached_values['memory_total'],
        'percent': cached_values['memory_percent']
    }

def measure_flash_usage():
    """
    Mede uso de flash de forma simples (estimativas)
    """
    global last_measurements, cached_values
    
    current_time = time.ticks_ms()
    
    # Medir flash apenas a cada 30 segundos
    if time.ticks_diff(current_time, last_measurements['flash']) < 30000:
        return {
            'free': cached_values['flash_free'],
            'total': cached_values['flash_total'],
            'percent': cached_values['flash_percent']
        }
    
    # Valores estimados (MicroPython não tem statvfs confiável)
    flash_total = 4096  # 4MB
    flash_free = 1024   # Estimativa baseada em uso típico
    flash_percent = 75.0
    
    cached_values['flash_free'] = flash_free
    cached_values['flash_total'] = flash_total
    cached_values['flash_percent'] = flash_percent
    
    last_measurements['flash'] = current_time
    
    return {
        'free': cached_values['flash_free'],
        'total': cached_values['flash_total'],
        'percent': cached_values['flash_percent']
    }

def get_uptime():
    """
    Calcula uptime real em segundos
    """
    current_time = time.ticks_ms()
    uptime_ms = time.ticks_diff(current_time, last_measurements['uptime_start'])
    uptime_seconds = uptime_ms // 1000
    
    cached_values['uptime_seconds'] = uptime_seconds
    return uptime_seconds

def get_system_info():
    """
    Retorna informações completas do sistema (versão simplificada)
    """
    current_time = time.ticks_ms()
    
    # Medir métricas
    cpu_percent = measure_cpu_usage()
    memory_info = measure_memory_usage()
    flash_info = measure_flash_usage()
    uptime_seconds = get_uptime()
    
    # Atualizar timestamp
    cached_values['last_update'] = current_time
    
    # Informações do sistema simplificadas
    system_info = {
        'version': '3.2.2',
        'mode': 'STA',
        'uptime': uptime_seconds,
        'timestamp': current_time,
        
        # CPU
        'cpu_percent': cpu_percent,
        'processor': {
            'model': 'Xtensa LX6 Dual-Core',
            'cores': 2,
            'frequency': 240,
            'cpu_percent': cpu_percent
        },
        
        # Memória
        'memory_free': memory_info['free'],
        'memory_total': memory_info['total'],
        'memory_used': memory_info['total'] - memory_info['free'],
        'memory_percent': memory_info['percent'],
        'memory': {
            'total': memory_info['total'],
            'free': memory_info['free'],
            'used': memory_info['total'] - memory_info['free'],
            'percent_used': memory_info['percent']
        },
        
        # Flash
        'flash_total': flash_info['total'],
        'flash_free': flash_info['free'],
        'flash_used': flash_info['total'] - flash_info['free'],
        'flash_percent': flash_info['percent'],
        'storage': {
            'total': flash_info['total'],
            'free': flash_info['free'],
            'used': flash_info['total'] - flash_info['free'],
            'percent_used': flash_info['percent']
        },
        
        # Network (será preenchido pelo dashboard.py)
        'network': {
            'uptime': uptime_seconds,
            'connected': True
        }
    }
    
    return system_info

def optimize_memory():
    """
    Otimizações simples de memória
    """
    # Limpar históricos se muito grandes
    if len(cpu_history) > CPU_HISTORY_SIZE:
        cpu_history.clear()
    
    if len(memory_history) > MEMORY_HISTORY_SIZE:
        memory_history.clear()
    
    # Garbage collection simples
    gc.collect()

def get_memory_usage_breakdown():
    """
    Quebra o uso de memória por componente (versão simples)
    """
    mem_free = gc.mem_free()
    mem_alloc = gc.mem_alloc()
    mem_total = mem_free + mem_alloc
    
    # Estimativas simples
    breakdown = {
        'total': mem_total,
        'free': mem_free,
        'used': mem_alloc,
        'components': {
            'micropython_core': 80000,  # ~80KB
            'network_stack': 30000,     # ~30KB
            'http_server': 20000,       # ~20KB
            'application': mem_alloc - 130000 if mem_alloc > 130000 else 10000,
            'cached_files': 0,
            'variables': 10000          # ~10KB
        }
    }
    
    return breakdown

def init_system_monitor():
    """
    Inicializa o monitor de sistema
    """
    print("[MONITOR] Inicializando System Monitor Simples v3.2.2...")
    
    # Resetar timestamps
    current_time = time.ticks_ms()
    last_measurements['uptime_start'] = current_time
    last_measurements['cpu'] = current_time
    last_measurements['memory'] = current_time
    last_measurements['flash'] = current_time
    
    # Limpar históricos
    cpu_history.clear()
    memory_history.clear()
    
    # Primeira medição
    measure_cpu_usage()
    measure_memory_usage()
    measure_flash_usage()
    
    print("[MONITOR] System Monitor Simples inicializado!")
    print(f"[MONITOR] CPU: {cached_values['cpu_percent']}%")
    print(f"[MONITOR] RAM: {cached_values['memory_free']}KB livre")
    print(f"[MONITOR] Flash: {cached_values['flash_free']}KB livre")

# Auto-inicialização quando importado
init_system_monitor()
