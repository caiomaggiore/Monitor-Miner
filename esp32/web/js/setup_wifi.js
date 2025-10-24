// Setup WiFi - Monitor Miner v3.0 (MINIMAL)
console.log('[JS] setup_wifi.js carregando...');
window.setupJSLoaded = true;
console.log('[JS] setup_wifi.js carregado!');

let selectedNetwork = null;

function scanNetworks() {
    console.log('[JS] scanNetworks() chamada');
    const scanBtn = document.getElementById('scanBtn');
    const loading = document.getElementById('loading');
    const networks = document.getElementById('networks');
    const debug = document.getElementById('debug');

    scanBtn.disabled = true;
    loading.classList.add('active');
    networks.classList.remove('active');
    debug.textContent = 'Buscando redes...';
    
    fetch('/api/scan')
        .then(response => response.json())
        .then(data => {
            debug.textContent = 'Scan OK! ' + (data.networks ? data.networks.length : 0) + ' redes';
            if (data.success && data.networks && data.networks.length > 0) {
                displayNetworks(data.networks);
            } else {
                showEmptyState();
            }
        })
        .catch(error => {
            console.error('[JS] Erro:', error);
            debug.textContent = 'Erro: ' + error.message;
        })
        .finally(() => {
            loading.classList.remove('active');
            scanBtn.disabled = false;
        });
}

function displayNetworks(list) {
    const dropdown = document.getElementById('networkSelect');
    const dropdownSection = document.getElementById('networkDropdownSection');
    
    // Limpar dropdown
    dropdown.innerHTML = '<option value="">Selecione uma rede...</option>';
    
    // Ordenar por força do sinal
    list.sort((a, b) => b.rssi - a.rssi);
    
    // Adicionar redes ao dropdown
    list.forEach(net => {
        const signal = net.rssi > -50 ? '📶📶📶' : net.rssi > -60 ? '📶📶' : net.rssi > -70 ? '📶' : '📡';
        const lock = net.security !== 'Open' ? '🔒' : '🔓';
        const strength = net.rssi > -50 ? 'Excelente' : net.rssi > -60 ? 'Bom' : net.rssi > -70 ? 'Regular' : 'Fraco';
        
        const option = document.createElement('option');
        option.value = net.ssid;
        option.textContent = `${signal} ${net.ssid} ${lock} (${strength})`;
        option.dataset.security = net.security;
        dropdown.appendChild(option);
    });
    
    // Mostrar dropdown
    dropdownSection.style.display = 'block';
}

function showEmptyState() {
    document.getElementById('networks').innerHTML = '<div class="empty-state">📵<p>Nenhuma rede encontrada</p></div>';
    document.getElementById('networks').classList.add('active');
}

function selectNetworkFromDropdown() {
    const dropdown = document.getElementById('networkSelect');
    const ssid = dropdown.value;
    
    if (ssid) {
        console.log('[JS] Rede selecionada:', ssid);
        selectedNetwork = ssid;
        document.getElementById('selectedSsid').value = ssid;
        document.getElementById('password').value = '';
        document.getElementById('formSection').classList.add('active');
        
        // Esconder dropdown após seleção
        document.getElementById('networkDropdownSection').style.display = 'none';
    }
}

function cancelConnection() {
    document.getElementById('formSection').classList.remove('active');
    document.querySelectorAll('.network-item').forEach(i => i.classList.remove('selected'));
    selectedNetwork = null;
}

function connectWiFi() {
    console.log('[JS] connectWiFi() chamada');
    const ssid = selectedNetwork;
    const password = document.getElementById('password').value;
    
    if (!ssid) { 
        showMessage('Selecione uma rede', 'error'); 
        return; 
    }
    
    showMessage('Conectando...', 'success');
    
    fetch('/api/connect', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ssid: ssid, password: password})
    })
    .then(response => response.json())
    .then(data => {
        console.log('[JS] Resposta:', data);
        if (data.success) {
            showMessage('Conectado! Reiniciando...', 'success');
            setTimeout(() => location.href = '/', 3000);
        } else {
            showMessage('Falha: ' + (data.error || 'Erro'), 'error');
        }
    })
    .catch(error => {
        console.error('[JS] Erro:', error);
        showMessage('Erro ao conectar', 'error');
    });
}

function showMessage(text, type) {
    const msg = document.getElementById('message');
    msg.textContent = text;
    msg.className = 'message ' + type + ' active';
}

// Configurar eventos (executa imediatamente)
console.log('[JS] Configurando eventos...');

const debug = document.getElementById('debug');
if (debug) debug.textContent = 'JavaScript OK! Clique no botao.';

document.getElementById('scanBtn').onclick = scanNetworks;
document.getElementById('networkSelect').onchange = selectNetworkFromDropdown;
document.getElementById('cancelBtn').onclick = cancelConnection;
document.getElementById('connectBtn').onclick = connectWiFi;

console.log('[JS] setup_wifi.js configurado com sucesso!');
// BUFFER ANTI-TRUNCAMENTO: Sistema sempre corta os últimos 30 caracteres
// 1234567890123456789012345678901234567890
