/**
 * API Client - Cliente REST para comunicação com backend ESP32
 * Leve e otimizado para ESP32
 */

class API {
    constructor(baseURL = '') {
        this.baseURL = baseURL;
        this.timeout = 10000; // 10 segundos
    }

    /**
     * Requisição HTTP genérica com timeout
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);
        
        try {
            const response = await fetch(url, {
                ...options,
                signal: controller.signal,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            clearTimeout(timeoutId);
            
            if (error.name === 'AbortError') {
                throw new Error('Tempo esgotado: ESP32 não respondeu');
            }
            
            console.error(`API Error [${endpoint}]:`, error);
            throw error;
        }
    }

    // ========================================================================
    // SENSORES
    // ========================================================================

    /**
     * Busca dados de todos os sensores
     */
    async getSensors() {
        return await this.request('/api/sensors');
    }

    /**
     * Busca dados de temperatura
     */
    async getTemperature() {
        return await this.request('/api/sensors/temperature');
    }

    /**
     * Busca dados de umidade
     */
    async getHumidity() {
        return await this.request('/api/sensors/humidity');
    }

    /**
     * Busca dados de corrente
     */
    async getCurrent() {
        return await this.request('/api/sensors/current');
    }

    // ========================================================================
    // RELÉS
    // ========================================================================

    /**
     * Busca estado de todos os relés
     */
    async getRelays() {
        return await this.request('/api/relays');
    }

    /**
     * Busca estado de um relé específico
     */
    async getRelay(relayId) {
        return await this.request(`/api/relays/${relayId}`);
    }

    /**
     * Controla um relé
     * @param {number} relayId - ID do relé (0-3)
     * @param {string} action - Ação: 'on', 'off', 'toggle'
     */
    async controlRelay(relayId, action = 'toggle') {
        return await this.request(`/api/relays/${relayId}`, {
            method: 'POST',
            body: JSON.stringify({ action })
        });
    }

    // ========================================================================
    // CONFIGURAÇÃO
    // ========================================================================

    /**
     * Busca configuração completa
     */
    async getConfig() {
        return await this.request('/api/config');
    }

    /**
     * Atualiza configuração
     */
    async updateConfig(config) {
        return await this.request('/api/config', {
            method: 'POST',
            body: JSON.stringify(config)
        });
    }

    /**
     * Busca configuração de WiFi
     */
    async getWifiConfig() {
        return await this.request('/api/config/wifi');
    }

    /**
     * Atualiza configuração de WiFi
     */
    async updateWifiConfig(wifiConfig) {
        return await this.request('/api/config/wifi', {
            method: 'POST',
            body: JSON.stringify(wifiConfig)
        });
    }

    // ========================================================================
    // SISTEMA
    // ========================================================================

    /**
     * Busca status do sistema
     */
    async getSystemStatus() {
        return await this.request('/api/system/status');
    }

    /**
     * Busca logs do sistema
     */
    async getLogs(limit = 50) {
        return await this.request(`/api/system/logs?limit=${limit}`);
    }

    /**
     * Reinicia o sistema
     */
    async restart() {
        return await this.request('/api/system/restart', {
            method: 'POST'
        });
    }

    /**
     * Ping para verificar conectividade
     */
    async ping() {
        try {
            const start = Date.now();
            await this.request('/api/system/ping');
            const latency = Date.now() - start;
            return { success: true, latency };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
}

// Instância global da API
const api = new API();

