# GitHub Setup Guide (हिंदी)

Ye guide aapko project ko GitHub pe daalne mein help karegi.

---

## Step 1: GitHub Account Banao

1. Browser mein kholo: https://github.com/signup
2. Email ID daalo
3. Password banado
4. Username choose karo
5. Email verify karo (link aayega email pe)

## Step 2: Naya Repository Banao

1. https://github.com/new  — ye page kholo
2. **Repository name** mein likho: `chess-ai-coach`
3. Description (optional): `Chess AI Coach - Desktop & Web`
4. **Public** selected rakho
5. **Create repository** button dabao

## Step 3: Project ko GitHub pe daalo

Project folder mein `UPDATE.bat` hai. Use **double-click** karo.

Pehli baar mein ye puchhega: `GitHub URL paste karo`

- GitHub ke page se URL copy karo (kuch aisa: `https://github.com/YOUR-NAME/chess-ai-coach.git`)
- UPDATE.bat mein paste karo
- Enter dabao

**Ho gaya!** Project GitHub pe aa gaya.

---

## Future Updates (Jab code change karo)

Sirf **UPDATE.bat** double-click karo. Ye automatically:
1. Saare changes detect karega
2. Commit karega (date/time ke saath)
3. GitHub pe push kar dega

---

## Project Kaise Download Karein Koi Aur?

Koi bhi ye commands use kare:

```bash
git clone https://github.com/YOUR-NAME/chess-ai-coach.git
cd chess-ai-coach
pip install -r requirements.txt
python run.py          # Desktop mode
# ya
python run.py web      # Web mode
```

---

## Problem ho rahi hai?

| Problem | Solution |
|---|---|
| "git not found" | https://git-scm.com/downloads se Git install karo |
| "Push failed" | Internet check karo, ya GitHub login check karo |
| "URL nahi hai" | UPDATE.bat delete karo aur dobara run karo |
