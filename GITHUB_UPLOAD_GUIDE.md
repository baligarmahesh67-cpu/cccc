# Upload this project to GitHub (Windows)

1. Download and extract `basic_crop_recommendation.zip`.
2. Open the extracted `basic_crop_recommendation` folder.
3. Open PowerShell in that folder.
4. Run the following commands.

```powershell
git init
git branch -M main
git add .
git commit -m "Add Basic Crop Recommendation System"
git remote add origin https://github.com/baligarmahesh67-cpu/cccc.git
git push -u origin main
```

If Git says `remote origin already exists`, run this instead of `git remote add origin`:

```powershell
git remote set-url origin https://github.com/baligarmahesh67-cpu/cccc.git
git push -u origin main
```

GitHub may open a browser sign-in flow. Do not paste passwords or personal access tokens into chats.
