import smtplib
import os
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Set up the email account
your_email = "imashikg@gmail.com"
your_password = "jbao usic aibn pkkv"

# Directories and files
scripts_dir = '/home/amohmad/Documents/ashik/scripts'
# production_file = 'info_stage_production_companies.json'
production_file = 'test_emails.json'

# Fetch the script file names (PDFs)
def get_script_file_names(directory):
    return [f for f in os.listdir(directory) if f.endswith('.pdf')]

# Load production companies from the JSON file
def load_production_companies():
    if os.path.exists(production_file):
        with open(production_file, 'r') as file:
            return json.load(file)
    return {}

# Save production companies to the JSON file
def save_production_companies(companies):
    with open(production_file, 'w') as file:
        json.dump(companies, file, indent=4)

# Function to send an email
def send_email(company_name, to_email, subject, body, attachments):
    try:
        print(f"Preparing to send email to {company_name} ({to_email})...")
        
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = your_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Attach the PDF files
        for attachment in attachments:
            with open(attachment, 'rb') as file:
                part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                msg.attach(part)

        # Connect to the SMTP server with a 10-second timeout
        print("Connecting to the SMTP server...")
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)  # Timeout of 10 seconds
        server.starttls()

        # Log in to the server
        print("Logging in to the SMTP server...")
        server.login(your_email, your_password)

        # Send the email
        print(f"Sending email to {company_name} ({to_email})...")
        server.sendmail(your_email, to_email, msg.as_string())
        server.quit()
        
        print(f"Email successfully sent to {company_name} ({to_email})")

    except Exception as e:
        print(f"Error sending email to {company_name}: {e}")

# Function to send an introductory email requesting submission contact details
def send_contact_request_email(company_name, to_email):
    subject = "Script Submission Inquiry – Original Screenplays Ready for Consideration"
    
    # HTML-formatted message
    message = f"""
    <html>
    <body>
        <p>Dear {company_name},</p>

        <p>Greetings.</p>

        <p>My name is <strong>Mohmad Ashik M A</strong>, and I am a screenplay writer and actor with a strong passion for storytelling. 
        I am reaching out to inquire about the appropriate contact or process within your esteemed production house to submit my scripts for your consideration.</p>

        <p>I currently have several original screenplays ready, complete with full script synopses and bounded, scene-to-scene drafts. 
        The stories span across various genres, designed to suit a range of budgets and casting preferences:</p>

        <ul>
            <li><strong>Two Friends</strong> – A sci-fi comedy drama (Low budget; suitable for new or established young actors)</li>
            <li><strong>Force</strong> – An Indian superhero film (Requires VFX budget; ideal for one high-profile actor)</li>
            <li><strong>True Love Never Dies</strong> – A college romantic drama (Low budget; new or young actors)</li>
            <li><strong>60 Minutes</strong> – A time-loop thriller (Low budget; suitable for new or established actors)</li>
            <li><strong>Mistakes</strong> – A road comedy thriller (Low budget; best with established actors)</li>
        </ul>

        <p>It would be a great honor to collaborate with your team and explore the possibility of bringing one or more of these stories to life under your banner.</p>

        <p>Looking forward to your kind guidance on the next steps.</p>

        <p>Warm regards,<br>
        <strong>Mohmad Ashik M A</strong><br>
        Director, Screenwriter, and Actor<br>
        +91 99121 40409<br>
        Hyderabad, Hitech City – 500081</p>
    </body>
    </html>
    """


    
    send_email(company_name, to_email, subject, message, [])


# Main function to run the script
def main():
    # Collect new production company emails
    new_companies = input("Enter new production company names and emails in the format 'Company Name : email' separated by commas (or press Enter to skip): ")
    if new_companies:
        new_companies_list = [company.strip().split(':') for company in new_companies.split(',')]
    
        companies = load_production_companies()

        for name, email in new_companies_list:
            companies[name.strip()] = email.strip()
        
        save_production_companies(companies)
        print('new company details saved successfully')
    # Load production companies
    production_companies = load_production_companies()
    for company_name, general_email in production_companies.items():
        send_contact_request_email(company_name, general_email)
        print(f"Sent request for contact details to the {company_name} for {general_email}.")

if __name__ == "__main__":
    main()
