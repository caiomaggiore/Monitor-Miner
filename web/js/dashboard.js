// Dashboard - Monitor Miner v3.0
console.log('[DASHBOARD] dashboard.js carregando...');

// Atualizar dados
async function updateDashboard() {
    try {
        // Buscar dados dos sensores
        const sensorsResponse = await fetch('/api/sensors');
        const sensorsData = await sensorsResponse.json();

        // Buscar status do sistema
        const statusResponse = await fetch('/api/status');
        const statusData = await statusResponse.json();

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

            // Atualizar informações do sistema
            document.getElementById('systemVersion').textContent = data.version || '3.0';
            document.getElementById('systemMode').textContent = data.mode || '--';
            document.getElementById('systemIp').textContent = data.ip || '--';
            document.getElementById('systemMemory').textContent = 
                ((data.memory_free || 0) / 1024).toFixed(1) + ' KB';
            
            // Calcular uptime
            const uptimeSeconds = data.uptime || 0;
            const hours = Math.floor(uptimeSeconds / 3600);
            const minutes = Math.floor((uptimeSeconds % 3600) / 60);
            document.getElementById('systemUptime').textContent = 
                `${hours}h ${minutes}m`;
        }

        // Atualizar timestamp
        const now = new Date();
        document.getElementById('lastUpdate').textContent = 
            'Última atualização: ' + now.toLocaleTimeString('pt-BR');

        // Mostrar conteúdo
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

console.log('[DASHBOARD] dashboard.js carregado!');

// BUFFER ANTI-TRUNCAMENTO: Sistema sempre corta os últimos 30 caracteres
// 1234567890123456789012345678901234567890

