"""
Logger - Sistema de logs estruturado
"""

import time
import json

class Logger:
    LEVELS = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3, 'CRITICAL': 4}
    
    def __init__(self, log_file='data/logs.json', max_size=10240, level='INFO'):
        self.log_file = log_file
        self.max_size = max_size
        self.level = self.LEVELS.get(level, 1)
        self.buffer = []
        self.buffer_size = 50
    
    def _format_time(self):
        """Formata timestamp"""
        try:
            t = time.localtime()
            return f"{t[0]:04d}-{t[1]:02d}-{t[2]:02d} {t[3]:02d}:{t[4]:02d}:{t[5]:02d}"
        except:
            return str(time.time())
    
    def _log(self, level, message, data=None):
        """Log interno"""
        if self.LEVELS.get(level, 0) < self.level:
            return
        
        entry = {
            'timestamp': self._format_time(),
            'level': level,
            'message': str(message)
        }
        
        if data:
            entry['data'] = data
        
        # Print no console
        print(f"[{level}] {message}")
        
        # Adicionar ao buffer
        self.buffer.append(entry)
        
        # Salvar se buffer cheio
        if len(self.buffer) >= self.buffer_size:
            self._flush()
    
    def _flush(self):
        """Salva buffer em arquivo"""
        if not self.buffer:
            return
        
        try:
            # Rotacionar se necessário
            try:
                import os
                if os.stat(self.log_file)[6] > self.max_size:
                    os.rename(self.log_file, self.log_file + '.old')
            except:
                pass
            
            # Escrever logs
            with open(self.log_file, 'a') as f:
                for entry in self.buffer:
                    f.write(json.dumps(entry) + '\n')
            
            self.buffer = []
        except Exception as e:
            print(f"Erro ao salvar logs: {e}")
    
    def get_recent(self, limit=50):
        """Retorna logs recentes"""
        try:
            logs = []
            with open(self.log_file, 'r') as f:
                for line in f:
                    try:
                        logs.append(json.loads(line.strip()))
                    except:
                        pass
            return logs[-limit:]
        except:
            return []
    
    def debug(self, message, data=None):
        self._log('DEBUG', message, data)
    
    def info(self, message, data=None):
        self._log('INFO', message, data)
    
    def warning(self, message, data=None):
        self._log('WARNING', message, data)
    
    def error(self, message, data=None):
        self._log('ERROR', message, data)
    
    def critical(self, message, data=None):
        self._log('CRITICAL', message, data)

