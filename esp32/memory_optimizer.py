"""
Memory Optimizer - Monitor Miner v3.2.1
Otimizações para reduzir footprint de memória e melhorar performance
"""

import gc
import time
import os

# ============================================================================
# CONFIGURAÇÕES DE OTIMIZAÇÃO
# ============================================================================

# Limites de memória
MIN_MEMORY_FREE = 50000  # 50KB mínimo livre
CRITICAL_MEMORY_FREE = 30000  # 30KB crítico

# Configurações do Garbage Collector
GC_THRESHOLD_FACTOR = 4  # Threshold = memória_livre / 4 + memória_alocada
GC_COLLECT_INTERVAL = 30000  # 30 segundos

# Cache de arquivos (LRU simples)
MAX_CACHED_FILES = 3
MAX_CACHE_SIZE = 15000  # 15KB máximo de cache

# ============================================================================
# OTIMIZADOR DE MEMÓRIA
# ============================================================================

class MemoryOptimizer:
    def __init__(self):
        self.last_gc_time = time.ticks_ms()
        self.cached_files = {}  # {filename: (content, access_time)}
        self.cache_size = 0
        
    def optimize_gc(self):
        """
        Otimiza configurações do Garbage Collector
        """
        mem_free = gc.mem_free()
        mem_alloc = gc.mem_alloc()
        
        # Configurar threshold dinâmico
        threshold = mem_free // GC_THRESHOLD_FACTOR + mem_alloc
        gc.threshold(threshold)
        
        print(f"[MEMORY] GC threshold: {threshold}")
        
    def smart_gc_collect(self):
        """
        Garbage Collection inteligente baseado em uso de memória
        """
        current_time = time.ticks_ms()
        mem_free = gc.mem_free()
        
        # Verificar se precisa fazer GC
        needs_gc = False
        
        # GC forçado se memória muito baixa
        if mem_free < CRITICAL_MEMORY_FREE:
            needs_gc = True
            print(f"[MEMORY] CRÍTICO: {mem_free}KB livre - GC forçado")
            
        # GC periódico
        elif time.ticks_diff(current_time, self.last_gc_time) > GC_COLLECT_INTERVAL:
            needs_gc = True
            print(f"[MEMORY] Periódico: {mem_free}KB livre - GC")
            
        # GC se memória baixa
        elif mem_free < MIN_MEMORY_FREE:
            needs_gc = True
            print(f"[MEMORY] Baixa: {mem_free}KB livre - GC")
            
        if needs_gc:
            # Medir memória antes
            mem_before = gc.mem_free()
            
            # Executar GC
            collected = gc.collect()
            
            # Medir memória depois
            mem_after = gc.mem_free()
            freed = mem_after - mem_before
            
            print(f"[MEMORY] GC: {collected} objetos, {freed}KB liberados")
            
            self.last_gc_time = current_time
            
            # Reconfigurar threshold após GC
            self.optimize_gc()
            
            return freed
        else:
            return 0
    
    def cache_file(self, filename, content):
        """
        Cache LRU simples para arquivos
        """
        current_time = time.ticks_ms()
        
        # Remover arquivo mais antigo se cache cheio
        if len(self.cached_files) >= MAX_CACHED_FILES:
            oldest_file = min(self.cached_files.keys(), 
                            key=lambda k: self.cached_files[k][1])
            self.remove_from_cache(oldest_file)
        
        # Adicionar novo arquivo
        content_size = len(content)
        
        # Verificar se cabe no cache
        if self.cache_size + content_size > MAX_CACHE_SIZE:
            # Remover arquivos até caber
            while (self.cache_size + content_size > MAX_CACHE_SIZE and 
                   self.cached_files):
                oldest_file = min(self.cached_files.keys(), 
                                key=lambda k: self.cached_files[k][1])
                self.remove_from_cache(oldest_file)
        
        self.cached_files[filename] = (content, current_time)
        self.cache_size += content_size
        
        print(f"[MEMORY] Cache: {filename} ({content_size}B) - Total: {self.cache_size}B")
    
    def get_from_cache(self, filename):
        """
        Recupera arquivo do cache
        """
        if filename in self.cached_files:
            content, access_time = self.cached_files[filename]
            
            # Atualizar tempo de acesso
            self.cached_files[filename] = (content, time.ticks_ms())
            
            return content
        return None
    
    def remove_from_cache(self, filename):
        """
        Remove arquivo do cache
        """
        if filename in self.cached_files:
            content, _ = self.cached_files[filename]
            del self.cached_files[filename]
            self.cache_size -= len(content)
            print(f"[MEMORY] Removido do cache: {filename}")
    
    def clear_cache(self):
        """
        Limpa todo o cache
        """
        self.cached_files.clear()
        self.cache_size = 0
        print("[MEMORY] Cache limpo")
    
    def get_memory_stats(self):
        """
        Retorna estatísticas de memória
        """
        mem_free = gc.mem_free()
        mem_alloc = gc.mem_alloc()
        mem_total = mem_free + mem_alloc
        
        return {
            'total': mem_total,
            'free': mem_free,
            'used': mem_alloc,
            'percent_used': (mem_alloc / mem_total) * 100 if mem_total > 0 else 0,
            'cache_size': self.cache_size,
            'cached_files': len(self.cached_files),
            'gc_threshold': gc.threshold(),
            'gc_count': gc.collect()
        }

# ============================================================================
# OTIMIZAÇÕES ESPECÍFICAS
# ============================================================================

def optimize_strings():
    """
    Otimiza strings para economizar memória
    """
    # Usar bytearray ao invés de strings quando possível
    # Reutilizar buffers
    pass

def optimize_imports():
    """
    Otimiza imports para carregar apenas o necessário
    """
    # Importar apenas funções específicas
    # Evitar imports desnecessários
    pass

def pre_allocate_buffers():
    """
    Pré-aloca buffers para evitar fragmentação
    """
    # Criar buffers reutilizáveis
    global _request_buffer, _response_buffer
    
    try:
        _request_buffer = bytearray(2048)
        _response_buffer = bytearray(8192)
        print("[MEMORY] Buffers pré-alocados")
    except:
        print("[MEMORY] Erro ao pré-alocar buffers")

# ============================================================================
# INSTÂNCIA GLOBAL
# ============================================================================

# Criar instância global do otimizador
memory_optimizer = MemoryOptimizer()

# Pré-alocar buffers
pre_allocate_buffers()

# Configurar GC inicial
memory_optimizer.optimize_gc()

print("[MEMORY] Memory Optimizer inicializado!")
print(f"[MEMORY] Memória inicial: {gc.mem_free()}KB livre")

# ============================================================================
# FUNÇÕES DE INTERFACE
# ============================================================================

def optimize_memory():
    """
    Função principal de otimização (chamada pelo dashboard)
    """
    return memory_optimizer.smart_gc_collect()

def cache_file(filename, content):
    """
    Interface para cache de arquivos
    """
    return memory_optimizer.cache_file(filename, content)

def get_cached_file(filename):
    """
    Interface para recuperar arquivo do cache
    """
    return memory_optimizer.get_from_cache(filename)

def clear_file_cache():
    """
    Interface para limpar cache
    """
    return memory_optimizer.clear_cache()

def get_memory_stats():
    """
    Interface para estatísticas
    """
    return memory_optimizer.get_memory_stats()
