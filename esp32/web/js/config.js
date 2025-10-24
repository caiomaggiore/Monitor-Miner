// Configuração de Sensores - Monitor Miner v3.2.2 (Otimizado)
console.log('[CONFIG] config.js carregando...');
console.log('[CONFIG] DOM ready state:', document.readyState);

// Configurações
const ESP32_PINS = {
    'DHT22': [4, 0, 2, 15, 22, 21],
    'DHT11': [4, 0, 2, 15, 22, 21],
    'Relay': [4, 0, 2, 15, 22, 21, 25, 26, 27, 32, 33],
    'Current': [36, 39, 34, 35, 32, 33],
    'Exaustor': [25, 26, 27, 32, 33]
};

// Menu Hamburger
function toggleMenu() {
    const navLinks = document.getElementById('navLinks');
    navLinks.classList.toggle('active');
}

// Atualizar informações do sistema
async function updateSystemInfo() {
    try {
        console.log('[CONFIG] Fazendo requisição para /api/status...');
        const response = await fetch('/api/status');
        const data = await response.json();
        console.log('[CONFIG] Resposta recebida:', data);
        
        if (data.success && data.data) {
            const system = data.data;
            console.log('[CONFIG] Dados do sistema:', system);
            
            // Atualizar informações do sistema - Primeira linha
            document.getElementById('systemVersion').textContent = system.version || '3.2.2';
            document.getElementById('systemProcessor').textContent = 'Xtensa LX6 Dual-Core @ 240MHz';
            document.getElementById('systemIp').textContent = system.ip || '--';
            
            // Calcular uptime
            const uptimeSeconds = system.uptime || 0;
            const hours = Math.floor(uptimeSeconds / 3600);
            const minutes = Math.floor((uptimeSeconds % 3600) / 60);
            document.getElementById('systemUptime').textContent = `${hours}h ${minutes}m`;

            // Atualizar informações do sistema - Segunda linha
            document.getElementById('systemCPU').textContent = (system.cpu_percent || 0).toFixed(1) + '%';
            
            // RAM: Livre / Total
            const ramFree = system.memory_free || 0;
            const ramTotal = system.memory_total || 320000; // 320KB padrão ESP32
            document.getElementById('systemRAM').textContent = `${formatBytes(ramFree)} / ${formatBytes(ramTotal)}`;
            
            // Flash: Livre / Total
            const flashFree = system.flash_free || 1024;
            const flashTotal = system.flash_total || 4096; // 4MB padrão ESP32
            document.getElementById('systemFlash').textContent = `${formatBytes(flashFree * 1024)} / ${formatBytes(flashTotal * 1024)}`;
            
            // Atualizar timestamp
            const now = new Date();
            document.getElementById('lastUpdate').textContent = 'Última atualização: ' + now.toLocaleTimeString('pt-BR');
            
            console.log('[CONFIG] Informações do sistema atualizadas com sucesso');
        } else {
            console.error('[CONFIG] Resposta inválida:', data);
        }
    } catch (error) {
        console.error('[CONFIG] Erro ao atualizar informações do sistema:', error);
    }
}

// Formatar bytes
function formatBytes(bytes) {
    if (bytes < 1024) return bytes + 'B';
    if (bytes < 1024 * 1024) return Math.round(bytes / 1024) + 'KB';
    return Math.round(bytes / (1024 * 1024)) + 'MB';
}

// Atualizar campos do formulário dinamicamente
function updateFormFields() {
    const itemType = document.getElementById('itemType').value;
    const dynamicFields = document.getElementById('dynamicFields');
    
    if (!itemType) {
        dynamicFields.style.display = 'none';
        return;
    }
    
    dynamicFields.style.display = 'block';
    dynamicFields.innerHTML = generateFields(itemType);
}

// Gerar campos baseado no tipo
function generateFields(type) {
    const pins = ESP32_PINS[type] || [];
    const pinOptions = pins.map(pin => `<option value="${pin}">GPIO ${pin}</option>`).join('');
    
    const baseFields = `
        <div class="form-group">
            <label for="sensorName">Nome:</label>
            <input type="text" id="sensorName" placeholder="Ex: ${type} Principal">
        </div>
        <div class="form-group">
            <label for="sensorEnvironment">Ambiente:</label>
            <select id="sensorEnvironment">
                <option value="sala_quente">🔥 Sala Quente</option>
                <option value="sala_fria">🏠 Sala Fria</option>
            </select>
        </div>
        <div class="form-group">
            <label for="sensorGPIO">GPIO:</label>
            <select id="sensorGPIO">${pinOptions}</select>
        </div>
    `;
    
    if (type === 'Current') {
        return baseFields + `
            <div class="form-group">
                <label for="calibration">Calibração:</label>
                <textarea id="calibration" placeholder="Formato: x1,y1;x2,y2;x3,y3" rows="3"></textarea>
            </div>
        `;
    }
    
    if (type === 'Exaustor') {
        return baseFields + `
            <div class="form-group">
                <label for="relayGPIO">GPIO Relé:</label>
                <select id="relayGPIO">${pinOptions}</select>
            </div>
            <div class="form-group">
                <label for="currentGPIO">GPIO Corrente:</label>
                <select id="currentGPIO">${ESP32_PINS.Current.map(pin => `<option value="${pin}">GPIO ${pin}</option>`).join('')}</select>
            </div>
        `;
    }
    
    return baseFields;
}

// Salvar item
async function saveItem() {
    const itemType = document.getElementById('itemType').value;
    if (!itemType) {
        alert('Selecione um tipo de sensor');
        return;
    }
    
    const sensorData = {
        type: itemType,
        name: document.getElementById('sensorName').value,
        environment: document.getElementById('sensorEnvironment').value,
        gpio: parseInt(document.getElementById('sensorGPIO').value)
    };
    
    if (itemType === 'Current') {
        sensorData.calibration = document.getElementById('calibration').value;
    }
    
    if (itemType === 'Exaustor') {
        sensorData.relay = {
            gpio: parseInt(document.getElementById('relayGPIO').value),
            enabled: true
        };
        sensorData.current = {
            gpio: parseInt(document.getElementById('currentGPIO').value),
            calibration: document.getElementById('calibration')?.value || '',
            enabled: true
        };
    }
    
    try {
        const response = await fetch('/api/sensors/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(sensorData)
        });
        
        const result = await response.json();
        if (result.success) {
            alert('Sensor adicionado com sucesso!');
            cancelAdd();
            loadSensorsConfig();
        } else {
            alert('Erro: ' + result.error);
        }
    } catch (error) {
        console.error('Erro ao salvar sensor:', error);
        alert('Erro ao salvar sensor');
    }
}

// Cancelar adição
function cancelAdd() {
    document.getElementById('itemType').value = '';
    document.getElementById('dynamicFields').style.display = 'none';
}

// Carregar configuração de sensores
async function loadSensorsConfig() {
    try {
        const response = await fetch('/api/sensors/config');
        const data = await response.json();
        
        if (data.success) {
            updateSensorsList(data.data);
        }
    } catch (error) {
        console.error('Erro ao carregar sensores:', error);
    }
}

// Atualizar lista de sensores
function updateSensorsList(config) {
    const sensorsList = document.getElementById('sensorsList');
    
    if (!config.sensors || config.sensors.length === 0) {
        sensorsList.innerHTML = '<p>Nenhum sensor configurado</p>';
        return;
    }
    
    const sensorsHtml = config.sensors.map(sensor => createSensorItem(sensor)).join('');
    sensorsList.innerHTML = sensorsHtml;
}

// Criar item de sensor
function createSensorItem(sensor) {
    const icon = getSensorIcon(sensor.type);
    const details = getSensorDetails(sensor);
    
    return `
        <div class="sensor-item">
            <div class="sensor-info">
                <span class="sensor-icon">${icon}</span>
                <div class="sensor-details">
                    <h4>${sensor.name}</h4>
                    <p>${details}</p>
                </div>
            </div>
            <div class="sensor-actions">
                <button onclick="editSensor('${sensor.id}')" class="btn btn-sm btn-secondary">✏️</button>
                <button onclick="removeSensor('${sensor.id}')" class="btn btn-sm btn-danger">🗑️</button>
            </div>
        </div>
    `;
}

// Obter ícone do sensor
function getSensorIcon(type) {
    const icons = {
        'DHT22': '🌡️',
        'DHT11': '🌡️',
        'Relay': '⚡',
        'Current': '🔌',
        'Exaustor': '🔄'
    };
    return icons[type] || '📡';
}

// Obter detalhes do sensor
function getSensorDetails(sensor) {
    let details = `Tipo: ${sensor.type} | GPIO: ${sensor.gpio}`;
    
    if (sensor.environment) {
        const env = sensor.environment === 'sala_quente' ? '🔥 Sala Quente' : '🏠 Sala Fria';
        details += ` | ${env}`;
    }
    
    if (sensor.relay) {
        details += ` | Relé: GPIO ${sensor.relay.gpio}`;
    }
    
    if (sensor.current) {
        details += ` | Corrente: GPIO ${sensor.current.gpio}`;
    }
    
    return details;
}

// Editar sensor (placeholder)
function editSensor(id) {
    console.log('Editar sensor:', id);
    // TODO: Implementar edição
}

// Remover sensor
async function removeSensor(id) {
    if (!confirm('Tem certeza que deseja remover este sensor?')) return;
    
    try {
        const response = await fetch('/api/sensors/remove', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: id })
        });
        
        const result = await response.json();
        if (result.success) {
            alert('Sensor removido com sucesso!');
            loadSensorsConfig();
        } else {
            alert('Erro: ' + result.error);
        }
    } catch (error) {
        console.error('Erro ao remover sensor:', error);
        alert('Erro ao remover sensor');
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    console.log('[CONFIG] DOM carregado, iniciando...');
    loadSensorsConfig();
    
    // Atualizar informações do sistema imediatamente
    updateSystemInfo();
    
    // Atualizar informações do sistema a cada 10 segundos
    setInterval(updateSystemInfo, 10000);
    
    console.log('[CONFIG] Sistema de atualização configurado');
});

console.log('[CONFIG] config.js carregado!');
console.log('[CONFIG] Elementos encontrados:');
console.log('[CONFIG] - systemVersion:', document.getElementById('systemVersion'));
console.log('[CONFIG] - systemProcessor:', document.getElementById('systemProcessor'));
console.log('[CONFIG] - systemIp:', document.getElementById('systemIp'));
console.log('[CONFIG] - systemUptime:', document.getElementById('systemUptime'));
console.log('[CONFIG] - systemCPU:', document.getElementById('systemCPU'));
console.log('[CONFIG] - systemRAM:', document.getElementById('systemRAM'));
console.log('[CONFIG] - systemFlash:', document.getElementById('systemFlash'));
console.log('[CONFIG] - lastUpdate:', document.getElementById('lastUpdate'));
