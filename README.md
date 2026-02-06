# Inbox Cleaner

Scan your Gmail for marketing emails and get all the unsubscribe links in one place. **Windows compatible.**

## Quick Start (15 minutes)

### 1. Install Python

1. Go to https://www.python.org/downloads/
2. Download and run the installer
3. Click "Install Python"
4. When it asks about "App execution aliases", type **y** and press Enter
5. In Windows Settings, click "App execution aliases"
6. Turn ON the toggles for "python.exe" and "python3.exe"
7. Close Settings

### 2. Download and Install

1. Click the green "Code" button at the top of this page
2. Click "Download ZIP"
3. Extract to your Desktop
4. Open the `inbox-cleaner` folder
5. **Double-click `setup.bat`** (installs everything automatically)

### 3. Get Google Credentials

You need to create a `credentials.json` file from Google Cloud Console:

1. Go to https://console.cloud.google.com/
2. Sign in with your Gmail
3. Click "Select a project" at the top → "NEW PROJECT"
4. Project name: `Gmail Tool` → Click "CREATE"
5. Click "APIs & Services" (left sidebar) → "Enable APIs and Services" (blue button)
6. Search for "Gmail API" → Click it → Click "ENABLE"
7. Click "Credentials" (left sidebar) → "CREATE CREDENTIALS" (top) → "OAuth client ID"

**First time OAuth setup:**
8. Click the blue "Get started" button
9. Fill in:
   - App name: `Inbox Cleaner`
   - User support email: (select your email from dropdown)
   - Click "Next"
10. On "Audience" screen: "External" is already selected → Click "Next"
11. On "Contact Information" screen:
    - Email addresses: Type your Gmail address
    - Click "Next"
12. Click "Create" (bottom left)

**Now create the credentials:**
13. You'll see "OAuth configuration created!" message at the bottom
14. Click the "Create OAuth client" button in the middle of the screen
15. Application type: Choose "Desktop app"
16. Name: `Gmail Desktop`
17. Click "CREATE"
18. Click "DOWNLOAD JSON" in the popup
19. Rename the downloaded file to exactly `credentials.json`
20. Move it into your `inbox-cleaner` folder

**Add yourself as a test user:**
21. Go back to https://console.cloud.google.com/
22. Click "APIs & Services" → "OAuth consent screen" (left sidebar)
23. Click "Audience" in the left sidebar (NOT Overview)
24. Scroll down to "Test users" section
25. Click "ADD USERS"
26. Type your Gmail address
27. Click "SAVE"

### 4. Run It

Double-click `run.bat`

First time: Browser opens for Gmail login. Click "Allow".

The tool scans your emails and creates `unsubscribe_list.txt` with all the unsubscribe links.

**IMPORTANT:** 
- Wait for the script to finish completely (it will say "Results saved...")
- Don't open the output files until you see the completion message
- If you have the files open while the script runs, close and reopen them after it finishes
- The script can take 2-5 minutes for 500 emails, longer for more

**Default:** Scans 500 emails. To scan more:
- Edit `run.bat` and change the last line to: `python unsubscriber.py --max-emails 2000`
- Or run from command line: `python unsubscriber.py --max-emails 2000`
- Gmail API allows up to ~10,000 emails per run

---

## What This Does

- Scans promotional and update emails
- Finds unsubscribe links in headers and email bodies
- Creates a text file with all the links
- **Does NOT automatically unsubscribe** (you click the links yourself)
- **Does NOT delete anything** (safe to run)


---

## Files in This Folder

- **`run.bat`** - Double-click to scan your emails
- **`setup.bat`** - Double-click once to install everything
- **`unsubscriber.py`** - The main program (don't edit unless you know Python)
- **`credentials.json`** - Your Google API key (you create this)
- **`token.pickle`** - Auto-created after first login (saves your login)
- **`unsubscribe_list.txt`** - Created after each run (your results)
- **`unsubscribe_list.html`** - Created after each run (clickable links)
- **`requirements.txt`** - List of required Python packages
- **`WINDOWS_SETUP.md`** - Detailed step-by-step instructions
- **`.gitignore`** - Tells git to ignore credentials (important for GitHub)

---

## Advanced Usage

### Scan More Emails (Default is 500)

**Method 1 - Edit the batch file:**
1. Right-click `run.bat`
2. Click "Edit" (or "Edit with Notepad")
3. Change the last line from `python unsubscriber.py` to:
   ```batch
   python unsubscriber.py --max-emails 2000
   ```
4. Save and close
5. Now double-clicking `run.bat` will scan 2000 emails

**Method 2 - Command line:**
```bash
python unsubscriber.py --max-emails 2000
```

Change 2000 to any number (Gmail API allows up to ~10,000 per run)

### Label Emails in Gmail

By default, the tool just creates a list. To also label emails with "Auto-Unsubscribed" in Gmail:
```batch
python unsubscriber.py --live
```

### Command Line Options

```bash
python unsubscriber.py                    # Scan 500 emails, dry run
python unsubscriber.py --live             # Apply labels to Gmail
python unsubscriber.py --max-emails 1000  # Scan more emails
```

### Run Weekly Automatically

**Windows Task Scheduler:**
1. Press Windows key, type "Task Scheduler"
2. Click "Create Basic Task"
3. Name: "Gmail Unsubscriber"
4. Trigger: Weekly, Sunday, 2:00 AM
5. Action: Start a program
6. Program: `C:\Users\YourName\Desktop\inbox-cleaner\run.bat`
7. Finish

---

### What You'll See

The program shows:
- How many emails it scanned (updates every 50 emails)
- How many unsubscribe links it found
- A list of all the marketing emails

**Wait for completion:** The script will print "Results saved..." when done. Don't open output files until you see this message.

Results save to two files:
- `unsubscribe_list.html` - **Open this in your browser for clickable unsubscribe buttons**
- `unsubscribe_list.txt` - Plain text version for reference

**Note:** Only emails with proper unsubscribe headers show up. If you only get a few results from 500 emails, that's normal. Run with `--max-emails 5000` to scan more.

---

## Troubleshooting

**"Python is not recognized"**
- You didn't enable the app execution aliases
- Go to Windows Settings → Apps → Advanced app settings → App execution aliases
- Turn ON "python.exe" and "python3.exe"

**"pip is not recognized" or setup.bat fails**
- Run Command Prompt as Administrator (right-click cmd → "Run as administrator")
- Run `setup.bat` again

**"credentials.json not found"**
- Make sure the file is named exactly `credentials.json` (not .txt or .json.txt)
- Make sure it's in the inbox-cleaner folder
- Turn on file extensions: File Explorer → View → Show → File name extensions

**"Access blocked" or "This app isn't verified"**
- You forgot to add yourself as a test user
- Go to Google Cloud Console → APIs & Services → OAuth consent screen → **Audience** (left sidebar)
- Scroll to "Test users" → Click "ADD USERS" → Add your Gmail → Click "SAVE"
- Or click "Advanced" → "Go to [app name] (unsafe)" when the error appears

**Browser doesn't open / Nothing happens**
- Check if antivirus is blocking it
- Try running Command Prompt as Administrator

**No unsubscribe links found**
- Some emails don't include proper unsubscribe headers
- Try `--max-emails 1000` to scan more

---

## Security & Privacy

- **Your credentials stay on your computer** (credentials.json and token.pickle)
- **Never share these files** or commit them to public GitHub
- The `.gitignore` file prevents accidental uploads
- This tool only **reads** your Gmail (doesn't delete or modify)
- To revoke access: https://myaccount.google.com/permissions

---

## License

MIT - Do whatever you want with this code.

