# 📚 Guia de Repositórios - Monitor Miner

## 🎯 Projetos Separados

### **1. Monitor Miner (ESP32)**
🔗 **GitHub:** https://github.com/caiomaggiore/Monitor-Miner  
📁 **Pasta:** `esp32/`

**Conteúdo:**
- Código MicroPython para ESP32
- Interface web (HTML/CSS/JS)
- APIs REST
- Servidor HTTP

**Arquivos:**
- `boot.py` - Inicialização WiFi
- `main.py` - Servidor + APIs
- `web/index.html` - Interface
- `microdot.py` - Framework

---

### **2. IDE ESP Cursor**
🔗 **GitHub:** https://github.com/caiomaggiore/IDE-ESP-Cursor  
📁 **Pasta:** `IDE-ESP-Cursor/`

**Conteúdo:**
- Ferramentas CLI para ESP32
- Sistema de upload inteligente
- Diagnóstico e testes
- Gerenciador interativo

**Arquivos principais:**
- `start.py` - Script de inicialização
- `esp_manager.py` - CLI principal
- `port_config.py` - Configuração
- 13 ferramentas auxiliares

---

## 🚀 Como Usar

### **Setup Inicial**

```bash
# 1. Executar script de configuração
setup_repos.bat

# 2. Fazer push inicial
cd esp32
git push -u origin main

cd ../IDE-ESP-Cursor
git push -u origin main
```

---

### **Desenvolvimento ESP32**

```bash
# Trabalhar no código ESP32
cd esp32
# Editar boot.py, main.py, etc.

# Commit
git add .
git commit -m "feat: adiciona nova funcionalidade"
git push

# Deploy na ESP32 (usar IDE)
cd ../IDE-ESP-Cursor
python start.py
# [1] Upload Completo
```

---

### **Desenvolvimento IDE**

```bash
# Trabalhar nas ferramentas
cd IDE-ESP-Cursor
# Editar esp_manager.py, etc.

# Commit
git add .
git commit -m "feat: melhora upload inteligente"
git push
```

---

## 📁 Estrutura Local

```
Monitor Miner/
│
├── esp32/                    # Repositório 1: Monitor-Miner
│   ├── .git/
│   ├── boot.py
│   ├── main.py
│   └── web/
│
├── IDE-ESP-Cursor/           # Repositório 2: IDE-ESP-Cursor
│   ├── .git/
│   ├── start.py
│   └── esp_manager.py
│
├── docs/                     # Local (não versionado)
├── _backup_v2_completa/      # Local (não versionado)
├── framework/                # Local (não versionado)
└── firmware/                 # Local (não versionado)
```

---

## 🔄 Workflow Completo

### **1. Clonar Projetos (novo ambiente)**

```bash
# Clonar ESP32
git clone git@github.com:caiomaggiore/Monitor-Miner.git

# Clonar IDE
git clone git@github.com:caiomaggiore/IDE-ESP-Cursor.git

# Configurar IDE
cd IDE-ESP-Cursor
cp config.example.py config.py
# Editar config.py com sua porta
```

### **2. Desenvolver**

```bash
# Editar código ESP32
cd Monitor-Miner
# Fazer mudanças

# Testar
cd ../IDE-ESP-Cursor
python start.py
# [1] Upload Completo (aponta para ../Monitor-Miner)
# [8] Monitor de Logs
```

### **3. Versionar**

```bash
# Commit ESP32
cd Monitor-Miner
git add .
git commit -m "feat: nova feature"
git push

# Commit IDE (se mudou)
cd ../IDE-ESP-Cursor
git add .
git commit -m "fix: correção"
git push
```

---

## 📦 Dependências

### **Monitor Miner (ESP32)**
- MicroPython v1.20+
- Microdot (incluído)

### **IDE ESP Cursor**
- Python 3.8+
- mpremote (`pip install mpremote`)
- esptool (`pip install esptool`)

---

## 🎯 Vantagens dessa Organização

✅ **Separação clara** de responsabilidades  
✅ **Versionamento independente**  
✅ **Reutilização** - IDE pode ser usado em outros projetos ESP32  
✅ **Backup automático** via Git  
✅ **Colaboração** facilitada  
✅ **Clone rápido** - apenas o que precisa  

---

## 📝 Convenções de Commit

### **Monitor Miner:**
```
feat: adiciona sensor DHT22
fix: corrige erro de memória
refactor: simplifica código WiFi
docs: atualiza README
```

### **IDE ESP:**
```
feat: adiciona upload diff
fix: corrige detecção de porta
perf: melhora velocidade de upload
docs: adiciona guia de uso
```

---

## 🔗 Links Úteis

- [Monitor Miner](https://github.com/caiomaggiore/Monitor-Miner)
- [IDE ESP Cursor](https://github.com/caiomaggiore/IDE-ESP-Cursor)

---

**Criado em:** 12/10/2025  
**Versão:** 2.0

