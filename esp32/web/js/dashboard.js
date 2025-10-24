// Dashboard - Monitor Miner v3.0
console.log('[DASHBOARD] dashboard.js carregando...');

// Menu Hamburger
function toggleMenu() {
    const navLinks = document.getElementById('navLinks');
    navLinks.classList.toggle('active');
}

// Atualizar informações do sistema
function updateSystemInfo(systemData) {
    try {
        // Atualizar informações do processador
        if (systemData.processor) {
            document.getElementById('systemProcessor').textContent = systemData.processor.model;
            document.getElementById('systemCPU').textContent = systemData.processor.cpu_percent + '%';
        }
        
        // Atualizar informações de RAM (usar IDs corretos)
        if (systemData.memory) {
            const ramElement = document.getElementById('systemRAM');
            if (ramElement) {
                ramElement.textContent = `${formatBytes(systemData.memory.free)} / ${formatBytes(systemData.memory.total)}`;
            }
        }
        
        // Atualizar informações de Flash (usar IDs corretos)
        if (systemData.storage) {
            const flashElement = document.getElementById('systemFlash');
            if (flashElement) {
                flashElement.textContent = `${formatBytes(systemData.storage.free * 1024)} / ${formatBytes(systemData.storage.total * 1024)}`;
            }
        }
        
        // Atualizar IP e uptime
        if (systemData.network) {
            document.getElementById('systemIp').textContent = systemData.network.ip;
            document.getElementById('systemUptime').textContent = formatUptime(systemData.network.uptime);
        }
    } catch (error) {
        console.error('[DASHBOARD] Erro ao atualizar informações do sistema:', error);
    }
}

// Formatar bytes para KB/MB
function formatBytes(bytes) {
    if (bytes < 1024) return bytes + 'B';
    if (bytes < 1024 * 1024) return Math.round(bytes / 1024) + 'KB';
    return Math.round(bytes / (1024 * 1024)) + 'MB';
}

// Formatar uptime em segundos para formato legível
function formatUptime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
        return `${hours}h ${minutes}m ${secs}s`;
    } else if (minutes > 0) {
        return `${minutes}m ${secs}s`;
    } else {
        return `${secs}s`;
    }
}

// Atualizar dados
async function updateDashboard() {
    console.log('[DASHBOARD] Atualizando dashboard...');
    try {
        // Buscar dados dos sensores
        const sensorsResponse = await fetch('/api/sensors');
        const sensorsData = await sensorsResponse.json();

        // Buscar status do sistema
        const statusResponse = await fetch('/api/status');
        const statusData = await statusResponse.json();
        console.log('[DASHBOARD] Status recebido:', statusData);
        
        // Atualizar informações do sistema
        if (statusData.success) {
            updateSystemInfo(statusData.data);
        }

        if (sensorsData.success) {
            const data = sensorsData.data;

            // Atualizar temperatura
            document.getElementById('temperature').textContent = 
                data.temperature ? data.temperature.toFixed(1) + '°C' : '--°C';

            // Atualizar umidade
            document.getElementById('humidity').textContent = 
                data.humidity ? data.humidity.toFixed(0) + '%' : '--%';

            // Atualizar mineradoras
            document.getElementById('minersTotal').textContent = data.miners.total || 0;
            document.getElementById('minersOnline').textContent = data.miners.online || 0;
            document.getElementById('minersOffline').textContent = data.miners.offline || 0;

            // Atualizar energia
            document.getElementById('powerConsumption').textContent = 
                (data.power.consumption || 0).toFixed(2) + ' kW';
            document.getElementById('powerStatus').textContent = 
                'Status: ' + (data.power.status || 'Desconhecido');
        }

        if (statusData.success) {
            const data = statusData.data;
            
            // Atualizar informações do sistema - Primeira linha
            document.getElementById('systemVersion').textContent = data.version || '3.0';
            document.getElementById('systemProcessor').textContent = 'Xtensa LX6 Dual-Core @ 240MHz';
            document.getElementById('systemIp').textContent = data.ip || '--';
            
            // Calcular uptime
            const uptimeSeconds = data.uptime || 0;
            const hours = Math.floor(uptimeSeconds / 3600);
            const minutes = Math.floor((uptimeSeconds % 3600) / 60);
            document.getElementById('systemUptime').textContent = 
                `${hours}h ${minutes}m`;

            // Atualizar informações do sistema - Segunda linha
            document.getElementById('systemCPU').textContent = 
                (data.cpu_percent || 0).toFixed(1) + '%';
            
            // RAM: Livre / Total
            const ramFree = data.memory_free || 0;
            const ramTotal = data.memory_total || 320000; // 320KB padrão ESP32
            document.getElementById('systemRAM').textContent = 
                `${formatBytes(ramFree)} / ${formatBytes(ramTotal)}`;
            
            // Flash: Livre / Total
            const flashFree = data.flash_free || 0;
            const flashTotal = data.flash_total || 4096; // 4MB padrão ESP32
            document.getElementById('systemFlash').textContent = 
                `${formatBytes(flashFree * 1024)} / ${formatBytes(flashTotal * 1024)}`;
        }

        // Atualizar timestamp
        const now = new Date();
        document.getElementById('lastUpdate').textContent = 
            'Última atualização: ' + now.toLocaleTimeString('pt-BR');

        // Mostrar conteúdo
        console.log('[DASHBOARD] Mostrando conteúdo...');
        document.getElementById('loading').style.display = 'none';
        document.getElementById('cardsGrid').style.display = 'grid';
        document.getElementById('systemInfo').style.display = 'block';

    } catch (error) {
        console.error('Erro ao atualizar dashboard:', error);
        document.getElementById('loading').innerHTML = 
            '<p style="color: #f44336;">❌ Erro ao carregar dados</p>';
    }
}

// Atualizar a cada 5 segundos
setInterval(updateDashboard, 5000);

// Carregar dados ao iniciar
window.addEventListener('load', updateDashboard);

// Inicialização imediata
document.addEventListener('DOMContentLoaded', function() {
    console.log('[DASHBOARD] DOM carregado, iniciando...');
    updateDashboard();
});

console.log('[DASHBOARD] dashboard.js carregado!');

// BUFFER ANTI-TRUNCAMENTO: Sistema sempre corta os últimos 30 caracteres
// 1234567890123456789012345678901234567890

