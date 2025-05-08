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
production_file = 'production_companies.json'

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
        msg.attach(MIMEText(body, 'plain'))

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

# Function to send the story and synopsis
def send_story(new_scripts):
    subject = "My Story and Synopsis"
    body_template = """
    Dear {company_name},

    I hope this email finds you well. Attached is the synopsis and complete story of my work that I believe would be a great fit for your production company.

    Looking forward to your feedback.

    Best regards,
    Mohmad Ashik M A
    +91 99121 40409
    """
    
    # Load production companies
    production_companies = load_production_companies()
    
    # Get list of script attachment files
    attachments = get_script_file_names(scripts_dir)
    print('***************************************************************************************')
    print("scripts : ",attachments)
    print('***************************************************************************************')

    # Send email to new companies and follow-ups for existing ones
    for company_name, email in production_companies.items():
        if new_scripts:
            body = body_template.format(company_name=company_name)
            send_email(company_name, email, subject, body, attachments)
    
    if new_scripts:
        print("New script emails sent to all companies!")

    # Send follow-up email for all companies
    send_follow_up()

# Function to send follow-up email
def send_follow_up():
    subject = "Following Up: Waiting for Your Reply"
    body_template = """
    Dear {company_name},

    I wanted to follow up on the story I sent recently. I would appreciate it if you could review it and provide any feedback or response.

    Best regards,
    Mohmad Ashik M A
    +91 99121 40409
    """
    
    production_companies = load_production_companies()
    
    print('Sending follow-up emails')
    for company_name, email in production_companies.items():
        body = body_template.format(company_name=company_name)
        send_email(company_name, email, subject, body, [])
    print("Follow-up emails sent!")

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

    # Collect new scripts
    new_scripts = input("Enter new script titles separated by commas (or press Enter to skip): ")
    if new_scripts:
        new_scripts_list = [script.strip() for script in new_scripts.split(',')]
        send_story(new_scripts_list)
    else:
        send_follow_up()

if __name__ == "__main__":
    main()
