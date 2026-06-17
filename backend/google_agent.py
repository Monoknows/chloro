import os
import pickle
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
# It needs .modify to allow the batchModify command to mark emails as read!
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/spreadsheets']

def get_google_services():
    """Authenticates the user via browser and returns secure Gmail and Sheets service objects."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    gmail_service = build('gmail', 'v1', credentials=creds)
    sheets_service = build('sheets', 'v4', credentials=creds)
    return gmail_service, sheets_service

def check_job_emails(gmail_service):
    """Scans inbox for direct corporate responses using defensive whitelisting."""
    query = "is:unread (application OR interview OR offer OR job OR status OR confirmation)"
    
    # Block list for any email containing these sender strings
    PLATFORM_BLOCKLIST = ["indeed", "jobstreet", "coursera", "linkedin", "noreply", "alert"]
    
    # Whitelist keywords: Subject MUST contain at least one of these to be read
    SUBJECT_WHITELIST = [
        "received", "confirmation", "confirmed", "interview", "schedule", 
        "invitation", "offer", "update", "status", "application to", 
        "thank you for applying", "next steps"
    ]

    try:
        results = gmail_service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        
        filtered_alerts = []
        if not messages:
            return []

        for msg in messages:
            msg_data = gmail_service.users().messages().get(userId='me', id=msg['id'], format='metadata').execute()
            headers = msg_data.get('payload', {}).get('headers', [])
            
            subject = "No Subject"
            sender = "Unknown Sender"
            for h in headers:
                if h['name'] == 'Subject': subject = h['value']
                if h['name'] == 'From': sender = h['value']
            
            sender_lower = sender.lower()
            subject_lower = subject.lower()
            
            # RULE 1: If it's from a known automated aggregator platform, kill it immediately
            if any(platform in sender_lower for platform in PLATFORM_BLOCKLIST):
                # We still mark it read so it doesn't loop forever, but it's silenced
                gmail_service.users().messages().batchModify(
                    userId='me', 
                    body={'ids': [msg['id']], 'removeLabelIds': ['UNREAD']}
                ).execute()
                continue
                
            # RULE 2: Verify the subject line looks like an actual conversation/confirmation
            is_important = any(keyword in subject_lower for keyword in SUBJECT_WHITELIST)
            
            if is_important:
                # This is a real target email! (e.g., "Application Confirmation for QA Tester")
                filtered_alerts.append({"sender": sender, "subject": subject, "id": msg['id']})
            
            # Always mark as read to clear out the unread queue securely
            gmail_service.users().messages().batchModify(
                userId='me', 
                body={'ids': [msg['id']], 'removeLabelIds': ['UNREAD']}
            ).execute()
            
        return filtered_alerts
    except Exception as e:
        print(f"[GOOGLE AGENT ERROR]: {e}")
        return []

def update_spreadsheet(sheets_service, spreadsheet_id, company, position, status):
    """Appends a new row to your Google Job Tracking Sheet automatically."""
   
    sheet_range = 'Sheet1!A:D' 
    value_input_option = 'USER_ENTERED'
    

    row_values = [[company, position, status, "Updated automatically by Chloro"]]
    body = {'values': row_values}
    
    try:
        sheets_service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, 
            range=sheet_range,
            valueInputOption=value_input_option, 
            body=body
        ).execute()
        return True
    except Exception as e:
        print(f"[SPREADSHEETS ERROR]: {e}")
        return False