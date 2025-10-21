/**
 * Settings Component - Configurações do sistema
 */

const Settings = {
    config: null,

    render() {
        return `
            <h2>⚙️ Configurações</h2>
            <p class="text-muted">Configure o sistema e os sensores</p>

            <div class="row mt-3">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">📶 Configuração WiFi</div>
                        <div class="card-body">
                            <form id="wifi-form" onsubmit="Settings.saveWifi(event)">
                                <div class="form-group">
                                    <label class="form-label">SSID</label>
                                    <input type="text" class="form-control" id="wifi-ssid" required>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Senha</label>
                                    <input type="password" class="form-control" id="wifi-password">
                                </div>
                                <div class="form-group">
                                    <label class="d-flex align-center gap-2">
                                        <input type="checkbox" id="wifi-dhcp">
                                        <span>Usar DHCP (IP Automático)</span>
                                    </label>
                                </div>
                                <div id="static-ip-fields" style="display:none">
                                    <div class="form-group">
                                        <label class="form-label">IP Estático</label>
                                        <input type="text" class="form-control" id="wifi-ip" 
                                               placeholder="192.168.1.100">
                                    </div>
                                    <div class="form-group">
                                        <label class="form-label">Máscara de Rede</label>
                                        <input type="text" class="form-control" id="wifi-mask" 
                                               value="255.255.255.0">
                                    </div>
                                    <div class="form-group">
                                        <label class="form-label">Gateway</label>
                                        <input type="text" class="form-control" id="wifi-gateway" 
                                               placeholder="192.168.1.1">
                                    </div>
                                </div>
                                <button type="submit" class="btn btn-primary btn-block">Salvar WiFi</button>
                            </form>
                        </div>
                    </div>
                </div>

                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">📊 Configurações de Sensores</div>
                        <div class="card-body">
                            <div class="alert alert-info">
                                Configuração de automação dos sensores será implementada em breve.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    },

    async load() {
        try {
            const config = await api.getConfig();
            this.config = config;
            this.populateFields();
            this.setupListeners();
        } catch (error) {
            console.error('Error loading settings:', error);
        }
    },

    populateFields() {
        if (!this.config) return;

        const wifi = this.config.wifi || {};
        document.getElementById('wifi-ssid').value = wifi.ssid || '';
        document.getElementById('wifi-dhcp').checked = wifi.use_dhcp !== false;
        document.getElementById('wifi-ip').value = wifi.static_ip || '';
        document.getElementById('wifi-mask').value = wifi.subnet_mask || '255.255.255.0';
        document.getElementById('wifi-gateway').value = wifi.gateway || '';
        
        this.toggleStaticIP();
    },

    setupListeners() {
        const dhcpCheckbox = document.getElementById('wifi-dhcp');
        if (dhcpCheckbox) {
            dhcpCheckbox.addEventListener('change', () => this.toggleStaticIP());
        }
    },

    toggleStaticIP() {
        const dhcp = document.getElementById('wifi-dhcp').checked;
        const staticFields = document.getElementById('static-ip-fields');
        if (staticFields) {
            staticFields.style.display = dhcp ? 'none' : 'block';
        }
    },

    async saveWifi(event) {
        event.preventDefault();

        const wifiConfig = {
            ssid: document.getElementById('wifi-ssid').value,
            password: document.getElementById('wifi-password').value || undefined,
            use_dhcp: document.getElementById('wifi-dhcp').checked,
            static_ip: document.getElementById('wifi-ip').value || undefined,
            subnet_mask: document.getElementById('wifi-mask').value || undefined,
            gateway: document.getElementById('wifi-gateway').value || undefined
        };

        // Validar IP se não for DHCP
        if (!wifiConfig.use_dhcp && wifiConfig.static_ip && !Utils.isValidIP(wifiConfig.static_ip)) {
            Utils.showToast('IP inválido', 'danger');
            return;
        }

        try {
            await api.updateWifiConfig(wifiConfig);
            Utils.showToast('Configuração WiFi salva! Reinicie o sistema para aplicar.', 'success');
        } catch (error) {
            console.error('Error saving WiFi config:', error);
            Utils.showToast('Erro ao salvar configuração: ' + error.message, 'danger');
        }
    },

    destroy() {
        // Cleanup
    }
};

