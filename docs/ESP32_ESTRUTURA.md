# 📂 Estrutura de Pastas no ESP32 com MicroPython

## 🎯 Limitações do MicroPython

### Sistema de Arquivos
O MicroPython no ESP32 usa um **sistema de arquivos simples** (LittleFS ou FAT):
- ✅ **Suporta pastas** (diretórios)
- ⚠️ **Limitações de profundidade** (geralmente 2-3 níveis)
- ⚠️ **Nomes de arquivo limitados** (geralmente 32 caracteres)
- ⚠️ **Case-sensitive** em alguns sistemas

---

## 📋 Estrutura Recomendada

### ✅ Simples e Eficiente (RECOMENDADO)
```
/ (raiz)
├── main.py           # Código principal
├── boot.py           # Inicialização
├── config.py         # Configurações
│
├── hardware/         # Hardware (1 nível)
│   ├── __init__.py
│   ├── relays.py
│   └── sensors.py
│
├── services/         # Serviços (1 nível)
│   ├── __init__.py
│   ├── database.py
│   └── logger.py
│
└── web/              # Web (máx 2 níveis)
    ├── index.html
    ├── style.css
    └── app.js
```

### ⚠️ Aninhamento Profundo (Pode dar problema)
```
/ (raiz)
└── web/
    └── assets/         # Nível 2
        └── css/        # Nível 3 - PODE FALHAR!
            └── main.css
```

---

## 🔧 Como o ESP Manager Funciona Agora

### 1. **Validação Real**
```python
# Antes de criar
directory_exists("hardware")  # Verifica se existe

# Criar
create_directory("hardware")  # Cria

# Validar novamente
directory_exists("hardware")  # ✅ Confirma
```

### 2. **Criação Recursiva**
```python
# Para criar web/css/main.css:
create_directory("web")       # Pai primeiro
create_directory("web/css")   # Depois filho
upload_file("main.css")       # Só então envia arquivo
```

### 3. **Relatório Honesto**
```
📂 Criando estrutura de diretórios...
  📁 hardware... ✅
  📁 services... ✅
  📁 web... ✅
  📁 web/css... ✅
  📁 web/js... ✅
  📁 web/js/components... ❌  # Se falhou, mostra!

⚠️  1 diretório(s) não foram criados:
  ❌ web/js/components

💡 O ESP32 pode não suportar pastas aninhadas neste modo.
   Arquivos nessas pastas podem falhar no upload.

Continuar mesmo assim? [s/N]:
```

---

## 💡 Soluções para Problemas Comuns

### Problema: Pastas muito aninhadas
```
❌ web/assets/images/icons/logo.png
```

**Solução 1:** Simplificar estrutura
```
✅ web/logo.png
```

**Solução 2:** Usar apenas 1 nível
```
✅ web/icon_logo.png
```

### Problema: Pastas duplicadas (web/web/)
```
❌ web/web/js/app.js
```

**Causa:** Estrutura de pastas mal organizada no projeto

**Solução:** Limpar duplicatas
```bash
# Remover pasta web/web/
rm -rf esp32/web/web/
```

---

## 🧪 Teste de Estrutura

### Comando para testar:
```bash
python start.py
# Escolha [6] - Ver Arquivos ESP32
```

### O que será mostrado:
```
📜 Arquivos no ESP32

📂 Raiz (/):
- boot.py
- main.py
- config.py
[hardware]
[services]
[web]

📂 hardware/:
- __init__.py
- relays.py
- sensors.py

📂 services/:
- __init__.py
- database.py
- logger.py

📂 web/:
- index.html
- style.css
- app.js
[css]
[js]
```

---

## 📝 Boas Práticas

### ✅ FAÇA
1. Mantenha estrutura **SIMPLES** (máx 2 níveis)
2. Use nomes **CURTOS** para arquivos
3. Teste upload com **poucos arquivos** primeiro
4. Verifique espaço disponível

### ❌ NÃO FAÇA
1. Pastas com mais de 3 níveis
2. Nomes de arquivo muito longos
3. Caracteres especiais em nomes
4. Upload de arquivos muito grandes (>100KB)

---

## 🔍 Diagnóstico

### Verificar estrutura atual:
```bash
python start.py
# [6] Ver Arquivos ESP32
```

### Verificar se pasta foi criada:
```python
# No REPL ([7])
import os
os.listdir('/')       # Ver raiz
os.listdir('web')     # Ver pasta web
os.stat('web')        # Ver info da pasta
```

### Criar pasta manualmente:
```python
# No REPL ([7])
import os
os.mkdir('web')
os.mkdir('web/css')
```

---

## 📚 Referências

- [MicroPython os module](https://docs.micropython.org/en/latest/library/os.html)
- [ESP32 File System](https://docs.micropython.org/en/latest/esp32/tutorial/filesystem.html)

---

**Última atualização:** 11/10/2025  
**Versão ESP Manager:** 2.2

