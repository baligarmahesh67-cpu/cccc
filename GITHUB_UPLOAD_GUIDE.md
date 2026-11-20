# Upload / Update the Project on GitHub (Windows)

This project is already connected to:

```text
https://github.com/baligarmahesh67-cpu/cccc.git
```

From the project folder:

```powershell
git status
git add .
git diff --cached --check
git commit -m "Update and verify crop recommendation application"
git push origin main
```

If Git says `remote origin already exists` and the URL is wrong:

```powershell
git remote set-url origin https://github.com/baligarmahesh67-cpu/cccc.git
git push origin main
```

Use GitHub CLI authentication for Git operations:

```powershell
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git --hostname github.com
gh auth status
gh api user --jq .login
```

The expected account is `baligarmahesh67-cpu`. Never paste a password or
personal access token into source code, documentation or a chat message.
