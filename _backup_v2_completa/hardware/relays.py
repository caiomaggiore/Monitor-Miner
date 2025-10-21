"""
Relay Controller - Controla os relés
"""

from machine import Pin
import time

class RelayController:
    def __init__(self):
        # Pinos dos relés: 25, 26, 32, 27
        self.pins = [25, 26, 32, 27]
        self.relays = [Pin(pin, Pin.OUT) for pin in self.pins]
        
        # Inicializar todos desligados
        for relay in self.relays:
            relay.value(0)
        
        # Rastrear tempo de ativação
        self.activation_time = [0, 0, 0, 0]
    
    def turn_on(self, relay_id):
        """Liga um relé"""
        if 0 <= relay_id < 4:
            self.relays[relay_id].value(1)
            self.activation_time[relay_id] = time.time()
    
    def turn_off(self, relay_id):
        """Desliga um relé"""
        if 0 <= relay_id < 4:
            self.relays[relay_id].value(0)
            self.activation_time[relay_id] = 0
    
    def toggle(self, relay_id):
        """Alterna estado de um relé"""
        if 0 <= relay_id < 4:
            current = self.relays[relay_id].value()
            if current:
                self.turn_off(relay_id)
            else:
                self.turn_on(relay_id)
    
    def get_state(self, relay_id):
        """Retorna estado de um relé"""
        if 0 <= relay_id < 4:
            return bool(self.relays[relay_id].value())
        return False
    
    def get_uptime(self, relay_id):
        """Retorna tempo ligado em segundos"""
        if 0 <= relay_id < 4:
            if self.activation_time[relay_id] > 0:
                return int(time.time() - self.activation_time[relay_id])
        return 0
    
    def get_all_states(self):
        """Retorna estado de todos os relés"""
        return {
            f'relay{i+1}': self.get_state(i)
            for i in range(4)
        }

