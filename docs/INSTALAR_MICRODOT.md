# 📦 Como Instalar Microdot no ESP32

## 🎯 O Problema

O `mip` (gerenciador de pacotes MicroPython) **NÃO tem o Microdot**!

Precisa instalar **manualmente**.

---

## ✅ Solução Automática (Recomendada)

```bash
python tools/download_microdot.py
```

**O que faz:**
1. 📥 Baixa `microdot.py` e `microdot_asyncio.py` do GitHub
2. 📤 Faz upload para ESP32
3. ✅ Verifica se funcionou

---

## 🔧 Solução Manual (Se automático falhar)

### Opção 1: Via Thonny (Mais Fácil)

1. **Baixe os arquivos:**
   - [microdot.py](https://raw.githubusercontent.com/miguelgrinberg/microdot/main/src/microdot/microdot.py)
   - [microdot_asyncio.py](https://raw.githubusercontent.com/miguelgrinberg/microdot/main/src/microdot/microdot_asyncio.py)

2. **No Thonny:**
   - Abra os arquivos baixados
   - `Arquivo → Salvar como... → Dispositivo MicroPython`
   - Salve como `microdot.py` e `microdot_asyncio.py`

3. **Verificar:**
   - No REPL:
   ```python
   >>> import microdot
   >>> import microdot_asyncio
   >>> print("OK!")
   ```

### Opção 2: Via mpremote

```bash
# 1. Baixar arquivos (no seu PC)
curl -o microdot.py https://raw.githubusercontent.com/miguelgrinberg/microdot/main/src/microdot/microdot.py

curl -o microdot_asyncio.py https://raw.githubusercontent.com/miguelgrinberg/microdot/main/src/microdot/microdot_asyncio.py

# 2. Upload para ESP32
python -m mpremote connect COM5 fs cp microdot.py :microdot.py
python -m mpremote connect COM5 fs cp microdot_asyncio.py :microdot_asyncio.py

# 3. Verificar
python -m mpremote connect COM5 exec "import microdot; print('OK')"
```

---

## 📋 Após Instalação

```bash
# 1. Reiniciar ESP32
python start.py
# Escolha [4] - Reiniciar ESP32

# 2. Monitor de Logs
python start.py  
# Escolha [8] - Monitor de Logs

# 3. Deve ver:
# [INFO] === Monitor Miner v2.0 ===
# [INFO] Iniciando servidor HTTP na porta 80...
# (sem erros!)
```

---

## ⚠️ Troubleshooting

### Erro: "No module named 'microdot'"
**Causa:** Arquivo não foi copiado corretamente

**Solução:**
```python
# No REPL, listar arquivos:
>>> import os
>>> os.listdir('/')
['boot.py', 'main.py', 'microdot.py', ...]  # Deve aparecer!
```

### Erro: "No module named 'microdot_asyncio'"
**Causa:** Faltou copiar o arquivo asyncio

**Solução:**
```bash
python tools/download_microdot.py
```

### Erro: Download falha
**Causa:** Sem internet no PC

**Solução:**
- Use Thonny para baixar e copiar manualmente

---

## 🔍 Verificar Instalação

```python
# No REPL:
>>> import microdot
>>> dir(microdot)
['Microdot', 'Response', 'send_file', ...]

>>> from microdot_asyncio import Microdot
>>> print("Async OK!")
```

---

## 📚 Referências

- [Microdot GitHub](https://github.com/miguelgrinberg/microdot)
- [Microdot Docs](https://microdot.readthedocs.io)
- [Issue sobre mip](https://github.com/miguelgrinberg/microdot/issues/67)

---

**Última atualização:** 11/10/2025

