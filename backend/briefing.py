import os 
import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import pickle

SPREADSHEET_ID = "1sqI20dH8f9WoM2XpmUNeVB3DjSCotP26XtNy98B0lSw"
RANGE_NAME = "Sheet1!A:G"

def get_google_services():
    token_path = os.path.join(os.path.dirname(__file__), 'token.pickle')
    if os.path.exists(token_path):
       with open(token_path, 'rb') as token:
              creds = pickle.load(token)
        return build('sheets', 'v4', credentials=creds)
    else:
        raise Exception("Google credentials not found. Please authenticate first.") 
        return None

def generate_startup_briefing():
    service = get_google_services()
    if not service:
        return "Unable to access Google Sheets. Please check your credentials."

    try:
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        rows = result.get('values', [])

        if not rows:
            return "No job applications found in your tracking sheet."
        
        print("Initializing briefing based on your job application tracking sheet...")

        interviewing_companies = []
        pending_follow_ups = 0

        for row in rows[1:]:  # Skip header row
            if len(row) < 4:
                continue  # Skip rows that don't have enough data

            company = row[0]
            status = row[3]
            job_title = row[6] if len(row) > 6 else "Position"

            if status.lower() == "interviewing":
                interviewing_companies.append(f"{job_title} at {company}")
            elif status.lower() == "pending follow-up":
                pending_follow_ups += 1

        briefing = f"\n==================================================\n"
        briefing += f" SYSTEM ONLINE — GOOD DAY, SIR\n"
        briefing += f"==================================================\n\n"

        if interviewing_companies:
            briefing += f"📌 INTERVIEWING WITH:\n"
            for interview in interviewing_companies:
                briefing += f"   - You have an active interviewing track for: {interview}.\n"
        else:
            briefing += f"📌 INTERVIEWING WITH:\n   - No active interviews at the moment. Keep applying!\n"

        if pending_follow_ups > 0:
            briefing += f"\n📊 Workspace Analytics:\n"
            briefing += f"  - There are currently {pending_follow_ups} applications pending an initial response.\n"
            briefing += f"  - Ready to generate automated follow-up drafts whenever you command.\n"      
        print(briefing)

    except Exception as e:
        print(f"[BRIEFING ERROR]: {e}")

if __name__ == "__main__":
    generate_startup_briefing()