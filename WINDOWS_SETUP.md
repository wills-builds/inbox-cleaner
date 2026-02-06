# QUICK START - Windows

## Never used Python before? Start here.

### 1. Install Python (5 minutes)

1. Go to https://www.python.org/downloads/
2. Click the yellow "Download Python" button
3. Run the installer
4. Click "Install Python"
5. A terminal window opens asking about "App execution aliases"
6. Type **y** and press Enter
7. Windows Settings opens automatically
8. Click "App execution aliases"
9. Find "python.exe" and "python3.exe" in the list
10. Turn both toggles **ON** (blue)
11. Close Settings
12. Close the installer when done

### 2. Download This Tool (2 minutes)

1. Click the green "Code" button at the top of this page
2. Click "Download ZIP"
3. Right-click the downloaded ZIP file
4. Click "Extract All"
5. Extract it to your Desktop

### 3. Set Up Gmail Access (10 minutes)

**You need to tell Google it's okay for this tool to read your Gmail.**

1. Open this link: https://console.cloud.google.com/
2. Sign in with your Gmail
3. Click "Select a project" (very top of page)
4. Click "NEW PROJECT" 
5. Project name: `Gmail Tool`
6. Click "CREATE"
7. Wait 10 seconds for the project to be created
8. Click "APIs & Services" (left sidebar, about halfway down)
9. Click "ENABLE APIS AND SERVICES" (blue button at top)
10. Type `gmail` in the search box
11. Click "Gmail API"
12. Click "ENABLE"
13. Click "Credentials" (left sidebar)
14. Click "CREATE CREDENTIALS" (top button)
15. Click "OAuth client ID"

**First time - Configure OAuth consent screen:**

16. Click the blue "Get started" button
17. On "App Information" screen:
    - App name: Type `Inbox Cleaner`
    - User support email: Click dropdown, select your email
    - Click "Next"
18. On "Audience" screen:
    - "External" is already selected (good!)
    - Click "Next"
19. On "Contact Information" screen:
    - Email addresses: Type your Gmail address
    - Click "Next"
20. Click "Create" (bottom left)

**Now create the actual credentials:**

21. You'll see "OAuth configuration created!" at the bottom of the screen
22. Click the "Create OAuth client" button in the middle of the screen
23. Application type: Select "Desktop app"
24. Name: Type `Gmail Desktop`
25. Click "CREATE"
26. A popup appears - Click "DOWNLOAD JSON"
27. A file downloads with a long weird name
28. **Rename it to exactly:** `credentials.json`
29. **Move it into** the `inbox-cleaner` folder on your Desktop

**Add yourself as a test user (IMPORTANT):**

30. Go back to https://console.cloud.google.com/
31. Click "APIs & Services" in the left sidebar
32. Click "OAuth consent screen"
33. Click "Audience" in the left sidebar (this is where Test users are)
34. Scroll down to the "Test users" section
35. Click "ADD USERS"
36. Type your Gmail address (the one you're using)
37. Click "SAVE"

Without this step, you'll get an "Access blocked" error when trying to run the tool.

### 4. Install Required Packages (2 minutes)

**EASY WAY:**
1. Go to Desktop > inbox-cleaner folder
2. Double-click `setup.bat`
3. Wait for it to finish

**IF THAT DOESN'T WORK:**
1. Press Windows key
2. Type `cmd`
3. **Right-click** on Command Prompt
4. Click "Run as administrator" (important!)
5. Type this and press Enter:
   ```
   cd %USERPROFILE%\Desktop\inbox-cleaner
   ```
6. Type this and press Enter:
   ```
   python -m pip install -r requirements.txt
   ```
7. Wait for it to finish (30 seconds)

### 5. Run It! (1 minute)

**Option A - Easy way:**
1. Go to Desktop > inbox-cleaner folder
2. Double-click `run.bat`

**Option B - Command line way:**
1. In the command prompt (still open from Step 4)
2. Type:
   ```
   python unsubscriber.py
   ```

**First time:** A browser will open asking you to sign in and allow access. Click "Continue" and "Allow".

**Wait time:** The script takes 2-5 minutes for 500 emails. Progress updates show every 50 emails. Wait until you see "Results saved..." before opening the output files.

**Note:** By default, scans 500 emails. To scan more:
- Right-click `run.bat` → Edit → Change last line to: `python unsubscriber.py --max-emails 2000`
- Or use command line: `python unsubscriber.py --max-emails 2000`
- You can scan up to ~10,000 emails per run

### 6. Check Results

**IMPORTANT:** Wait for the script to finish (you'll see "Results saved..." in the terminal)

1. Go to Desktop > inbox-cleaner
2. If you opened the files early, close them and reopen after the script finishes
3. Double-click `unsubscribe_list.html` to open in your browser
4. You'll see all your marketing emails with blue "Unsubscribe" buttons
5. Click the buttons to unsubscribe

**Note:** Only 2-10 results from 500 emails is normal - most emails don't have proper unsubscribe headers. To find more, run: `python unsubscriber.py --max-emails 5000`

There's also a text file (`unsubscribe_list.txt`) with the same info.

---

## Run It Again Later

Just double-click `run.bat` in the inbox-cleaner folder.

---

## Troubleshooting

**"Python is not recognized"**
- You didn't enable the app execution aliases during install
- Fix: Go to Settings → Apps → Advanced app settings → App execution aliases
- Turn ON the toggles for "python.exe" and "python3.exe"

**"pip is not recognized" or setup.bat fails**
- Use `python -m pip` instead of `pip`
- Or run Command Prompt as Administrator:
  1. Press Windows key
  2. Type `cmd`
  3. Right-click "Command Prompt"
  4. Click "Run as administrator"
  5. Then run: `python -m pip install -r requirements.txt`

**"No module named google"**
- Double-click `setup.bat` in the folder
- If that doesn't work, run Command Prompt as Administrator and run:
  ```
  python -m pip install -r requirements.txt
  ```

**"credentials.json not found"**
- Make sure the file is named EXACTLY `credentials.json` (not credentials.json.txt)
- Make sure it's in the inbox-cleaner folder
- In File Explorer, click View > Show > File name extensions (to see the real filename)

**"Access blocked"**
- You didn't add yourself as a test user (Step 30-37 in setup above)
- Fix: Go to https://console.cloud.google.com/ → APIs & Services → OAuth consent screen → **Audience** (left sidebar)
- Scroll to "Test users" → Click "ADD USERS" → Type your Gmail → Click "SAVE"
- Or click "Advanced" → "Go to Inbox Cleaner (unsafe)" when the error appears

**Nothing happens**
- Check if antivirus is blocking it
- Try running command prompt as Administrator (right-click cmd, "Run as administrator")
