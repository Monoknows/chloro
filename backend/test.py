from google_agent import get_google_services, check_job_emails
from ui_linker import set_chloro_ui_state

def run_chloro_email_sync():
    # Initialize connection
    gmail_svc, sheets_svc = get_google_services()
    
    # 1. Trigger thinking state while checking API
    set_chloro_ui_state("thinking")
    
    # Run the inbox scan
    job_alerts = check_job_emails(gmail_svc)
    total_emails = len(job_alerts)
    
    # 2. Trigger answering state to deliver the payload text
    set_chloro_ui_state("answering")
    
    print("\n==================================================")
    print(f"🤖 [CHLORO]: Sir, I have detected {total_emails} new job application emails.")
    print("==================================================\n")
    
    # Return back to standby listening mode
    set_chloro_ui_state("listening")

if __name__ == "__main__":
    run_chloro_email_sync()