# Automatski Deploy na PythonAnywhere iz Cursor-a

## Opcija 1: Git + PythonAnywhere Git Deploy (NAJLAKŠE) ⭐

### Korak 1: Postavi Git repozitorijum

```bash
# Ako još nemaš Git repozitorijum
git init
git add .
git commit -m "Initial commit"
git branch -M main
```

### Korak 2: Push na GitHub

1. Kreiraj repozitorijum na GitHub
2. Poveži lokalni repo:

```bash
git remote add origin https://github.com/tvojusername/tvojrepo.git
git push -u origin main
```

### Korak 3: Poveži PythonAnywhere sa GitHub-om

1. Idi na PythonAnywhere → **Web** tab
2. U sekciji **"Source code"** klikni **"Git"**
3. Unesi:
   - **Repository URL**: `https://github.com/tvojusername/tvojrepo.git`
   - **Branch**: `main`
   - **Source directory**: `/home/toxicraf/mysite/` (ili tvoj path)
4. Klikni **"Pull from Git"**

### Korak 4: Automatski deploy iz Cursor-a

Sada možeš jednostavno:

```bash
# U Cursor terminal-u
git add .
git commit -m "Tvoja poruka"
git push
```

Zatim na PythonAnywhere:
- Idi na **Web** tab
- Klikni **"Reload"** (ili koristi API - vidi Opcija 2)

---

## Opcija 2: Automatski Reload preko API-ja

### Korak 1: Kreiraj API Token

1. Idi na PythonAnywhere → **Account** tab
2. Scroll do **"API Token"** sekcije
3. Klikni **"Create new API token"**
4. Kopiraj token (nećeš ga više moći da vidiš!)

### Korak 2: Postavi Environment Varijable

U Cursor-u, kreiraj `.env` fajl (ili postavi u sistemu):

```bash
# Windows PowerShell
$env:PYTHONANYWHERE_USERNAME="toxicraf"
$env:PYTHONANYWHERE_API_TOKEN="tvoj_token_ovde"
```

Ili kreiraj `.env` fajl u root direktorijumu projekta:

```
PYTHONANYWHERE_USERNAME=toxicraf
PYTHONANYWHERE_API_TOKEN=tvoj_token_ovde
```

**⚠️ VAŽNO**: Dodaj `.env` u `.gitignore` (već je dodato)!

### Korak 3: Koristi Deploy Skriptu

#### Windows (PowerShell):

```powershell
# Instaliraj requests ako nemaš
pip install requests

# Pokreni deploy skriptu
python deploy.py
```

#### Linux/Mac:

```bash
# Instaliraj requests
pip install requests

# Pokreni deploy skriptu
python3 deploy.py
```

Ili koristi bash skriptu:

```bash
chmod +x deploy.sh
./deploy.sh
```

---

## Opcija 3: GitHub Actions (Potpuno Automatski) 🤖

Kreiraj `.github/workflows/deploy.yml`:

```yaml
name: Deploy to PythonAnywhere

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Reload PythonAnywhere
        run: |
          curl -X POST \
            -H "Authorization: Token ${{ secrets.PYTHONANYWHERE_API_TOKEN }}" \
            https://www.pythonanywhere.com/api/v0/user/${{ secrets.PYTHONANYWHERE_USERNAME }}/webapps/${{ secrets.PYTHONANYWHERE_USERNAME }}.pythonanywhere.com/reload/
```

### Postavi GitHub Secrets:

1. Idi na GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Dodaj:
   - `PYTHONANYWHERE_USERNAME` = `toxicraf`
   - `PYTHONANYWHERE_API_TOKEN` = `tvoj_token`

Sada će se aplikacija automatski reload-ovati kad push-uješ na GitHub! 🎉

---

## Preporučeni Workflow

1. **Radi promene u Cursor-u**
2. **Commit i push na GitHub**:
   ```bash
   git add .
   git commit -m "Opis promene"
   git push
   ```
3. **Na PythonAnywhere**:
   - Idi na **Web** tab
   - Klikni **"Pull from Git"** (ako koristiš Git deploy)
   - Ili klikni **"Reload"** (ako si upload-ovao ručno)

---

## Troubleshooting

### Problem: "Git nije instaliran"
**Rešenje**: Instaliraj Git sa https://git-scm.com/

### Problem: "API token ne radi"
**Rešenje**: 
- Proveri da li je token ispravno kopiran
- Kreiraj novi token ako je potrebno
- Proveri da li je username tačan

### Problem: "Reload ne radi"
**Rešenje**:
- Proveri da li je aplikacija aktivna na PythonAnywhere
- Proveri da li su svi fajlovi upload-ovani
- Proveri error log na PythonAnywhere → **Web** tab → **Error log**

---

## Brzi Setup (5 minuta)

1. **Postavi Git** (ako nemaš):
   ```bash
   git init
   git remote add origin https://github.com/tvojusername/tvojrepo.git
   ```

2. **Postavi PythonAnywhere Git Deploy**:
   - Web tab → Source code → Git
   - Unesi GitHub URL

3. **Deploy**:
   ```bash
   git add . && git commit -m "Deploy" && git push
   ```
   - PythonAnywhere → Web tab → Pull from Git → Reload

**Gotovo!** 🎉

