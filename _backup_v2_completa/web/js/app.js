/**
 * App - Aplicação Principal (SPA)
 * Gerencia navegação e componentes
 */

class App {
    constructor() {
        this.currentPage = null;
        this.currentComponent = null;
        this.components = {
            'dashboard': Dashboard,
            'sensors': Sensors,
            'relays': Relays,
            'settings': Settings,
            'system': System
        };
        
        this.init();
    }

    /**
     * Inicializa a aplicação
     */
    init() {
        console.log('🔥 Monitor Miner v2.0 - Iniciando...');
        
        // Configurar navegação
        this.setupNavigation();
        
        // Carregar página inicial (dashboard)
        this.loadPage('dashboard');
        
        // Verificar conectividade inicial
        this.checkConnection();
        
        console.log('✅ Aplicação iniciada com sucesso');
    }

    /**
     * Configura eventos de navegação
     */
    setupNavigation() {
        const navLinks = document.querySelectorAll('.nav-link[data-page]');
        
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = e.target.getAttribute('data-page');
                this.loadPage(page);
            });
        });
        
        // Navegação por URL hash (opcional)
        window.addEventListener('hashchange', () => {
            const page = window.location.hash.slice(1) || 'dashboard';
            this.loadPage(page);
        });
        
        // Carregar página do hash se existir
        const initialPage = window.location.hash.slice(1);
        if (initialPage && this.components[initialPage]) {
            return initialPage;
        }
        
        return 'dashboard';
    }

    /**
     * Carrega uma página/componente
     */
    async loadPage(pageName) {
        // Prevenir recarregamento da mesma página
        if (this.currentPage === pageName) {
            return;
        }
        
        console.log(`📄 Carregando página: ${pageName}`);
        
        // Verificar se componente existe
        const Component = this.components[pageName];
        if (!Component) {
            console.error(`Componente não encontrado: ${pageName}`);
            this.showError('Página não encontrada');
            return;
        }
        
        // Destruir componente anterior se existir
        if (this.currentComponent && this.currentComponent.destroy) {
            this.currentComponent.destroy();
        }
        
        // Atualizar estado
        this.currentPage = pageName;
        this.currentComponent = Component;
        
        // Atualizar navbar
        this.updateNavbar(pageName);
        
        // Atualizar hash da URL
        window.location.hash = pageName;
        
        // Obter container
        const appContainer = document.getElementById('app');
        if (!appContainer) {
            console.error('Container #app não encontrado');
            return;
        }
        
        try {
            // Renderizar componente
            appContainer.innerHTML = Component.render();
            
            // Carregar dados do componente
            if (Component.load) {
                await Component.load();
            }
            
            console.log(`✅ Página carregada: ${pageName}`);
            
        } catch (error) {
            console.error(`Erro ao carregar página ${pageName}:`, error);
            this.showError(`Erro ao carregar página: ${error.message}`);
        }
    }

    /**
     * Atualiza navbar (marca link ativo)
     */
    updateNavbar(activePage) {
        const navLinks = document.querySelectorAll('.nav-link[data-page]');
        
        navLinks.forEach(link => {
            const page = link.getAttribute('data-page');
            
            if (page === activePage) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    /**
     * Mostra mensagem de erro
     */
    showError(message) {
        const appContainer = document.getElementById('app');
        if (appContainer) {
            appContainer.innerHTML = `
                <div class="alert alert-danger">
                    <h4>❌ Erro</h4>
                    <p>${Utils.escapeHtml(message)}</p>
                    <button class="btn btn-primary mt-2" onclick="app.loadPage('dashboard')">
                        Voltar ao Dashboard
                    </button>
                </div>
            `;
        }
    }

    /**
     * Verifica conectividade com ESP32
     */
    async checkConnection() {
        try {
            const result = await api.ping();
            
            if (result.success) {
                console.log(`✅ Conexão OK - Latência: ${result.latency}ms`);
                this.updateConnectionStatus(true, result.latency);
            } else {
                console.warn('⚠️ Falha na conexão inicial');
                this.updateConnectionStatus(false);
            }
        } catch (error) {
            console.error('❌ Erro ao verificar conexão:', error);
            this.updateConnectionStatus(false);
        }
    }

    /**
     * Atualiza status de conexão no footer
     */
    updateConnectionStatus(connected, latency = null) {
        const statusBar = document.getElementById('status-bar');
        if (!statusBar) return;
        
        const badge = connected
            ? '<span class="badge badge-success">Conectado</span>'
            : '<span class="badge badge-danger">Desconectado</span>';
        
        const latencyText = latency 
            ? `| Latência: ${latency}ms` 
            : '';
        
        const uptimeText = '<span class="text-muted">| Uptime: <span id="uptime">--</span></span>';
        
        statusBar.innerHTML = `${badge} ${latencyText} ${uptimeText}`;
    }

    /**
     * Recarrega página atual
     */
    reload() {
        if (this.currentPage) {
            const temp = this.currentPage;
            this.currentPage = null;
            this.loadPage(temp);
        }
    }
}

// ============================================================================
// INICIALIZAR APLICAÇÃO
// ============================================================================

let app;

// Aguardar DOM estar pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        app = new App();
    });
} else {
    // DOM já está pronto
    app = new App();
}

// Expor app globalmente para debug
window.app = app;

// Log de versão
console.log('%c🔥 Monitor Miner v2.0', 'font-size: 20px; font-weight: bold; color: #2563eb');
console.log('%cESP32 + MicroPython + API REST', 'font-size: 12px; color: #64748b');

