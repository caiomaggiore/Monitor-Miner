# ============================================================================
# SYSTEM MONITOR SERVICE - Monitor Miner v4.0
# ============================================================================
# Serviço independente para monitoramento do sistema
# - Métricas de CPU, RAM, Flash
# - Histórico de dados
# - Otimizações de memória
# ============================================================================

import gc
import time

class SystemMonitorService:
    """
    Serviço de monitoramento do sistema
    - Métricas em tempo real
    - Histórico de dados
    - Otimizações automáticas
    """
    
    def __init__(self):
        # Configurações
        self.cpu_history_size = 5
        self.memory_history_size = 5
        
        # Timestamps das medições
        self.last_measurements = {
            'cpu': 0,
            'memory': 0,
            'flash': 0,
            'uptime_start': time.ticks_ms()
        }
        
        # Cache de valores
        self.cached_values = {
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
        
        # Históricos
        self.cpu_history = []
        self.memory_history = []
        
        print("[SERVICE] ✅ System Monitor Service inicializado")
    
    def get_cpu_usage(self):
        """Retorna uso de CPU"""
        current_time = time.ticks_ms()
        
        # Medir CPU apenas a cada 1 segundo
        if time.ticks_diff(current_time, self.last_measurements['cpu']) < 1000:
            return self.cached_values['cpu_percent']
        
        # Medição simples de CPU
        start_time = time.ticks_ms()
        
        # Loop simples para medir CPU
        for i in range(500):
            pass
        
        end_time = time.ticks_ms()
        execution_time = time.ticks_diff(end_time, start_time)
        
        # Calcular percentual
        if execution_time > 0:
            cpu_percent = min(100.0, execution_time * 5.0)
        else:
            cpu_percent = 0.0
        
        # Adicionar ao histórico
        self.cpu_history.append(cpu_percent)
        
        # Manter apenas os últimos N valores
        if len(self.cpu_history) > self.cpu_history_size:
            self.cpu_history.pop(0)
        
        # Média simples
        smoothed_cpu = sum(self.cpu_history) / len(self.cpu_history)
        
        self.cached_values['cpu_percent'] = round(smoothed_cpu, 1)
        self.last_measurements['cpu'] = current_time
        
        return self.cached_values['cpu_percent']
    
    def get_memory_usage(self):
        """Retorna uso de memória"""
        current_time = time.ticks_ms()
        
        # Medir memória apenas a cada 5 segundos
        if time.ticks_diff(current_time, self.last_measurements['memory']) < 5000:
            return {
                'free': self.cached_values['memory_free'],
                'total': self.cached_values['memory_total'],
                'percent': self.cached_values['memory_percent']
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
        self.memory_history.append({
            'free': mem_free,
            'total': mem_total,
            'percent': mem_percent
        })
        
        # Manter apenas os últimos N valores
        if len(self.memory_history) > self.memory_history_size:
            self.memory_history.pop(0)
        
        # Média simples
        avg_free = sum(m['free'] for m in self.memory_history) / len(self.memory_history)
        avg_total = sum(m['total'] for m in self.memory_history) / len(self.memory_history)
        avg_percent = sum(m['percent'] for m in self.memory_history) / len(self.memory_history)
        
        self.cached_values['memory_free'] = int(avg_free)
        self.cached_values['memory_total'] = int(avg_total)
        self.cached_values['memory_percent'] = round(avg_percent, 1)
        
        self.last_measurements['memory'] = current_time
        
        return {
            'free': self.cached_values['memory_free'],
            'total': self.cached_values['memory_total'],
            'percent': self.cached_values['memory_percent']
        }
    
    def get_flash_usage(self):
        """Retorna uso de flash"""
        current_time = time.ticks_ms()
        
        # Medir flash apenas a cada 30 segundos
        if time.ticks_diff(current_time, self.last_measurements['flash']) < 30000:
            return {
                'free': self.cached_values['flash_free'],
                'total': self.cached_values['flash_total'],
                'percent': self.cached_values['flash_percent']
            }
        
        # Valores estimados (MicroPython não tem statvfs confiável)
        flash_total = 4096  # 4MB
        flash_free = 1024   # Estimativa baseada em uso típico
        flash_percent = 75.0
        
        self.cached_values['flash_free'] = flash_free
        self.cached_values['flash_total'] = flash_total
        self.cached_values['flash_percent'] = flash_percent
        
        self.last_measurements['flash'] = current_time
        
        return {
            'free': self.cached_values['flash_free'],
            'total': self.cached_values['flash_total'],
            'percent': self.cached_values['flash_percent']
        }
    
    def get_uptime(self):
        """Retorna uptime em segundos"""
        current_time = time.ticks_ms()
        uptime_ms = time.ticks_diff(current_time, self.last_measurements['uptime_start'])
        uptime_seconds = uptime_ms // 1000
        
        self.cached_values['uptime_seconds'] = uptime_seconds
        return uptime_seconds
    
    def get_system_info(self):
        """Retorna informações completas do sistema"""
        current_time = time.ticks_ms()
        
        # Medir métricas
        cpu_percent = self.get_cpu_usage()
        memory_info = self.get_memory_usage()
        flash_info = self.get_flash_usage()
        uptime_seconds = self.get_uptime()
        
        # Atualizar timestamp
        self.cached_values['last_update'] = current_time
        
        # Informações do sistema
        system_info = {
            'version': '4.0.0',
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
            
            # Network
            'network': {
                'uptime': uptime_seconds,
                'connected': True
            }
        }
        
        return system_info
    
    def optimize_memory(self):
        """Otimizações de memória"""
        # Limpar históricos se muito grandes
        if len(self.cpu_history) > self.cpu_history_size:
            self.cpu_history.clear()
        
        if len(self.memory_history) > self.memory_history_size:
            self.memory_history.clear()
        
        # Garbage collection
        gc.collect()
    
    def get_memory_breakdown(self):
        """Retorna quebra do uso de memória"""
        mem_free = gc.mem_free()
        mem_alloc = gc.mem_alloc()
        mem_total = mem_free + mem_alloc
        
        breakdown = {
            'total': mem_total,
            'free': mem_free,
            'used': mem_alloc,
            'components': {
                'micropython_core': 80000,
                'network_stack': 30000,
                'http_server': 20000,
                'application': mem_alloc - 130000 if mem_alloc > 130000 else 10000,
                'cached_files': 0,
                'variables': 10000
            }
        }
        
        return breakdown
    
    def get_stats(self):
        """Retorna estatísticas do serviço"""
        return {
            'cpu_history_size': len(self.cpu_history),
            'memory_history_size': len(self.memory_history),
            'last_cpu_update': self.last_measurements['cpu'],
            'last_memory_update': self.last_measurements['memory'],
            'uptime_seconds': self.get_uptime()
        }

# Instância global do serviço
system_monitor = SystemMonitorService()

# Funções de conveniência para compatibilidade
def get_system_info():
    """Função de conveniência"""
    return system_monitor.get_system_info()

def get_cpu_usage():
    """Função de conveniência"""
    return system_monitor.get_cpu_usage()

def get_memory_usage():
    """Função de conveniência"""
    return system_monitor.get_memory_usage()

def get_flash_usage():
    """Função de conveniência"""
    return system_monitor.get_flash_usage()

def get_uptime():
    """Função de conveniência"""
    return system_monitor.get_uptime()

def optimize_memory():
    """Função de conveniência"""
    return system_monitor.optimize_memory()
