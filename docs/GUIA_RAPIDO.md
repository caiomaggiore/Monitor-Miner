# 🚀 GUIA RÁPIDO - Monitor Miner v2.0

## ⚡ Início Rápido (5 minutos)

### 1. Configurar WiFi

```bash
# Criar arquivo de configuração
cp config.example.py config.py

# Editar (use seu editor preferido)
notepad config.py
```

Altere:
```python
WIFI_SSID = "SuaRedeWiFi"
WIFI_PASSWORD = "SuaSenha123"
```

### 2. Upload para ESP32

**Opção A - Pymakr (Recomendado):**
```
1. Abrir Cursor
2. Pressionar Ctrl+Shift+P
3. "Pymakr: Connect"
4. Selecionar porta COM
5. "Pymakr: Upload Project"
```

**Opção B - mpremote:**
```bash
python -m mpremote connect COM3 fs cp -r . :
```

### 3. Acessar

1. Monitor serial mostrará IP
2. Abrir navegador: `http://192.168.x.x`
3. Pronto! 🎉

---

## 📊 Recursos Principais

### Dashboard
- Temperatura (2 sensores)
- Umidade (2 sensores)  
- Corrente (4 canais)
- Controle de 4 relés
- Status de rede e sistema

### API REST

```bash
# Sensores
curl http://192.168.x.x/api/sensors

# Controlar relé
curl -X POST http://192.168.x.x/api/relays/0 \
  -H "Content-Type: application/json" \
  -d '{"action":"toggle"}'

# Status
curl http://192.168.x.x/api/system/status
```

---

## 🔧 Pinout ESP32

```
DHT22  → GPIO 23
DHT11  → GPIO 22
Relé 1 → GPIO 25
Relé 2 → GPIO 26
Relé 3 → GPIO 32
Relé 4 → GPIO 27
ADC 1  → GPIO 34
ADC 2  → GPIO 35
ADC 3  → GPIO 36
ADC 4  → GPIO 39
```

---

## 🐛 Problemas Comuns

### Não conecta WiFi
- Verificar SSID/senha
- WiFi 2.4GHz (não 5GHz)
- Rebootar ESP32

### Interface não carrega
- Verificar IP no serial
- ESP32 e PC mesma rede
- Testar: `ping IP_DO_ESP32`

### Sensores "--"
- Verificar conexões
- Alimentação correta
- Pinos GPIO corretos

---

## 📝 Arquivos Importantes

| Arquivo | Descrição |
|---------|-----------|
| `main.py` | Backend API |
| `boot.py` | Inicialização |
| `web/index.html` | Frontend |
| `config.py` | Configurações |
| `data/config.json` | Config sistema |

---

## 🎯 Próximos Passos

1. ✅ Testar sensores
2. ✅ Testar relés
3. ⏳ Configurar automação
4. ⏳ Customizar interface
5. ⏳ Adicionar novos sensores

---

## 💡 Dicas

- **Performance**: Ajuste intervalo de leitura em `config.py`
- **Logs**: Ver em `data/logs.json`
- **Debug**: Monitor serial mostra todos os logs
- **Backup**: Salve `data/config.json` regularmente

---

## 📞 Ajuda

- README.md - Documentação completa
- Monitor serial - Logs em tempo real
- `/api/system/logs` - Logs via API

---

**Monitor Miner v2.0 | ESP32 + MicroPython | 2025**

