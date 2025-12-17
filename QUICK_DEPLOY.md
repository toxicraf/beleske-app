# 🚀 Brzi Deploy na PythonAnywhere

## Prvo: Postavi Git na PythonAnywhere

1. Idi na PythonAnywhere → **Consoles** → **Bash**
2. Pokreni:
   ```bash
   cd /home/toxicraf/mysite
   git init
   git remote add origin https://github.com/toxicraf/beleske-app.git
   git fetch
   git reset --hard origin/main
   ```

## Korišćenje Deploy Skripte

### Opcija 1: Sa Environment Varijablama (Preporučeno)

Postavi u PowerShell-u:

```powershell
$env:PYTHONANYWHERE_USERNAME="toxicraf"
$env:PYTHONANYWHERE_API_TOKEN="tvoj_token_ovde"
```

Zatim pokreni:

```bash
python deploy.py
```

### Opcija 2: Interaktivno

Jednostavno pokreni:

```bash
python deploy.py
```

Skripta će te pitati za username i token.

## Kako dobiti API Token?

1. Idi na PythonAnywhere → **Account** tab
2. Scroll do **"API Token"** sekcije
3. Klikni **"Create new API token"**
4. Kopiraj token

## Šta skripta radi?

1. ✅ Proverava Git status
2. ✅ Commit-uje promene (ako postoje)
3. ✅ Push-uje na GitHub
4. ✅ Reload-uje aplikaciju na PythonAnywhere
5. 💡 Daje instrukcije za git pull na PythonAnywhere

## Nakon deploy-a

Na PythonAnywhere:
1. **Consoles** → **Bash**
2. Pokreni: `cd /home/toxicraf/mysite && git pull origin main`
3. **Web** tab → **Reload**

---

**Gotovo!** 🎉

