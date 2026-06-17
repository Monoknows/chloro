import os
import pickle
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Required Permissions: modifying allows marking emails read, spreadsheets allows tracking logging.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/spreadsheets']

def get_google_services():
    """Authenticates the user via browser and returns secure Gmail and Sheets service objects."""
    creds = None
    token_path = os.path.join(os.path.dirname(__file__), 'token.pickle')
    creds_path = os.path.join(os.path.dirname(__file__), 'credentials.json')
    
    # Check if access tokens are already available cached locally
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
            
    # If there are no valid credentials available, execute OAuth2 handshake loop.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for subsequent execution sessions
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    gmail_service = build('gmail', 'v1', credentials=creds)
    sheets_service = build('sheets', 'v4', credentials=creds)
    return gmail_service, sheets_service

def check_job_emails(gmail_service):
    """Scans inbox for direct corporate responses using defensive whitelisting."""
    query = "is:unread (application OR interview OR offer OR job OR status OR confirmation)"
    
    # Block list targeting known automated aggregator and automated distribution pipelines
    PLATFORM_BLOCKLIST = [
        "indeed", "jobstreet", "coursera", "linkedin", "glassdoor", "geeksforgeeks",
        "noreply", "no-reply", "alert", "info@", "customercare", "marketing", "newsletter"
    ]
    
    # Whitelist keywords: Subject line MUST contain at least one of these to bypass the defensive layer
    SUBJECT_WHITELIST = [
        "received", "confirmation", "confirmed", "interview", "schedule", 
        "invitation", "offer", "update", "status", "application to", 
        "thank you for applying", "next steps"
    ]
    
    # Strict secondary trap: If any of these are found, it is explicitly classified as promotional noise
    PROMO_TRAP = ["%", "off", "refund", "promo", "discount", "cologne", "fragrance", "ends tonight", "cheat sheet"]

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
            
            # --- CRITICAL PROTECTION FILTER ---
            # Rule A: If it matches automated platform handles, kill it immediately.
            is_spam_sender = any(platform in sender_lower for platform in PLATFORM_BLOCKLIST)
            
            # Rule B: If it contains promotional clickbait bait phrases, kill it immediately.
            is_promo_spam = any(spam_word in subject_lower for spam_word in PROMO_TRAP)
            
            if is_spam_sender or is_promo_spam:
                # Silently clear it out from your unread pile so it doesn't break loop state focus
                gmail_service.users().messages().batchModify(
                    userId='me', 
                    body={'ids': [msg['id']], 'removeLabelIds': ['UNREAD']}
                ).execute()
                continue
                
            # --- VERIFICATION PASSTHROUGH ---
            # Verify the email is an actual human response or formal application receipt confirmation
            is_important = any(keyword in subject_lower for keyword in SUBJECT_WHITELIST)
            
            if is_important:
                # Verified corporate application record
                filtered_alerts.append({"sender": sender, "subject": subject, "id": msg['id']})
            
            # Always mark processed emails as read to prevent infinite analysis cycles
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
    sheet_range = 'Sheet1!A:G'  # Updated to match your tracking row limit configuration range
    value_input_option = 'USER_ENTERED'
    
    # Formats row matching your primary sheet arrangement index array
    row_values = [[company, "", "", status, "", "", position]]
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