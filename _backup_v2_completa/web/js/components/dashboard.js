/**
 * Dashboard Component
 * Página principal com visão geral do sistema
 */

const Dashboard = {
    data: null,
    updateInterval: null,

    /**
     * Renderiza o HTML do dashboard
     */
    render() {
        return `
            <div class="row">
                <div class="col-12">
                    <h2>📊 Dashboard</h2>
                    <p class="text-muted">Visão geral do sistema em tempo real</p>
                </div>
            </div>

            <!-- Sensores de Temperatura -->
            <div class="row mt-3">
                <div class="col-md-3">
                    <div class="card">
                        <div class="card-body">
                            <div class="card-title">🌡️ Temperatura 1</div>
                            <div class="card-value" id="temp1" style="color: var(--primary)">--</div>
                            <span class="card-unit">°C</span>
                            <div class="mt-2 text-muted" style="font-size: 0.875rem">Sensor DHT22</div>
                        </div>
                    </div>
                </div>

                <div class="col-md-3">
                    <div class="card">
                        <div class="card-body">
                            <div class="card-title">🌡️ Temperatura 2</div>
                            <div class="card-value" id="temp2" style="color: var(--primary)">--</div>
                            <span class="card-unit">°C</span>
                            <div class="mt-2 text-muted" style="font-size: 0.875rem">Sensor DHT11</div>
                        </div>
                    </div>
                </div>

                <div class="col-md-3">
                    <div class="card">
                        <div class="card-body">
                            <div class="card-title">💧 Umidade 1</div>
                            <div class="card-value" id="humid1" style="color: var(--info)">--</div>
                            <span class="card-unit">%</span>
                            <div class="mt-2 text-muted" style="font-size: 0.875rem">Sensor DHT22</div>
                        </div>
                    </div>
                </div>

                <div class="col-md-3">
                    <div class="card">
                        <div class="card-body">
                            <div class="card-title">💧 Umidade 2</div>
                            <div class="card-value" id="humid2" style="color: var(--info)">--</div>
                            <span class="card-unit">%</span>
                            <div class="mt-2 text-muted" style="font-size: 0.875rem">Sensor DHT11</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Sensores de Corrente -->
            <div class="row mt-3">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">⚡ Monitoramento de Corrente</div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-3 text-center">
                                    <div class="text-muted mb-1">Canal 1</div>
                                    <div style="font-size: 1.5rem; font-weight: 600" id="current1">--</div>
                                    <small class="text-muted">Amperes</small>
                                </div>
                                <div class="col-md-3 text-center">
                                    <div class="text-muted mb-1">Canal 2</div>
                                    <div style="font-size: 1.5rem; font-weight: 600" id="current2">--</div>
                                    <small class="text-muted">Amperes</small>
                                </div>
                                <div class="col-md-3 text-center">
                                    <div class="text-muted mb-1">Canal 3</div>
                                    <div style="font-size: 1.5rem; font-weight: 600" id="current3">--</div>
                                    <small class="text-muted">Amperes</small>
                                </div>
                                <div class="col-md-3 text-center">
                                    <div class="text-muted mb-1">Canal 4</div>
                                    <div style="font-size: 1.5rem; font-weight: 600" id="current4">--</div>
                                    <small class="text-muted">Amperes</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Controle de Relés -->
            <div class="row mt-3">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">🔌 Controle de Relés</div>
                        <div class="card-body">
                            <div id="relay-controls" class="row">
                                <!-- Preenchido via JavaScript -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Status do Sistema -->
            <div class="row mt-3">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">📶 Status de Rede</div>
                        <div class="card-body">
                            <div class="d-flex justify-between mb-2">
                                <span>IP:</span>
                                <strong id="wifi-ip">--</strong>
                            </div>
                            <div class="d-flex justify-between mb-2">
                                <span>RSSI:</span>
                                <strong id="wifi-rssi">--</strong>
                            </div>
                            <div class="d-flex justify-between">
                                <span>Status:</span>
                                <span id="wifi-status"><span class="badge badge-success">Conectado</span></span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">💻 Status do Sistema</div>
                        <div class="card-body">
                            <div class="d-flex justify-between mb-2">
                                <span>Uptime:</span>
                                <strong id="system-uptime">--</strong>
                            </div>
                            <div class="d-flex justify-between mb-2">
                                <span>Memória Livre:</span>
                                <strong id="system-memory">--</strong>
                            </div>
                            <div class="d-flex justify-between">
                                <span>Versão:</span>
                                <strong id="system-version">2.0.0</strong>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    },

    /**
     * Inicializa o componente
     */
    async load() {
        await this.update();
        this.startAutoUpdate();
    },

    /**
     * Atualiza os dados do dashboard
     */
    async update() {
        try {
            // Buscar dados de sensores e sistema em paralelo
            const [sensors, relays, system] = await Promise.all([
                api.getSensors().catch(() => null),
                api.getRelays().catch(() => null),
                api.getSystemStatus().catch(() => null)
            ]);

            // Atualizar sensores
            if (sensors) {
                this.updateSensors(sensors);
            }

            // Atualizar relés
            if (relays) {
                this.updateRelays(relays);
            }

            // Atualizar sistema
            if (system) {
                this.updateSystemStatus(system);
            }

        } catch (error) {
            console.error('Error updating dashboard:', error);
        }
    },

    /**
     * Atualiza valores dos sensores
     */
    updateSensors(sensors) {
        // Temperatura
        const temp1 = sensors.temperature?.sensor1;
        const temp2 = sensors.temperature?.sensor2;
        
        const temp1El = document.getElementById('temp1');
        const temp2El = document.getElementById('temp2');
        
        if (temp1El) {
            temp1El.textContent = Utils.formatNumber(temp1);
            temp1El.style.color = Utils.getValueColor(temp1, 'temperature');
        }
        
        if (temp2El) {
            temp2El.textContent = Utils.formatNumber(temp2);
            temp2El.style.color = Utils.getValueColor(temp2, 'temperature');
        }

        // Umidade
        const humid1 = sensors.humidity?.sensor1;
        const humid2 = sensors.humidity?.sensor2;
        
        const humid1El = document.getElementById('humid1');
        const humid2El = document.getElementById('humid2');
        
        if (humid1El) {
            humid1El.textContent = Utils.formatNumber(humid1);
            humid1El.style.color = Utils.getValueColor(humid1, 'humidity');
        }
        
        if (humid2El) {
            humid2El.textContent = Utils.formatNumber(humid2);
            humid2El.style.color = Utils.getValueColor(humid2, 'humidity');
        }

        // Corrente
        for (let i = 1; i <= 4; i++) {
            const current = sensors.current?.[`channel${i}`];
            const el = document.getElementById(`current${i}`);
            if (el) {
                el.textContent = Utils.formatNumber(current, 2);
                el.style.color = Utils.getValueColor(current, 'current');
            }
        }
    },

    /**
     * Atualiza controles dos relés
     */
    updateRelays(relays) {
        const container = document.getElementById('relay-controls');
        if (!container) return;

        let html = '';
        for (let i = 1; i <= 4; i++) {
            const state = relays[`relay${i}`];
            const btnClass = state ? 'btn-success' : 'btn-secondary';
            const stateText = state ? 'ON' : 'OFF';
            const icon = state ? '🟢' : '🔴';

            html += `
                <div class="col-md-3 mb-2">
                    <button class="btn ${btnClass} btn-block" 
                            onclick="Dashboard.toggleRelay(${i - 1})"
                            style="padding: var(--spacing-lg)">
                        <div style="font-size: 1.5rem">${icon}</div>
                        <div style="font-weight: 600; margin-top: var(--spacing-xs)">
                            Relé ${i}
                        </div>
                        <div style="font-size: 0.875rem">
                            ${stateText}
                        </div>
                    </button>
                </div>
            `;
        }

        container.innerHTML = html;
    },

    /**
     * Atualiza status do sistema
     */
    updateSystemStatus(system) {
        // WiFi
        const ipEl = document.getElementById('wifi-ip');
        const rssiEl = document.getElementById('wifi-rssi');
        const statusEl = document.getElementById('wifi-status');
        
        if (ipEl && system.wifi?.ip) {
            ipEl.textContent = system.wifi.ip;
        }
        
        if (rssiEl && system.wifi?.rssi) {
            rssiEl.textContent = `${system.wifi.rssi} dBm`;
        }
        
        if (statusEl) {
            const connected = system.wifi?.connected;
            statusEl.innerHTML = connected
                ? '<span class="badge badge-success">Conectado</span>'
                : '<span class="badge badge-danger">Desconectado</span>';
        }

        // Sistema
        const uptimeEl = document.getElementById('system-uptime');
        const memoryEl = document.getElementById('system-memory');
        const versionEl = document.getElementById('system-version');
        
        if (uptimeEl && system.uptime) {
            uptimeEl.textContent = Utils.formatUptime(system.uptime);
        }
        
        if (memoryEl && system.free_memory) {
            memoryEl.textContent = Utils.formatBytes(system.free_memory);
        }
        
        if (versionEl && system.version) {
            versionEl.textContent = system.version;
        }

        // Atualizar footer uptime
        const footerUptimeEl = document.getElementById('uptime');
        if (footerUptimeEl && system.uptime) {
            footerUptimeEl.textContent = Utils.formatUptime(system.uptime);
        }
    },

    /**
     * Toggle relé
     */
    async toggleRelay(relayId) {
        try {
            // Mostrar feedback visual
            const btn = event.target.closest('button');
            btn.disabled = true;
            btn.style.opacity = '0.6';

            // Enviar comando
            await api.controlRelay(relayId, 'toggle');

            // Atualizar imediatamente
            await this.update();

            // Restaurar botão
            btn.disabled = false;
            btn.style.opacity = '1';

        } catch (error) {
            console.error('Error toggling relay:', error);
            Utils.showToast('Erro ao alternar relé: ' + error.message, 'danger');
            
            // Restaurar botão em caso de erro
            const btn = event.target.closest('button');
            btn.disabled = false;
            btn.style.opacity = '1';
        }
    },

    /**
     * Inicia atualização automática
     */
    startAutoUpdate() {
        // Limpar intervalo anterior se existir
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }

        // Atualizar a cada 5 segundos
        this.updateInterval = setInterval(() => {
            this.update();
        }, 5000);
    },

    /**
     * Para atualização automática
     */
    stopAutoUpdate() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    },

    /**
     * Cleanup ao sair da página
     */
    destroy() {
        this.stopAutoUpdate();
    }
};

