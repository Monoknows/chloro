import os
import sys
import pickle
from googleapiclient.discovery import build

# Ensure Python can find sibling files in the backend directory securely
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import the UI controller module and your updated whitelisted Gmail scanner function
from ui_linker import set_chloro_ui_state
from google_agent import check_job_emails 

SPREADSHEET_ID = "1sqI20dH8f9WoM2XpmUNeVB3DjSCotP26XtNy98B0lSw"
RANGE_NAME = "Sheet1!A:G"

def get_google_services():
    """Authenticates using your token and builds both Gmail and Sheets service engines."""
    token_path = os.path.join(os.path.dirname(__file__), 'token.pickle')
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
        
        # Build both required services using your token credentials
        gmail_service = build('gmail', 'v1', credentials=creds)
        sheets_service = build('sheets', 'v4', credentials=creds)
        return gmail_service, sheets_service
    else:
        raise Exception("Google credentials not found. Please authenticate first.")

def generate_startup_briefing():
    print("\n[STARTUP]: Initializing secure connections to Google Cloud Platforms...")
    
    # 1. Shift UI instantly to Blue (Thinking) while contacting API endpoints
    set_chloro_ui_state("thinking")
    
    try:
        gmail_service, sheets_service = get_google_services()
    except Exception as e:
        print(f"[AUTH ERROR]: {e}")
        set_chloro_ui_state("listening")
        return

    # ---- TRACK 1: GMAIL INBOX INTELLIGENCE ----
    print("🧠 [CHLORO]: Syncing inbox payloads and filtering out automated job alerts...")
    direct_responses = check_job_emails(gmail_service)
    total_emails = len(direct_responses)

    # ---- TRACK 2: GOOGLE SHEETS WORKSPACE ANALYTICS ----
    print("🧠 [CHLORO]: Processing local application metrics from tracking matrix...")
    interviewing_companies = []
    pending_follow_ups = 0

    try:
        sheet = sheets_service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        rows = result.get('values', [])

        if rows:
            for row in rows[1:]:  # Skip headers
                if len(row) < 4:
                    continue

                company = row[0]
                status = row[3]
                job_title = row[6] if len(row) > 6 else "Position"

                if status.lower() == "interviewing":
                    interviewing_companies.append(f"{job_title} at {company}")
                elif status.lower() == "pending follow-up":
                    pending_follow_ups += 1
    except Exception as e:
        print(f"[SHEETS ERROR]: Could not pull matrix data. {e}")

    # ---- TRACK 3: CHOREOGRAPHED SYSTEM BRIEFING DELIVERY ----
    # 2. Shift UI cleanly to Purple (Answering) while compiling the final terminal report
    set_chloro_ui_state("answering")

    print("\n==================================================")
    print(" SYSTEM ONLINE — GOOD DAY, SIR")
    print("==================================================")

    # Output Email Updates First (Using Whitelist Filters)
    print(f"📬 INCOMING CORRESPONDENCE:")
    if total_emails > 0:
        print(f"   - Sir, I have isolated {total_emails} verified action item updates from recruiters:")
        for item in direct_responses:
            print(f"     🔹 From: {item['sender']}\n        Subject: {item['subject']}")
        print("\n🗣️ [CHLORO]: 'Sir, direct communications detected. Shall I read the details out loud?'")
    else:
        print(f"   - Stream isolated. Zero actionable company responses detected on this cycle.")

    # Output your Sheet Analytics
    print(f"\n📌 INTERVIEWING WITH:")
    if interviewing_companies:
        for interview in interviewing_companies:
            print(f"   - Active tracking sequence active: {interview}.")
    else:
        print(f"   - No active interview tracking profiles logged right now.")

    print(f"\n📊 WORKSPACE ANALYTICS:")
    print(f"   - There are currently {pending_follow_ups} applications pending a response matrix update.")
    print(f"   - Automated follow-up pipeline scripts stand prepared for deployment.")
    print("==================================================\n")

    # 3. Return UI safely back to Cyan (Listening/Standby) to accept user voice inputs
    set_chloro_ui_state("listening")

if __name__ == "__main__":
    generate_startup_briefing()