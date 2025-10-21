/**
 * Relays Component - Controle detalhado dos relés
 */

const Relays = {
    updateInterval: null,

    render() {
        return `
            <h2>🔌 Controle de Relés</h2>
            <p class="text-muted">Controle e monitoramento individual dos relés</p>

            <div id="relays-container" class="row mt-3"></div>
        `;
    },

    async load() {
        await this.update();
        this.startAutoUpdate();
    },

    async update() {
        try {
            const relays = await api.getRelays();
            const container = document.getElementById('relays-container');
            
            let html = '';
            for (let i = 1; i <= 4; i++) {
                const state = relays[`relay${i}`];
                const btnClass = state ? 'btn-success' : 'btn-danger';
                const stateText = state ? 'LIGADO' : 'DESLIGADO';
                const icon = state ? '🟢' : '🔴';
                const actionBtn = state ? 'Desligar' : 'Ligar';
                
                html += `
                    <div class="col-md-6 mb-3">
                        <div class="card">
                            <div class="card-header d-flex justify-between align-center">
                                <span>Relé ${i}</span>
                                <span class="badge ${state ? 'badge-success' : 'badge-danger'}">${stateText}</span>
                            </div>
                            <div class="card-body">
                                <div class="text-center mb-3">
                                    <div style="font-size: 4rem">${icon}</div>
                                    <div style="font-size: 1.5rem; font-weight: 600">${stateText}</div>
                                </div>
                                <div class="row gap-2">
                                    <div class="col-md-6">
                                        <button class="btn ${btnClass} btn-block" 
                                                onclick="Relays.control(${i-1}, '${state ? 'off' : 'on'}')">
                                            ${actionBtn}
                                        </button>
                                    </div>
                                    <div class="col-md-6">
                                        <button class="btn btn-secondary btn-block" 
                                                onclick="Relays.control(${i-1}, 'toggle')">
                                            Alternar
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }
            
            if (container) container.innerHTML = html;
        } catch (error) {
            console.error('Error updating relays:', error);
        }
    },

    async control(relayId, action) {
        try {
            await api.controlRelay(relayId, action);
            Utils.showToast(`Relé ${relayId + 1} ${action === 'on' ? 'ligado' : action === 'off' ? 'desligado' : 'alternado'}`, 'success');
            await this.update();
        } catch (error) {
            console.error('Error controlling relay:', error);
            Utils.showToast('Erro ao controlar relé: ' + error.message, 'danger');
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

