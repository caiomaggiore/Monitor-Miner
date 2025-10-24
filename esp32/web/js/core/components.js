/**
 * COMPONENTS v4.0 - Monitor Miner v4.0
 * ============================================================================
 * Componentes UI reutilizáveis
 * - Cards de métricas
 * - Gráficos simples
 * - Formulários
 * - Modais
 * ============================================================================
 */

class UIComponents {
    constructor() {
        this.components = new Map();
        this.theme = 'dark';
        console.log('[UI] ✅ Components v4.0 carregados');
    }

    /**
     * Cria um card de métrica
     */
    createMetricCard(id, title, value, unit, icon, color = 'primary') {
        const card = document.createElement('div');
        card.className = `metric-card metric-card--${color}`;
        card.id = `metric-${id}`;
        
        card.innerHTML = `
            <div class="metric-card__icon">
                <i class="icon-${icon}"></i>
            </div>
            <div class="metric-card__content">
                <div class="metric-card__title">${title}</div>
                <div class="metric-card__value">
                    <span class="metric-card__number">${value}</span>
                    <span class="metric-card__unit">${unit}</span>
                </div>
            </div>
            <div class="metric-card__status">
                <div class="status-indicator status-indicator--online"></div>
            </div>
        `;
        
        return card;
    }

    /**
     * Cria um gráfico simples
     */
    createSimpleChart(id, title, data, type = 'line') {
        const chart = document.createElement('div');
        chart.className = `chart chart--${type}`;
        chart.id = `chart-${id}`;
        
        chart.innerHTML = `
            <div class="chart__header">
                <h3 class="chart__title">${title}</h3>
                <div class="chart__controls">
                    <button class="chart__btn" data-action="refresh">
                        <i class="icon-refresh"></i>
                    </button>
                </div>
            </div>
            <div class="chart__canvas" id="canvas-${id}">
                <div class="chart__placeholder">
                    <i class="icon-chart"></i>
                    <p>Carregando dados...</p>
                </div>
            </div>
        `;
        
        // Renderizar gráfico
        this._renderChart(chart, data, type);
        
        return chart;
    }

    /**
     * Cria um formulário
     */
    createForm(id, fields, submitText = 'Salvar') {
        const form = document.createElement('form');
        form.className = 'form';
        form.id = `form-${id}`;
        
        let formHTML = '<div class="form__fields">';
        
        fields.forEach(field => {
            formHTML += this._createFormField(field);
        });
        
        formHTML += `
            </div>
            <div class="form__actions">
                <button type="submit" class="btn btn--primary">${submitText}</button>
                <button type="button" class="btn btn--secondary" data-action="cancel">Cancelar</button>
            </div>
        `;
        
        form.innerHTML = formHTML;
        
        // Adicionar event listeners
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this._handleFormSubmit(form, fields);
        });
        
        return form;
    }

    /**
     * Cria um modal
     */
    createModal(id, title, content, actions = []) {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.id = `modal-${id}`;
        
        modal.innerHTML = `
            <div class="modal__backdrop"></div>
            <div class="modal__content">
                <div class="modal__header">
                    <h3 class="modal__title">${title}</h3>
                    <button class="modal__close" data-action="close">
                        <i class="icon-close"></i>
                    </button>
                </div>
                <div class="modal__body">
                    ${content}
                </div>
                <div class="modal__footer">
                    ${actions.map(action => `
                        <button class="btn btn--${action.type || 'secondary'}" data-action="${action.action}">
                            ${action.text}
                        </button>
                    `).join('')}
                </div>
            </div>
        `;
        
        // Adicionar event listeners
        modal.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal__backdrop') || 
                e.target.closest('[data-action="close"]')) {
                this.closeModal(modal);
            }
        });
        
        return modal;
    }

    /**
     * Cria uma tabela
     */
    createTable(id, columns, data = []) {
        const table = document.createElement('div');
        table.className = 'table-container';
        table.id = `table-${id}`;
        
        let tableHTML = `
            <div class="table__header">
                <h3 class="table__title">Dados</h3>
                <div class="table__controls">
                    <button class="btn btn--small" data-action="refresh">
                        <i class="icon-refresh"></i>
                    </button>
                </div>
            </div>
            <div class="table__wrapper">
                <table class="table">
                    <thead>
                        <tr>
                            ${columns.map(col => `<th>${col.title}</th>`).join('')}
                        </tr>
                    </thead>
                    <tbody>
                        ${data.map(row => `
                            <tr>
                                ${columns.map(col => `<td>${row[col.key] || '-'}</td>`).join('')}
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
        
        table.innerHTML = tableHTML;
        
        return table;
    }

    /**
     * Cria um alerta
     */
    createAlert(message, type = 'info', duration = 5000) {
        const alert = document.createElement('div');
        alert.className = `alert alert--${type}`;
        
        alert.innerHTML = `
            <div class="alert__content">
                <i class="alert__icon icon-${type}"></i>
                <span class="alert__message">${message}</span>
            </div>
            <button class="alert__close" data-action="close">
                <i class="icon-close"></i>
            </button>
        `;
        
        // Adicionar ao DOM
        document.body.appendChild(alert);
        
        // Auto-remover após duração
        if (duration > 0) {
            setTimeout(() => {
                this.removeAlert(alert);
            }, duration);
        }
        
        // Event listener para fechar
        alert.addEventListener('click', (e) => {
            if (e.target.closest('[data-action="close"]')) {
                this.removeAlert(alert);
            }
        });
        
        return alert;
    }

    /**
     * Atualiza um card de métrica
     */
    updateMetricCard(id, value, unit = null) {
        const card = document.getElementById(`metric-${id}`);
        if (!card) return;
        
        const valueElement = card.querySelector('.metric-card__number');
        if (valueElement) {
            valueElement.textContent = value;
        }
        
        if (unit) {
            const unitElement = card.querySelector('.metric-card__unit');
            if (unitElement) {
                unitElement.textContent = unit;
            }
        }
    }

    /**
     * Atualiza dados de uma tabela
     */
    updateTable(id, data) {
        const table = document.getElementById(`table-${id}`);
        if (!table) return;
        
        const tbody = table.querySelector('tbody');
        if (!tbody) return;
        
        // Limpar dados existentes
        tbody.innerHTML = '';
        
        // Adicionar novos dados
        data.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = Object.values(row).map(value => `<td>${value || '-'}</td>`).join('');
            tbody.appendChild(tr);
        });
    }

    /**
     * Mostra modal
     */
    showModal(modal) {
        modal.style.display = 'block';
        document.body.classList.add('modal-open');
    }

    /**
     * Fecha modal
     */
    closeModal(modal) {
        modal.style.display = 'none';
        document.body.classList.remove('modal-open');
    }

    /**
     * Remove alerta
     */
    removeAlert(alert) {
        if (alert && alert.parentNode) {
            alert.parentNode.removeChild(alert);
        }
    }

    /**
     * Cria campo de formulário
     */
    _createFormField(field) {
        const fieldHTML = `
            <div class="form__field form__field--${field.type}">
                <label class="form__label" for="${field.id}">${field.label}</label>
                ${this._createFormInput(field)}
                ${field.help ? `<div class="form__help">${field.help}</div>` : ''}
            </div>
        `;
        
        return fieldHTML;
    }

    /**
     * Cria input de formulário
     */
    _createFormInput(field) {
        switch (field.type) {
            case 'text':
            case 'email':
            case 'password':
                return `<input type="${field.type}" id="${field.id}" name="${field.name}" class="form__input" value="${field.value || ''}" ${field.required ? 'required' : ''}>`;
            
            case 'select':
                const options = field.options.map(opt => 
                    `<option value="${opt.value}" ${opt.selected ? 'selected' : ''}>${opt.text}</option>`
                ).join('');
                return `<select id="${field.id}" name="${field.name}" class="form__select" ${field.required ? 'required' : ''}>${options}</select>`;
            
            case 'textarea':
                return `<textarea id="${field.id}" name="${field.name}" class="form__textarea" ${field.required ? 'required' : ''}>${field.value || ''}</textarea>`;
            
            case 'checkbox':
                return `<input type="checkbox" id="${field.id}" name="${field.name}" class="form__checkbox" ${field.checked ? 'checked' : ''}>`;
            
            default:
                return `<input type="text" id="${field.id}" name="${field.name}" class="form__input" value="${field.value || ''}">`;
        }
    }

    /**
     * Manipula submit do formulário
     */
    _handleFormSubmit(form, fields) {
        const formData = new FormData(form);
        const data = {};
        
        fields.forEach(field => {
            data[field.name] = formData.get(field.name);
        });
        
        // Emitir evento customizado
        form.dispatchEvent(new CustomEvent('formSubmit', {
            detail: { data, form }
        }));
    }

    /**
     * Renderiza gráfico
     */
    _renderChart(container, data, type) {
        const canvas = container.querySelector('.chart__canvas');
        if (!canvas) return;
        
        // Implementação básica de gráfico
        if (type === 'line') {
            this._renderLineChart(canvas, data);
        } else if (type === 'bar') {
            this._renderBarChart(canvas, data);
        }
    }

    /**
     * Renderiza gráfico de linha
     */
    _renderLineChart(canvas, data) {
        // Implementação básica
        canvas.innerHTML = `
            <div class="chart__line">
                <div class="chart__line-path" style="height: 100px; background: linear-gradient(45deg, #007bff, #28a745);"></div>
            </div>
        `;
    }

    /**
     * Renderiza gráfico de barras
     */
    _renderBarChart(canvas, data) {
        // Implementação básica
        canvas.innerHTML = `
            <div class="chart__bars">
                <div class="chart__bar" style="height: 60%;"></div>
                <div class="chart__bar" style="height: 80%;"></div>
                <div class="chart__bar" style="height: 40%;"></div>
            </div>
        `;
    }
}

// Instância global
window.UIComponents = UIComponents;
window.ui = new UIComponents();

console.log('[UI] 🎨 Componentes UI v4.0 prontos!');
