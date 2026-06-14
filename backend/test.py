from brain import ask_chloro
# Import the functions from your google_agent.py file
from google_agent import get_google_services, check_job_emails, update_spreadsheet

# paste your actual spreadsheet ID here to test the writing function
TEST_SPREADSHEET_ID = "1sqI20dH8f9WoM2XpmUNeVB3DjSCotP26XtNy98B0lSw"

print("==================================================")
print("       CHLORO WORKSPACE AGENT: TESTING SUITE       ")
print("==================================================")

try:
    print("\n[STEP 1]: Attempting Google OAuth Connection...")
    print("👉 Note: If this is your first time, a browser window will pop up asking you to sign in.")
    
    gmail_srv, sheets_srv = get_google_services()
    print("✅ Success: Google token initialized and services built successfully!")
    
    # ─── TEST 1: EMAIL SCANNING ───
    print("\n[STEP 2]: Scanning inbox for job-related keywords...")
    found_emails = check_job_emails(gmail_srv)
    print(f"📬 Scan complete. Found {len(found_emails)} unread matching emails.")
    
    for email in found_emails:
        print(f"  -> From: {email['sender']} | Subject: {email['subject']}")

    # ─── TEST 2: SHEET LOGGING ───
    print("\n[STEP 3]: Testing Google Spreadsheet logging entry...")
    if TEST_SPREADSHEET_ID == "YOUR_GOOGLE_SHEET_LONG_ID_STRING":
        print("⚠️ Skipped: Update the TEST_SPREADSHEET_ID variable to test writing to your sheet.")
    else:
        success = update_spreadsheet(
            sheets_srv, 
            TEST_SPREADSHEET_ID, 
            company="Test Corp", 
            position="Cybersecurity Engineer", 
            status="Testing Integration"
        )
        if success:
            print("✅ Success: A test row has been appended to your Google Sheet!")
        else:
            print("❌ Failure: Could not write data to the spreadsheet.")

    # ─── TEST 3: CHLORO BRAIN VERIFICATION ───
    print("\n[STEP 4]: Asking Chloro to evaluate the setup status...")
    report_query = f"I just successfully connected your background framework to Google APIs. I found {len(found_emails)} new job emails. Give me a quick status acknowledgment."
    chloro_response = ask_chloro(report_query)
    print(f"\nCHLORO response: {chloro_response}")

except Exception as global_err:
    print(f"\n❌ CRITICAL SUITE ERROR: {global_err}")
    print("Make sure 'credentials.json' is in the same folder and pip packages are installed.")

print("\n==================================================")
print("               TEST RUN COMPLETE                  ")
print("==================================================")