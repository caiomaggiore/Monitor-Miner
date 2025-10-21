# Configuração da Porta ESP32

## 🎯 O que mudou?

Agora **TODAS** as ferramentas leem a porta COM do arquivo `config.py`! Não precisa mais editar 13 arquivos diferentes.

## 📋 Como configurar

### 1️⃣ Descubra a porta da sua ESP32

**Windows:**
```bash
# No Device Manager ou no PowerShell:
Get-WmiObject Win32_SerialPort | Select-Object Name, DeviceID
```
Resultado: `COM3`, `COM5`, `COM6`, etc.

**Linux/Mac:**
```bash
ls /dev/tty*
```
Resultado: `/dev/ttyUSB0`, `/dev/ttyUSB1`, etc.

### 2️⃣ Edite o arquivo `config.py`

Abra o arquivo `config.py` e altere a linha:

```python
ESP32_PORT = "COM5"  # 🔧 ALTERE AQUI PARA SUA PORTA
```

Por exemplo:
- Se sua porta é COM6: `ESP32_PORT = "COM6"`
- Se sua porta é COM3: `ESP32_PORT = "COM3"`
- Linux/Mac: `ESP32_PORT = "/dev/ttyUSB0"`

### 3️⃣ Pronto! Use as ferramentas normalmente

Agora todos os scripts vão usar automaticamente a porta configurada:

```bash
# Testar conexão
python tools/test_esp32_simple.py

# Diagnóstico
python tools/diagnose_esp32.py

# Upload
python tools/upload_esp32.py

# Instalar MicroPython
python tools/install_micropython.py
```

## 🔧 Ferramentas Atualizadas (13 arquivos)

Todos estes arquivos agora leem do `config.py`:

1. ✅ `tools/test_esp32_simple.py`
2. ✅ `tools/diagnose_esp32.py`
3. ✅ `tools/install_micropython.py`
4. ✅ `tools/upload_esp32.py`
5. ✅ `tools/simple_upload.py`
6. ✅ `tools/format_esp32_auto.py`
7. ✅ `tools/format_esp32_force.py`
8. ✅ `tools/upload_file_by_file.py`
9. ✅ `tools/upload_factory_reset.py`
10. ✅ `tools/hard_reset_esp32.py`
11. ✅ `tools/auto_hard_reset.py`
12. ✅ `tools/reinstall_micropython.py`
13. ✅ `tools/esp32_upload.py`

## 🎯 Como funciona?

- **Arquivo criado:** `tools/port_config.py` - Gerencia a leitura da configuração
- **Prioridade de busca:**
  1. `config.py` (ESP32_PORT)
  2. Variável de ambiente `ESP32_PORT`
  3. Padrão: COM5 (Windows) ou /dev/ttyUSB0 (Linux/Mac)

## 💡 Dicas

- Se esquecer de configurar, o sistema usa COM5 por padrão
- Cada ferramenta mostra qual porta está usando quando executa
- Você pode ter múltiplos arquivos de config e trocar entre eles

## 🚀 Exemplo de uso

```bash
# 1. Configure a porta no config.py
ESP32_PORT = "COM6"

# 2. Teste a nova ESP32
python tools/test_esp32_simple.py

# Saída:
# 📌 Usando porta do config.py: COM6
# 🧪 Teste Simples ESP32
# 🔌 Teste 1: Conectar ao ESP32...
# ✅ OK
```

## ❓ Problemas?

Se algo não funcionar:
1. Verifique se a porta está correta no Device Manager
2. Confirme que o arquivo `config.py` existe
3. Verifique se não tem outros programas usando a porta
4. Execute: `python tools/port_config.py` para ver a configuração atual

---

**Pronto!** Agora é só configurar uma vez e usar todas as ferramentas! 🎉

