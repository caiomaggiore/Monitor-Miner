/**
 * Sensors Component - Visualização detalhada dos sensores
 */

const Sensors = {
    updateInterval: null,

    render() {
        return `
            <h2>🌡️ Sensores</h2>
            <p class="text-muted">Monitoramento detalhado de todos os sensores</p>

            <div class="row mt-3">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">Sensor 1 - DHT22</div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-6 text-center">
                                    <div class="text-muted mb-2">Temperatura</div>
                                    <div class="card-value" id="s1-temp">--</div>
                                    <span class="card-unit">°C</span>
                                </div>
                                <div class="col-6 text-center">
                                    <div class="text-muted mb-2">Umidade</div>
                                    <div class="card-value" id="s1-humid">--</div>
                                    <span class="card-unit">%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">Sensor 2 - DHT11</div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-6 text-center">
                                    <div class="text-muted mb-2">Temperatura</div>
                                    <div class="card-value" id="s2-temp">--</div>
                                    <span class="card-unit">°C</span>
                                </div>
                                <div class="col-6 text-center">
                                    <div class="text-muted mb-2">Umidade</div>
                                    <div class="card-value" id="s2-humid">--</div>
                                    <span class="card-unit">%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row mt-3">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">⚡ Sensores de Corrente</div>
                        <div class="card-body" id="current-sensors"></div>
                    </div>
                </div>
            </div>
        `;
    },

    async load() {
        await this.update();
        this.startAutoUpdate();
    },

    async update() {
        try {
            const sensors = await api.getSensors();
            
            // Temperatura/Umidade
            document.getElementById('s1-temp').textContent = Utils.formatNumber(sensors.temperature?.sensor1);
            document.getElementById('s1-humid').textContent = Utils.formatNumber(sensors.humidity?.sensor1);
            document.getElementById('s2-temp').textContent = Utils.formatNumber(sensors.temperature?.sensor2);
            document.getElementById('s2-humid').textContent = Utils.formatNumber(sensors.humidity?.sensor2);

            // Corrente
            let html = '<div class="row">';
            for (let i = 1; i <= 4; i++) {
                const current = sensors.current?.[`channel${i}`] || '--';
                html += `
                    <div class="col-md-3 text-center mb-3">
                        <div class="text-muted">Canal ${i}</div>
                        <div style="font-size: 2rem; font-weight: 600; color: ${Utils.getValueColor(current, 'current')}">
                            ${Utils.formatNumber(current, 2)}
                        </div>
                        <small>Amperes</small>
                    </div>
                `;
            }
            html += '</div>';
            document.getElementById('current-sensors').innerHTML = html;

        } catch (error) {
            console.error('Error updating sensors:', error);
        }
    },

    startAutoUpdate() {
        if (this.updateInterval) clearInterval(this.updateInterval);
        this.updateInterval = setInterval(() => this.update(), 5000);
    },

    destroy() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }
};

