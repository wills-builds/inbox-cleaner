#!/usr/bin/env python3
"""
Inbox Cleaner - Automatically unsubscribe from marketing emails
"""

import os
import re
import base64
import pickle
from typing import List, Dict, Optional
from pathlib import Path
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailUnsubscriber:
    def __init__(self, credentials_path: str = 'credentials.json'):
        self.credentials_path = credentials_path
        self.token_path = 'token.pickle'
        self.service = None
        self.stats = {
            'emails_scanned': 0,
            'unsubscribe_links_found': 0,
            'unsubscribe_emails_found': 0,
            'actions_taken': 0,
            'errors': 0
        }

    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('gmail', 'v1', credentials=creds)
        print("✓ Authenticated with Gmail")

    def find_unsubscribe_info(self, headers: List[Dict], body: str) -> Optional[Dict]:
        """Extract unsubscribe URL or email from message"""
        unsubscribe_info = {}
        
        # Check List-Unsubscribe header
        for header in headers:
            if header['name'].lower() == 'list-unsubscribe':
                value = header['value']
                
                # Extract mailto
                mailto_match = re.search(r'<mailto:([^>]+)>', value)
                if mailto_match:
                    unsubscribe_info['email'] = mailto_match.group(1)
                
                # Extract URL
                url_match = re.search(r'<(https?://[^>]+)>', value)
                if url_match:
                    unsubscribe_info['url'] = url_match.group(1)
        
        # Fallback: search body for unsubscribe links
        if not unsubscribe_info and body:
            url_patterns = [
                r'https?://[^\s<>"]+unsubscribe[^\s<>"]*',
                r'https?://[^\s<>"]+/optout[^\s<>"]*',
                r'https?://[^\s<>"]+/opt-out[^\s<>"]*',
            ]
            for pattern in url_patterns:
                match = re.search(pattern, body, re.IGNORECASE)
                if match:
                    unsubscribe_info['url'] = match.group(0)
                    break
        
        return unsubscribe_info if unsubscribe_info else None

    def get_message_body(self, payload: Dict) -> str:
        """Extract text body from message payload"""
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain' or part['mimeType'] == 'text/html':
                    if 'data' in part['body']:
                        body += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
        elif 'body' in payload and 'data' in payload['body']:
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
        
        return body

    def scan_emails(self, query: str = 'category:promotions OR category:updates', max_results: int = 500):
        """Scan emails for unsubscribe information"""
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                print("No messages found.")
                return []
            
            print(f"\nFound {len(messages)} emails to scan")
            
            unsubscribe_candidates = []
            
            for i, message in enumerate(messages, 1):
                try:
                    msg = self.service.users().messages().get(
                        userId='me',
                        id=message['id'],
                        format='full'
                    ).execute()
                    
                    headers = msg['payload']['headers']
                    body = self.get_message_body(msg['payload'])
                    
                    # Get sender
                    sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown')
                    subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No subject')
                    
                    # Find unsubscribe info
                    unsubscribe_info = self.find_unsubscribe_info(headers, body)
                    
                    if unsubscribe_info:
                        candidate = {
                            'message_id': message['id'],
                            'sender': sender,
                            'subject': subject,
                            'unsubscribe_info': unsubscribe_info
                        }
                        unsubscribe_candidates.append(candidate)
                        
                        if 'email' in unsubscribe_info:
                            self.stats['unsubscribe_emails_found'] += 1
                        if 'url' in unsubscribe_info:
                            self.stats['unsubscribe_links_found'] += 1
                    
                    self.stats['emails_scanned'] += 1
                    
                    if i % 50 == 0:
                        print(f"  Scanned {i}/{len(messages)}...")
                
                except Exception as e:
                    print(f"Error processing message: {e}")
                    self.stats['errors'] += 1
            
            return unsubscribe_candidates
        
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []

    def create_label(self, label_name: str = 'Auto-Unsubscribed') -> str:
        """Create a label for tracking unsubscribed emails"""
        try:
            # Check if label exists
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            
            for label in labels:
                if label['name'] == label_name:
                    return label['id']
            
            # Create new label
            label_object = {
                'name': label_name,
                'labelListVisibility': 'labelShow',
                'messageListVisibility': 'show'
            }
            
            created_label = self.service.users().labels().create(
                userId='me',
                body=label_object
            ).execute()
            
            return created_label['id']
        
        except HttpError as error:
            print(f'Error creating label: {error}')
            return None

    def label_email(self, message_id: str, label_id: str):
        """Add label to email"""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'addLabelIds': [label_id]}
            ).execute()
        except HttpError as error:
            print(f'Error labeling message: {error}')

    def run(self, dry_run: bool = True, auto_label: bool = True):
        """Run the unsubscriber"""
        print("\n" + "="*60)
        print("Inbox Cleaner")
        print("="*60)
        
        if dry_run:
            print("\n⚠️  DRY RUN MODE - No actions will be taken")
        
        self.authenticate()
        
        print("\nScanning emails...")
        candidates = self.scan_emails()
        
        print(f"\n{'='*60}")
        print("SCAN RESULTS")
        print(f"{'='*60}")
        print(f"Emails scanned: {self.stats['emails_scanned']}")
        print(f"Unsubscribe links found: {self.stats['unsubscribe_links_found']}")
        print(f"Unsubscribe emails found: {self.stats['unsubscribe_emails_found']}")
        print(f"Total candidates: {len(candidates)}")
        
        if candidates:
            print(f"\n{'='*60}")
            print("UNSUBSCRIBE CANDIDATES")
            print(f"{'='*60}\n")
            
            # Create label if enabled
            label_id = None
            if auto_label and not dry_run:
                label_id = self.create_label()
            
            for i, candidate in enumerate(candidates, 1):
                print(f"{i}. {candidate['sender'][:50]}")
                print(f"   Subject: {candidate['subject'][:60]}")
                
                if 'url' in candidate['unsubscribe_info']:
                    print(f"   Unsubscribe URL: {candidate['unsubscribe_info']['url'][:80]}")
                
                if 'email' in candidate['unsubscribe_info']:
                    print(f"   Unsubscribe Email: {candidate['unsubscribe_info']['email']}")
                
                if not dry_run and label_id:
                    self.label_email(candidate['message_id'], label_id)
                
                print()
            
            # Save results to file
            self.save_results(candidates)
            
            print(f"\n✓ Results saved to unsubscribe_list.txt and unsubscribe_list.html")
            print("\nNext steps:")
            print("1. Open unsubscribe_list.html in your browser for clickable links")
            print("2. Click the unsubscribe buttons")
            print("3. Or use unsubscribe_list.txt for reference")
        
        print(f"\n{'='*60}\n")


    def save_results(self, candidates: List[Dict]):
        """Save unsubscribe candidates to file"""
        # Save as text file
        try:
            with open('unsubscribe_list.txt', 'w', encoding='utf-8') as f:
                f.write("Gmail Unsubscribe List\n")
                f.write("="*60 + "\n\n")
                
                for i, candidate in enumerate(candidates, 1):
                    f.write(f"{i}. {candidate['sender']}\n")
                    f.write(f"   Subject: {candidate['subject']}\n")
                    
                    if 'url' in candidate['unsubscribe_info']:
                        f.write(f"   Unsubscribe URL: {candidate['unsubscribe_info']['url']}\n")
                    
                    if 'email' in candidate['unsubscribe_info']:
                        f.write(f"   Unsubscribe Email: {candidate['unsubscribe_info']['email']}\n")
                    
                    f.write("\n")
            print("✓ Text file created successfully")
        except Exception as e:
            print(f"Error creating text file: {e}")
        
        # Save as HTML file with clickable links
        try:
            with open('unsubscribe_list.html', 'w', encoding='utf-8') as f:
                f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Gmail Unsubscribe List</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #fff; }
        h1 { color: #333; }
        .email { margin-bottom: 20px; padding: 15px; background: #f5f5f5; border-left: 4px solid #4285f4; }
        .sender { font-weight: bold; color: #1a73e8; font-size: 14px; }
        .subject { color: #666; font-style: italic; margin-top: 5px; }
        .unsubscribe { margin-top: 8px; }
        a { color: #1a73e8; text-decoration: none; font-weight: bold; }
        a:hover { text-decoration: underline; }
        .unsubscribe-btn { 
            display: inline-block; 
            padding: 8px 16px; 
            background: #1a73e8; 
            color: white; 
            border-radius: 4px; 
            margin-top: 8px;
        }
        .unsubscribe-btn:hover { background: #1557b0; }
    </style>
</head>
<body>
    <h1>Gmail Unsubscribe List</h1>
    <p>Found """ + str(len(candidates)) + """ emails with unsubscribe links</p>
""")
                
                for i, candidate in enumerate(candidates, 1):
                    sender = candidate["sender"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    subject = candidate["subject"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    
                    f.write(f'<div class="email">\n')
                    f.write(f'<div class="sender">{i}. {sender}</div>\n')
                    f.write(f'<div class="subject">Subject: {subject}</div>\n')
                    
                    if 'url' in candidate['unsubscribe_info']:
                        url = candidate['unsubscribe_info']['url']
                        f.write(f'<div class="unsubscribe"><a href="{url}" target="_blank" class="unsubscribe-btn">Unsubscribe</a></div>\n')
                    
                    if 'email' in candidate['unsubscribe_info']:
                        email = candidate['unsubscribe_info']['email']
                        f.write(f'<div class="unsubscribe">Email: <a href="mailto:{email}">{email}</a></div>\n')
                    
                    f.write('</div>\n')
                
                f.write("""
</body>
</html>
""")
            print("✓ HTML file created successfully")
        except Exception as e:
            print(f"Error creating HTML file: {e}")
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Inbox Cleaner')
    parser.add_argument('--live', action='store_true', help='Run in live mode (apply labels)')
    parser.add_argument('--credentials', default='credentials.json', help='Path to credentials.json')
    parser.add_argument('--max-emails', type=int, default=500, help='Maximum emails to scan')
    
    args = parser.parse_args()
    
    unsubscriber = GmailUnsubscriber(credentials_path=args.credentials)
    unsubscriber.run(dry_run=not args.live)


if __name__ == '__main__':
    main()
