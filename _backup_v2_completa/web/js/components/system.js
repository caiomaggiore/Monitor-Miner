/**
 * System Component - Informações e controle do sistema
 */

const System = {
    updateInterval: null,

    render() {
        return `
            <h2>💻 Sistema</h2>
            <p class="text-muted">Informações e controle do sistema ESP32</p>

            <div class="row mt-3">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">📊 Informações do Sistema</div>
                        <div class="card-body">
                            <div class="d-flex justify-between mb-3">
                                <span>Versão:</span>
                                <strong id="sys-version">--</strong>
                            </div>
                            <div class="d-flex justify-between mb-3">
                                <span>Uptime:</span>
                                <strong id="sys-uptime">--</strong>
                            </div>
                            <div class="d-flex justify-between mb-3">
                                <span>Memória Livre:</span>
                                <strong id="sys-memory">--</strong>
                            </div>
                            <div class="d-flex justify-between">
                                <span>CPU:</span>
                                <strong>ESP32 (240MHz)</strong>
                            </div>
                        </div>
                    </div>

                    <div class="card mt-3">
                        <div class="card-header">📶 Rede</div>
                        <div class="card-body">
                            <div class="d-flex justify-between mb-3">
                                <span>Status:</span>
                                <span id="net-status">--</span>
                            </div>
                            <div class="d-flex justify-between mb-3">
                                <span>IP:</span>
                                <strong id="net-ip">--</strong>
                            </div>
                            <div class="d-flex justify-between mb-3">
                                <span>RSSI:</span>
                                <strong id="net-rssi">--</strong>
                            </div>
                            <div class="d-flex justify-between">
                                <span>Latência:</span>
                                <strong id="net-latency">--</strong>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">🔧 Ações do Sistema</div>
                        <div class="card-body">
                            <button class="btn btn-primary btn-block mb-2" onclick="System.testConnection()">
                                🔄 Testar Conexão
                            </button>
                            <button class="btn btn-warning btn-block mb-2" onclick="System.confirmRestart()">
                                🔄 Reiniciar Sistema
                            </button>
                            <button class="btn btn-secondary btn-block" onclick="System.refreshData()">
                                ♻️ Atualizar Dados
                            </button>
                        </div>
                    </div>

                    <div class="card mt-3">
                        <div class="card-header">📝 Logs Recentes</div>
                        <div class="card-body">
                            <div id="logs-container" style="max-height: 300px; overflow-y: auto; font-family: var(--font-mono); font-size: 0.875rem">
                                <div class="text-muted">Carregando logs...</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    },

    async load() {
        await this.update();
        await this.loadLogs();
        this.startAutoUpdate();
    },

    async update() {
        try {
            const status = await api.getSystemStatus();
            
            // Sistema
            document.getElementById('sys-version').textContent = status.version || '2.0.0';
            document.getElementById('sys-uptime').textContent = Utils.formatUptime(status.uptime);
            document.getElementById('sys-memory').textContent = Utils.formatBytes(status.free_memory);
            
            // Rede
            const connected = status.wifi?.connected;
            const statusEl = document.getElementById('net-status');
            if (statusEl) {
                statusEl.innerHTML = connected
                    ? '<span class="badge badge-success">Conectado</span>'
                    : '<span class="badge badge-danger">Desconectado</span>';
            }
            
            document.getElementById('net-ip').textContent = status.wifi?.ip || '--';
            document.getElementById('net-rssi').textContent = status.wifi?.rssi 
                ? `${status.wifi.rssi} dBm` 
                : '--';
            
        } catch (error) {
            console.error('Error updating system:', error);
        }
    },

    async loadLogs() {
        try {
            const logs = await api.getLogs(20);
            const container = document.getElementById('logs-container');
            
            if (!logs || logs.length === 0) {
                container.innerHTML = '<div class="text-muted">Nenhum log disponível</div>';
                return;
            }
            
            let html = '';
            logs.forEach(log => {
                const levelClass = {
                    'DEBUG': 'text-muted',
                    'INFO': 'text-primary',
                    'WARNING': 'text-warning',
                    'ERROR': 'text-danger',
                    'CRITICAL': 'text-danger'
                }[log.level] || '';
                
                html += `
                    <div class="mb-2">
                        <span class="${levelClass}">[${log.level}]</span>
                        <span class="text-muted">${log.timestamp}</span>
                        <br>
                        <span>${Utils.escapeHtml(log.message)}</span>
                    </div>
                `;
            });
            
            container.innerHTML = html;
            
        } catch (error) {
            console.error('Error loading logs:', error);
            document.getElementById('logs-container').innerHTML = 
                '<div class="text-danger">Erro ao carregar logs</div>';
        }
    },

    async testConnection() {
        const latencyEl = document.getElementById('net-latency');
        latencyEl.textContent = 'Testando...';
        
        try {
            const result = await api.ping();
            
            if (result.success) {
                latencyEl.textContent = `${result.latency}ms`;
                latencyEl.style.color = result.latency < 100 ? 'var(--success)' : 'var(--warning)';
                Utils.showToast(`Conexão OK! Latência: ${result.latency}ms`, 'success');
            } else {
                latencyEl.textContent = 'Falhou';
                latencyEl.style.color = 'var(--danger)';
                Utils.showToast('Falha na conexão', 'danger');
            }
        } catch (error) {
            latencyEl.textContent = 'Erro';
            latencyEl.style.color = 'var(--danger)';
            Utils.showToast('Erro ao testar conexão', 'danger');
        }
    },

    confirmRestart() {
        if (confirm('Tem certeza que deseja reiniciar o sistema?')) {
            this.restart();
        }
    },

    async restart() {
        try {
            Utils.showToast('Reiniciando sistema...', 'warning');
            await api.restart();
            
            // Aguardar 3 segundos e recarregar página
            setTimeout(() => {
                window.location.reload();
            }, 3000);
            
        } catch (error) {
            console.error('Error restarting system:', error);
            Utils.showToast('Erro ao reiniciar: ' + error.message, 'danger');
        }
    },

    async refreshData() {
        Utils.showToast('Atualizando dados...', 'info');
        await this.update();
        await this.loadLogs();
        Utils.showToast('Dados atualizados!', 'success');
    },

    startAutoUpdate() {
        if (this.updateInterval) clearInterval(this.updateInterval);
        this.updateInterval = setInterval(() => this.update(), 10000);
    },

    destroy() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }
};

