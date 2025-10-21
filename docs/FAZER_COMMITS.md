# 📝 Como Fazer Commits e Push

## ✅ Repositórios Já Configurados

Ambos os repositórios já têm:
- ✅ Git inicializado (`.git/`)
- ✅ Remote configurado
- ⚠️ Commits **PENDENTES**

---

## 🚀 Executar Agora

### **Monitor Miner (ESP32):**

```bash
cd esp32
git add .
git commit -m "feat: versao inicial estavel - WiFi AP + Servidor Web + Hello World"
git push -u origin main
cd ..
```

---

### **IDE ESP Cursor:**

```bash
cd IDE-ESP-Cursor
git add .
git commit -m "feat: IDE ESP32 - ferramentas CLI completas para desenvolvimento"
git push -u origin main
cd ..
```

---

## 📋 Checklist

### Monitor Miner
- [ ] `cd esp32`
- [ ] `git add .`
- [ ] `git commit -m "feat: versao inicial..."`
- [ ] `git push -u origin main`
- [ ] Verificar no GitHub

### IDE ESP Cursor
- [ ] `cd IDE-ESP-Cursor`
- [ ] `git add .`
- [ ] `git commit -m "feat: IDE ESP32..."`
- [ ] `git push -u origin main`
- [ ] Verificar no GitHub

---

## 🔍 Verificar Status

### Antes do commit:
```bash
cd esp32
git status
# Deve mostrar: "Untracked files" ou "Changes not staged"
```

### Depois do commit:
```bash
git log --oneline
# Deve mostrar: commit inicial
```

### Depois do push:
```bash
git status
# Deve mostrar: "Your branch is up to date with 'origin/main'"
```

---

## ⚠️ Se Houver Problemas

### "Please tell me who you are"
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

### "Permission denied (publickey)"
```bash
# Verificar se tem SSH key configurada
ssh -T git@github.com

# Se não tiver, usar HTTPS:
git remote set-url origin https://github.com/caiomaggiore/Monitor-Miner.git
```

---

## ✅ Depois do Push

Verifique nos repositórios:
- https://github.com/caiomaggiore/Monitor-Miner
- https://github.com/caiomaggiore/IDE-ESP-Cursor

---

**Execute os comandos acima no terminal PowerShell!**

