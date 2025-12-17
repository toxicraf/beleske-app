# Kako da objaviš aplikaciju na internetu

## Opcija 1: Render.com (NAJLAKŠE - Preporučeno) ⭐

### Koraci:

1. **Kreiraj GitHub nalog** (ako ga nemaš):
   - Idi na https://github.com
   - Registruj se i kreiraj novi repozitorijum
   - Upload sve fajlove projekta

2. **Kreiraj Render nalog**:
   - Idi na https://render.com
   - Registruj se sa GitHub nalogom (besplatno)

3. **Deploy aplikacije**:
   - Klikni "New +" → "Web Service"
   - Poveži GitHub repozitorijum
   - Render će automatski detektovati Flask aplikaciju
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - Klikni "Create Web Service"

4. **Dodaj Environment Variable**:
   - U Settings → Environment Variables
   - Dodaj: `SECRET_KEY` = (bilo koji random string)

5. **Gotovo!** 
   - Render će dati URL tipa: `https://tvoja-aplikacija.onrender.com`

---

## Opcija 2: PythonAnywhere (Alternativa)

### Koraci:

1. **Registruj se**:
   - Idi na https://www.pythonanywhere.com
   - Kreiraj besplatni nalog (Beginner plan)

2. **Upload fajlova**:
   - Idi na "Files" tab
   - Upload sve fajlove projekta (app.py, templates/, requirements.txt)

3. **Kreiraj Web App**:
   - Idi na "Web" tab
   - Klikni "Add a new web app"
   - Izaberi Flask i Python verziju
   - Unesi path do app.py: `/home/tvojusername/mysite/app.py`

4. **Instaliraj zavisnosti**:
   - Idi na "Consoles" → "Bash"
   - Pokreni: `pip3.10 install --user -r requirements.txt`

5. **Reload aplikacije**:
   - Idi na "Web" tab → "Reload"

---

## Opcija 3: Railway (Moderan)

### Koraci:

1. **Registruj se**:
   - Idi na https://railway.app
   - Registruj se sa GitHub nalogom

2. **Deploy**:
   - Klikni "New Project" → "Deploy from GitHub repo"
   - Izaberi repozitorijum
   - Railway automatski detektuje Flask i deploy-uje

---

## Važne napomene:

⚠️ **SQLite baza**: SQLite baza će se resetovati pri svakom redeploy-u na većini platformi. Za produkciju, razmotri PostgreSQL.

⚠️ **Secret Key**: Uvek koristi environment varijable za secret key u produkciji!

✅ **Besplatno**: Sve tri opcije imaju besplatne planove za testiranje.

---

## Najbrži način (Render.com):

1. Upload kod na GitHub
2. Registruj se na Render.com
3. Poveži GitHub repo
4. Klikni Deploy
5. Gotovo! 🎉

