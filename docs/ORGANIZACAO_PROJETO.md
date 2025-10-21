# 📁 Organização do Projeto - Monitor Miner

## 🎯 Estrutura Multi-Repositório

O projeto foi dividido em repositórios separados para melhor organização:

### 1. **Monitor Miner** (Código ESP32)
**Repositório:** https://github.com/caiomaggiore/Monitor-Miner

**Conteúdo:**
```
esp32/
├── boot.py          # WiFi AP + Inicialização
├── main.py          # Servidor web + APIs
├── web/
│   └── index.html   # Interface Hello World
├── microdot.py      # Framework
└── README.md
```

**O que vai aqui:**
- Código MicroPython para ESP32
- Interface web (HTML/CSS/JS)
- Bibliotecas MicroPython
- Documentação de uso

---

### 2. **IDE ESP Cursor** (Ferramentas CLI)
**Repositório:** https://github.com/caiomaggiore/IDE-ESP-Cursor

**Conteúdo:**
```
IDE-ESP-Cursor/
├── start.py              # Script principal
├── esp_manager.py        # CLI interativo
├── port_config.py        # Configuração de porta
├── config.example.py     # Template
├── .espignore            # Controle de upload
│
├── test_esp32_simple.py
├── diagnose_esp32.py
├── upload_esp32.py
├── simple_upload.py
├── format_esp32_auto.py
└── ... (13 ferramentas)
```

**O que vai aqui:**
- Ferramentas de desenvolvimento
- Scripts de upload
- Diagnóstico e testes
- Formatação e instalação
- Gerenciador CLI

---

### 3. **Docs** (Documentação - Local)
**Não vai para Git (por enquanto)**

**Conteúdo:**
```
docs/
├── README.md
├── GUIA_RAPIDO.md
├── CONFIGURAR_PORTA.md
├── COMO_USAR.md
├── MONITORAR_LOGS.md
├── ESP32_ESTRUTURA.md
├── INSTALAR_MICRODOT.md
├── MELHORIAS.md
├── ANALISE_MAIN.md
└── CAPTIVE_PORTAL.md
```

---

### 4. **Backup** (Local)
**Não vai para Git**

```
_backup_v2_completa/   # Versão complexa anterior
framework/             # Microdot do GitHub
firmware/              # Binários MicroPython
```

---

## 🔄 Workflow de Desenvolvimento

### **Desenvolvimento ESP32:**
```bash
# 1. Clonar repositório
git clone git@github.com:caiomaggiore/Monitor-Miner.git

# 2. Desenvolver em esp32/

# 3. Testar localmente

# 4. Commit e push
git add .
git commit -m "feat: nova funcionalidade"
git push
```

### **Usando IDE ESP:**
```bash
# 1. Clonar IDE
git clone git@github.com:caiomaggiore/IDE-ESP-Cursor.git

# 2. Configurar porta
cp config.example.py config.py
# Editar config.py

# 3. Usar ferramentas
python start.py
```

### **Upload para ESP32:**
```bash
# Na pasta IDE-ESP-Cursor
python start.py
# [1] Upload Completo
# Aponta para: ../esp32
```

---

## 📦 Como Configurar Projeto Completo

```bash
# Estrutura ideal:
PROJETOS/
├── Monitor-Miner/          # Repositório 1
│   ├── boot.py
│   ├── main.py
│   └── web/
│
└── IDE-ESP-Cursor/         # Repositório 2
    ├── start.py
    ├── esp_manager.py
    └── config.py
```

---

## 🚀 Próximos Passos

### **1. Push Inicial**
```bash
cd esp32
git push -u origin main

cd ../IDE-ESP-Cursor
git push -u origin main
```

### **2. Desenvolvimento**
- Trabalhe em cada repositório independentemente
- Use o IDE para fazer deploy no ESP32
- Commits separados para cada projeto

---

## 📝 Convenções

### **Commits Monitor Miner:**
```
feat: adiciona sensor de temperatura
fix: corrige erro de memória
docs: atualiza README
```

### **Commits IDE ESP:**
```
feat: adiciona upload inteligente
fix: corrige detecção de porta
refactor: simplifica esp_manager
```

---

**Data:** 12/10/2025  
**Versão:** 2.0

