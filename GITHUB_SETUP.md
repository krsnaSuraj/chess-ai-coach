# GitHub Setup Guide

Follow these steps to publish the project on GitHub.

---

## Step 1: Create a GitHub Account

1. Go to https://github.com/signup
2. Enter your email, create a password, and choose a username
3. Verify your email address

## Step 2: Create a New Repository

1. Open https://github.com/new
2. Enter **Repository name**: `chess-ai-coach`
3. Leave it **Public** so others can access it
4. Click **Create repository**

## Step 3: Upload the Project

In the project folder, double-click **`UPDATE.bat`**.

The first time you run it, it will ask for the GitHub URL:
- Copy the URL from your new repository page (looks like `https://github.com/YOUR-NAME/chess-ai-coach.git`)
- Paste it into the script and press Enter

The project will upload automatically.

---

## Future Updates

Whenever you make changes to the code, simply double-click **`UPDATE.bat`**. It will:
1. Detect all changes
2. Create a commit with timestamp
3. Push to GitHub automatically

---

## How Others Download It

Anyone can run:

```bash
git clone https://github.com/YOUR-NAME/chess-ai-coach.git
cd chess-ai-coach
pip install -r requirements.txt
python run.py          # Desktop mode
python run.py web      # Web mode
```

---

## Troubleshooting

| Issue | Solution |
|---|---|
| "git not found" | Install Git from https://git-scm.com/downloads |
| "Push failed" | Check your internet connection and GitHub login |
| Repository exists but script fails | Run `UPDATE.bat` again and enter the correct URL |
