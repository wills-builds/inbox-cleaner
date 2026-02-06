# Inbox Cleaner - START HERE

## What is this?

A tool that scans your Gmail and finds all the unsubscribe links in one place.

## Windows Setup (15 minutes total)

### 1. Install Python (if you don't have it)

1. Go to https://www.python.org/downloads/
2. Download and run the installer
3. Click "Install Python"
4. When asked about "App execution aliases", type **y** and press Enter
5. In Settings, click "App execution aliases"
6. Turn ON "python.exe" and "python3.exe"
7. Close Settings

### 2. Install the tool

1. Extract this ZIP to your Desktop
2. Open the `inbox-cleaner` folder
3. **Double-click `setup.bat`**
4. Wait for it to install (takes 1-2 minutes)

### 3. Get Google credentials

You need a `credentials.json` file from Google. Open `WINDOWS_SETUP.md` and follow Step 3 (the Gmail setup part).

It's a lot of clicking in Google Cloud Console but I walk you through every single step.

### 4. Run it

Double-click `run.bat`

Your browser will open for Gmail login (first time only). Then it scans your emails and creates `unsubscribe_list.txt`.

## Files in this folder

- `run.bat` - Click this to scan your emails
- `setup.bat` - Click this once to install everything
- `WINDOWS_SETUP.md` - Full detailed instructions
- `README.md` - Technical documentation
- `unsubscriber.py` - The actual program (don't touch)
- `requirements.txt` - List of required packages (don't touch)

## Need help?

1. Open `WINDOWS_SETUP.md` for detailed step-by-step
2. Check the Troubleshooting section at the bottom
3. Make sure you ran `setup.bat` first
4. Make sure your `credentials.json` file is in this folder
