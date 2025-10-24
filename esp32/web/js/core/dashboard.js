/**
 * DASHBOARD v4.0 - Monitor Miner v4.0
 * ============================================================================
 * Dashboard principal usando componentes reutilizáveis
 * - Métricas do sistema
 * - Gráficos em tempo real
 * - Atualizações automáticas
 * ============================================================================
 */

class Dashboard {
    constructor() {
        this.updateInterval = 5000; // 5 segundos
        this.updateTimer = null;
        this.metrics = {};
        this.charts = {};
        
        console.log('[DASHBOARD] ✅ Dashboard v4.0 inicializado');
    }

    /**
     * Inicializa o dashboard
     */
    init() {
        this.createLayout();
        this.bindEvents();
        this.startAutoUpdate();
        
        console.log('[DASHBOARD] 🚀 Dashboard iniciado');
    }

    /**
     * Cria layout do dashboard
     */
    createLayout() {
        const container = document.getElementById('dashboard-container');
        if (!container) return;

        // Limpar container
        container.innerHTML = '';

        // Header
        const header = this.createHeader();
        container.appendChild(header);

        // Métricas do sistema
        const metricsSection = this.createMetricsSection();
        container.appendChild(metricsSection);

        // Gráficos
        const chartsSection = this.createChartsSection();
        container.appendChild(chartsSection);

        // Sensores
        const sensorsSection = this.createSensorsSection();
        container.appendChild(sensorsSection);
    }

    /**
     * Cria header do dashboard
     */
    createHeader() {
        const header = document.createElement('div');
        header.className = 'dashboard-header';
        
        header.innerHTML = `
            <div class="dashboard-header__content">
                <h1 class="dashboard-header__title">
                    <i class="icon-monitor"></i>
                    Monitor Miner v4.0
                </h1>
                <div class="dashboard-header__status">
                    <div class="status-indicator status-indicator--online"></div>
                    <span class="status-text">Online</span>
                </div>
            </div>
            <div class="dashboard-header__actions">
                <button class="btn btn--small" data-action="refresh">
                    <i class="icon-refresh"></i>
                    Atualizar
                </button>
                <button class="btn btn--small" data-action="settings">
                    <i class="icon-settings"></i>
                    Configurações
                </button>
            </div>
        `;
        
        return header;
    }

    /**
     * Cria seção de métricas
     */
    createMetricsSection() {
        const section = document.createElement('div');
        section.className = 'dashboard-section';
        section.id = 'metrics-section';
        
        section.innerHTML = `
            <div class="section-header">
                <h2 class="section-title">Métricas do Sistema</h2>
                <div class="section-actions">
                    <button class="btn btn--small" data-action="refresh-metrics">
                        <i class="icon-refresh"></i>
                    </button>
                </div>
            </div>
            <div class="metrics-grid" id="metrics-grid">
                <!-- Métricas serão adicionadas aqui -->
            </div>
        `;
        
        return section;
    }

    /**
     * Cria seção de gráficos
     */
    createChartsSection() {
        const section = document.createElement('div');
        section.className = 'dashboard-section';
        section.id = 'charts-section';
        
        section.innerHTML = `
            <div class="section-header">
                <h2 class="section-title">Gráficos</h2>
                <div class="section-actions">
                    <button class="btn btn--small" data-action="refresh-charts">
                        <i class="icon-refresh"></i>
                    </button>
                </div>
            </div>
            <div class="charts-grid" id="charts-grid">
                <!-- Gráficos serão adicionados aqui -->
            </div>
        `;
        
        return section;
    }

    /**
     * Cria seção de sensores
     */
    createSensorsSection() {
        const section = document.createElement('div');
        section.className = 'dashboard-section';
        section.id = 'sensors-section';
        
        section.innerHTML = `
            <div class="section-header">
                <h2 class="section-title">Sensores</h2>
                <div class="section-actions">
                    <button class="btn btn--small" data-action="add-sensor">
                        <i class="icon-plus"></i>
                        Adicionar
                    </button>
                </div>
            </div>
            <div class="sensors-grid" id="sensors-grid">
                <!-- Sensores serão adicionados aqui -->
            </div>
        `;
        
        return section;
    }

    /**
     * Vincula eventos
     */
    bindEvents() {
        // Eventos de botões
        document.addEventListener('click', (e) => {
            const action = e.target.closest('[data-action]');
            if (!action) return;
            
            const actionName = action.dataset.action;
            this.handleAction(actionName, action);
        });

        // Eventos de formulários
        document.addEventListener('formSubmit', (e) => {
            this.handleFormSubmit(e.detail);
        });
    }

    /**
     * Manipula ações
     */
    handleAction(action, element) {
        switch (action) {
            case 'refresh':
                this.refreshAll();
                break;
            case 'refresh-metrics':
                this.updateMetrics();
                break;
            case 'refresh-charts':
                this.updateCharts();
                break;
            case 'add-sensor':
                this.showAddSensorModal();
                break;
            case 'settings':
                this.openSettings();
                break;
        }
    }

    /**
     * Manipula submit de formulário
     */
    handleFormSubmit(detail) {
        const { data, form } = detail;
        
        if (form.id === 'form-add-sensor') {
            this.addSensor(data);
        }
    }

    /**
     * Inicia atualização automática
     */
    startAutoUpdate() {
        this.updateTimer = setInterval(() => {
            this.updateMetrics();
            this.updateSensors();
        }, this.updateInterval);
    }

    /**
     * Para atualização automática
     */
    stopAutoUpdate() {
        if (this.updateTimer) {
            clearInterval(this.updateTimer);
            this.updateTimer = null;
        }
    }

    /**
     * Atualiza todas as métricas
     */
    async refreshAll() {
        try {
            await Promise.all([
                this.updateMetrics(),
                this.updateSensors(),
                this.updateCharts()
            ]);
            
            ui.createAlert('Dados atualizados com sucesso!', 'success');
        } catch (error) {
            console.error('[DASHBOARD] Erro ao atualizar:', error);
            ui.createAlert('Erro ao atualizar dados', 'error');
        }
    }

    /**
     * Atualiza métricas do sistema
     */
    async updateMetrics() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            this.metrics = data;
            this.renderMetrics(data);
            
        } catch (error) {
            console.error('[DASHBOARD] Erro ao obter métricas:', error);
        }
    }

    /**
     * Atualiza dados dos sensores
     */
    async updateSensors() {
        try {
            const response = await fetch('/api/sensors');
            const data = await response.json();
            
            this.renderSensors(data.sensors || []);
            
        } catch (error) {
            console.error('[DASHBOARD] Erro ao obter sensores:', error);
        }
    }

    /**
     * Atualiza gráficos
     */
    updateCharts() {
        // Implementar atualização de gráficos
        console.log('[DASHBOARD] Atualizando gráficos...');
    }

    /**
     * Renderiza métricas
     */
    renderMetrics(data) {
        const grid = document.getElementById('metrics-grid');
        if (!grid) return;

        // Limpar métricas existentes
        grid.innerHTML = '';

        // CPU
        const cpuCard = ui.createMetricCard(
            'cpu',
            'CPU',
            data.cpu_percent || 0,
            '%',
            'cpu',
            'primary'
        );
        grid.appendChild(cpuCard);

        // Memória
        const memoryCard = ui.createMetricCard(
            'memory',
            'Memória',
            data.memory_free || 0,
            'KB',
            'memory',
            'info'
        );
        grid.appendChild(memoryCard);

        // Flash
        const flashCard = ui.createMetricCard(
            'flash',
            'Flash',
            data.flash_free || 0,
            'KB',
            'storage',
            'warning'
        );
        grid.appendChild(flashCard);

        // Uptime
        const uptimeCard = ui.createMetricCard(
            'uptime',
            'Uptime',
            this.formatUptime(data.uptime || 0),
            '',
            'clock',
            'success'
        );
        grid.appendChild(uptimeCard);
    }

    /**
     * Renderiza sensores
     */
    renderSensors(sensors) {
        const grid = document.getElementById('sensors-grid');
        if (!grid) return;

        // Limpar sensores existentes
        grid.innerHTML = '';

        if (sensors.length === 0) {
            grid.innerHTML = `
                <div class="empty-state">
                    <i class="icon-sensor"></i>
                    <p>Nenhum sensor configurado</p>
                    <button class="btn btn--primary" data-action="add-sensor">
                        Adicionar Sensor
                    </button>
                </div>
            `;
            return;
        }

        sensors.forEach(sensor => {
            const sensorCard = ui.createMetricCard(
                sensor.id,
                sensor.name,
                sensor.value,
                sensor.unit,
                sensor.type,
                sensor.status === 'online' ? 'success' : 'error'
            );
            grid.appendChild(sensorCard);
        });
    }

    /**
     * Mostra modal para adicionar sensor
     */
    showAddSensorModal() {
        const fields = [
            {
                id: 'sensor-name',
                name: 'name',
                label: 'Nome do Sensor',
                type: 'text',
                required: true
            },
            {
                id: 'sensor-type',
                name: 'type',
                label: 'Tipo',
                type: 'select',
                options: [
                    { value: 'temperature', text: 'Temperatura' },
                    { value: 'humidity', text: 'Umidade' },
                    { value: 'pressure', text: 'Pressão' },
                    { value: 'light', text: 'Luz' }
                ],
                required: true
            },
            {
                id: 'sensor-pin',
                name: 'pin',
                label: 'Pino GPIO',
                type: 'text',
                required: true
            }
        ];

        const form = ui.createForm('add-sensor', fields, 'Adicionar Sensor');
        const modal = ui.createModal('add-sensor', 'Adicionar Sensor', form.outerHTML, [
            { action: 'close', text: 'Cancelar', type: 'secondary' }
        ]);

        document.body.appendChild(modal);
        ui.showModal(modal);
    }

    /**
     * Adiciona sensor
     */
    async addSensor(data) {
        try {
            const response = await fetch('/api/sensors', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                ui.createAlert('Sensor adicionado com sucesso!', 'success');
                this.updateSensors();
            } else {
                throw new Error('Erro ao adicionar sensor');
            }
        } catch (error) {
            console.error('[DASHBOARD] Erro ao adicionar sensor:', error);
            ui.createAlert('Erro ao adicionar sensor', 'error');
        }
    }

    /**
     * Abre configurações
     */
    openSettings() {
        window.location.href = '/config';
    }

    /**
     * Formata uptime
     */
    formatUptime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        return `${hours}h ${minutes}m`;
    }
}

// Inicializar dashboard quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new Dashboard();
    dashboard.init();
    
    // Tornar disponível globalmente
    window.dashboard = dashboard;
});

console.log('[DASHBOARD] 🎯 Dashboard v4.0 carregado!');
