/**
 * Utils - Funções utilitárias
 */

const Utils = {
    /**
     * Formata timestamp Unix para data/hora legível
     */
    formatDateTime(timestamp) {
        if (!timestamp) return '--';
        const date = new Date(timestamp * 1000);
        return date.toLocaleString('pt-BR');
    },

    /**
     * Formata tempo de uptime (segundos) para formato legível
     */
    formatUptime(seconds) {
        if (!seconds || seconds < 0) return '--';
        
        const days = Math.floor(seconds / 86400);
        const hours = Math.floor((seconds % 86400) / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);
        
        let result = [];
        if (days > 0) result.push(`${days}d`);
        if (hours > 0) result.push(`${hours}h`);
        if (minutes > 0) result.push(`${minutes}m`);
        if (secs > 0 || result.length === 0) result.push(`${secs}s`);
        
        return result.join(' ');
    },

    /**
     * Formata bytes para formato legível
     */
    formatBytes(bytes) {
        if (!bytes || bytes === 0) return '0 B';
        
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        
        return `${(bytes / Math.pow(1024, i)).toFixed(2)} ${sizes[i]}`;
    },

    /**
     * Formata número com casas decimais
     */
    formatNumber(value, decimals = 1) {
        if (value === null || value === undefined || value === '--') return '--';
        return Number(value).toFixed(decimals);
    },

    /**
     * Mostra notificação toast
     */
    showToast(message, type = 'info') {
        // Criar elemento toast
        const toast = document.createElement('div');
        toast.className = `alert alert-${type}`;
        toast.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            max-width: 500px;
            animation: slideIn 0.3s ease;
        `;
        toast.textContent = message;
        
        // Adicionar ao DOM
        document.body.appendChild(toast);
        
        // Remover após 3 segundos
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },

    /**
     * Debounce function
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Verifica se valor está dentro do range
     */
    inRange(value, min, max) {
        return value >= min && value <= max;
    },

    /**
     * Retorna cor baseada no valor (temperatura, umidade, etc)
     */
    getValueColor(value, type) {
        if (value === '--' || value === null) return 'var(--gray-500)';
        
        switch(type) {
            case 'temperature':
                if (value < 20) return 'var(--info)';
                if (value < 30) return 'var(--success)';
                if (value < 35) return 'var(--warning)';
                return 'var(--danger)';
            
            case 'humidity':
                if (value < 40) return 'var(--warning)';
                if (value < 70) return 'var(--success)';
                return 'var(--danger)';
            
            case 'current':
                if (value < 5) return 'var(--success)';
                if (value < 10) return 'var(--warning)';
                return 'var(--danger)';
            
            default:
                return 'var(--primary)';
        }
    },

    /**
     * Sanitiza HTML para prevenir XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    /**
     * Gera ID único
     */
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    },

    /**
     * Valida endereço IP
     */
    isValidIP(ip) {
        const pattern = /^(\d{1,3}\.){3}\d{1,3}$/;
        if (!pattern.test(ip)) return false;
        
        const parts = ip.split('.');
        return parts.every(part => {
            const num = parseInt(part, 10);
            return num >= 0 && num <= 255;
        });
    },

    /**
     * Retorna ícone baseado no tipo
     */
    getIcon(type) {
        const icons = {
            temperature: '🌡️',
            humidity: '💧',
            current: '⚡',
            relay: '🔌',
            wifi: '📶',
            system: '💻',
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        return icons[type] || '•';
    }
};

// Adicionar animações CSS inline para toast
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

