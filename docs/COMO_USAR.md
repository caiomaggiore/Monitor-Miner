# 🚀 Como Usar o Monitor Miner

## Início Rápido

### 1️⃣ Configure a Porta COM

Descubra qual porta sua ESP32 está usando:

**Windows:**
- Abra o **Gerenciador de Dispositivos**
- Procure em **Portas (COM e LPT)**
- Anote a porta (ex: COM6, COM7, etc)

**Linux/Mac:**
```bash
ls /dev/tty*
# Procure por /dev/ttyUSB0 ou similar
```

Edite o arquivo `config.py` na raiz do projeto:
```python
ESP32_PORT = "COM6"  # Coloque sua porta aqui
```

### 2️⃣ Inicie o ESP Manager

**Opção 1 (Recomendada):**
```bash
python start.py
```

**Opção 2:**
```bash
python tools/esp_manager.py
```

### 3️⃣ Use o Menu Interativo

```
🔧 ESP32 Manager - Monitor Miner v2.0
================================================
Porta: COM6 | Status: ✅ Conectado
Projeto: C:\...\esp32

📋 OPÇÕES:

  [1] 📤 Upload Completo (esp32/)
  [2] 📁 Upload Seletivo
  [3] 📊 Diagnóstico
  [4] 🔄 Reiniciar ESP32
  [5] 💾 Verificar Espaço
  [6] 📜 Ver Arquivos ESP32
  [7] 🖥️  REPL Interativo
  [8] 🧹 Formatar ESP32
  [9] 🔌 Testar Conexão
  [0] ℹ️  Sobre

  [q] ❌ Sair

Digite sua escolha:
```

---

## 📋 Comandos Disponíveis

### Gerenciamento (Recomendado)
```bash
# Iniciar Manager
python start.py
```

### Testes e Diagnóstico
```bash
# Teste simples de conexão
python tools/test_esp32_simple.py

# Diagnóstico completo
python tools/diagnose_esp32.py
```

### Upload
```bash
# Upload rápido (essencial)
python tools/simple_upload.py

# Upload completo
python tools/upload_esp32.py

# Upload arquivo por arquivo
python tools/upload_file_by_file.py
```

### Formatação e Instalação
```bash
# Formatar automaticamente
python tools/format_esp32_auto.py

# Formatar forçado
python tools/format_esp32_force.py

# Instalar MicroPython
python tools/install_micropython.py

# Reinstalar MicroPython
python tools/reinstall_micropython.py
```

---

## 🎯 Workflows Comuns

### Primeira Instalação
```bash
# 1. Configure config.py
# 2. Teste conexão
python tools/test_esp32_simple.py

# 3. Se necessário, formate
python tools/format_esp32_auto.py

# 4. Faça primeiro upload
python start.py
# Escolha opção [1] - Upload Completo
```

### Desenvolvimento Diário
```bash
# 1. Desenvolva em esp32/
# 2. Faça upload
python start.py
# Escolha [1] para completo ou [2] para seletivo

# 3. Monitore logs
# Escolha [7] - REPL Interativo
```

### Debug
```bash
# 1. Diagnóstico
python tools/diagnose_esp32.py

# 2. Ou use Manager
python start.py
# Escolha [3] - Diagnóstico
```

---

## ⚠️ Problemas Comuns

### ESP32 não conecta
```bash
# 1. Verifique porta no Device Manager
# 2. Feche outros programas (Thonny, Arduino IDE)
# 3. Teste conexão
python tools/test_esp32_simple.py
```

### Erro de upload
```bash
# 1. Verifique espaço
python start.py  # Opção [5]

# 2. Se pouco espaço, formate
python tools/format_esp32_auto.py

# 3. Tente novamente
```

### Filesystem corrompido
```bash
# Formatação forçada
python tools/format_esp32_force.py
```

---

## 💡 Dicas

1. **Use sempre o ESP Manager** (`python start.py`) - é mais fácil!
2. **Upload Seletivo** é útil para testar mudanças pequenas
3. **REPL** é ótimo para ver logs em tempo real
4. **Thonny** é bom para debug rápido, mas use Manager para deploy

---

## 📚 Mais Informações

- **README.md** - Visão geral do projeto
- **GUIA_RAPIDO.md** - Guia rápido
- **CONFIGURAR_PORTA.md** - Detalhes sobre configuração de porta

---

**Pronto para começar? Execute:**
```bash
python start.py
```

