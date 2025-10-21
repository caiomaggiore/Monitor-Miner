"""
Sensor Manager - Gerencia todos os sensores
"""

from machine import Pin
import dht
import uasyncio as asyncio

class SensorManager:
    def __init__(self):
        # Sensores DHT
        try:
            self.dht22 = dht.DHT22(Pin(23))
            self.dht11 = dht.DHT11(Pin(22))
        except Exception as e:
            print(f"Erro ao inicializar sensores DHT: {e}")
            self.dht22 = None
            self.dht11 = None
        
        # Sensores de corrente (ADC)
        # Pinos: 34, 35, 36, 39
        try:
            from machine import ADC, Pin
            self.current_sensors = [
                ADC(Pin(34)),
                ADC(Pin(35)),
                ADC(Pin(36)),
                ADC(Pin(39))
            ]
            for sensor in self.current_sensors:
                sensor.atten(ADC.ATTN_11DB)  # 0-3.6V
                sensor.width(ADC.WIDTH_12BIT)  # 0-4095
        except Exception as e:
            print(f"Erro ao inicializar sensores de corrente: {e}")
            self.current_sensors = []
        
        # Cache de valores
        self.temperature = {'sensor1': '--', 'sensor2': '--'}
        self.humidity = {'sensor1': '--', 'sensor2': '--'}
        self.current = {
            'channel1': 0, 'channel2': 0,
            'channel3': 0, 'channel4': 0
        }
    
    async def read_all(self):
        """Lê todos os sensores"""
        await asyncio.sleep(0)  # Yield
        
        # Ler DHT22
        if self.dht22:
            try:
                self.dht22.measure()
                self.temperature['sensor1'] = self.dht22.temperature()
                self.humidity['sensor1'] = self.dht22.humidity()
            except:
                self.temperature['sensor1'] = '--'
                self.humidity['sensor1'] = '--'
        
        # Ler DHT11
        if self.dht11:
            try:
                self.dht11.measure()
                self.temperature['sensor2'] = self.dht11.temperature()
                self.humidity['sensor2'] = self.dht11.humidity()
            except:
                self.temperature['sensor2'] = '--'
                self.humidity['sensor2'] = '--'
        
        # Ler corrente
        for i, sensor in enumerate(self.current_sensors, 1):
            try:
                raw = sensor.read()
                # Converter ADC para Amperes (calibrar conforme sensor)
                voltage = (raw / 4095) * 3.6
                amperes = (voltage - 1.65) / 0.066  # ACS712 30A
                self.current[f'channel{i}'] = round(max(0, amperes), 2)
            except:
                self.current[f'channel{i}'] = 0
    
    def get_temperature(self):
        """Retorna temperaturas"""
        return self.temperature
    
    def get_humidity(self):
        """Retorna umidades"""
        return self.humidity
    
    def get_current(self):
        """Retorna correntes"""
        return self.current

