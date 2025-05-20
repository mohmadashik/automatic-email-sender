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
scripts_dir = '/home/amohmad/lab/automatic-email-sender/synopsis/'
production_files = ['valid_tamil_production_companies.json','valid_telugu_production_companies.json','valid_production_companies.json']
# production_files = ['test_emails.json']

# Fetch the script file names (PDFs)
def get_script_file_names(directory):
    # return full list of full paths 
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.pdf')]
    # return [f for f in os.listdir(directory) if f.endswith('.pdf')]

# Load production companies from the JSON file
def load_production_companies():
    production_companies = {}
    for production_file in production_files:
        if os.path.exists(production_file):
            with open(production_file, 'r') as file:
                data = json.load(file)
                for name,email in data.items():
                    # Check if the company name already exists
                    if name not in production_companies:
                        production_companies[name] = email
    return production_companies


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

# Function to send the story and synopsis
def send_story():

    subject = "BRO CODE #0143 - Feature Film Pitch & Synopsis"
    # Load production companies
    production_companies = load_production_companies()
    
    # Get list of script attachment files
    attachments = get_script_file_names(scripts_dir)
    print('***************************************************************************************')
    print("scripts : ",attachments)
    print('***************************************************************************************')

    # Send email to new companies and follow-ups for existing ones
    for company_name, email in production_companies.items():
        body_template = f"""
<html>
  <body style="font-family: Arial, sans-serif; font-size: 16px; color: #333; line-height: 1.6; padding: 20px;">
    <p>Dear <strong>{company_name}</strong>,</p>

    <p>I hope this message finds you well.</p>

    <p>
      I’m excited to share with you the synopsis of a film script titled <br>
      <strong style="color: #d62828;">BRO CODE #0143</strong>.  
    </p>
    <p>
      <strong>Genre:</strong> Comedy, Action, Drama — with a blink of Sci-Fi ✨  
    </p>

    <p>
      This story is <strong>high-concept</strong>, <strong>commercially viable</strong>, and has the potential to evolve into a successful film franchise.
    </p>
    <p>
      The <strong>full bound screenplay is ready</strong> and available upon request. I'd love to explore a collaboration with your team to bring this project to life on screen.
    </p>

    <p style="font-style: italic; font-weight: bold; color: #2a9d8f;">
      This is not just a film — this will become a legacy for those who give it a chance.
    </p>

    <p>I look forward to hearing from you.</p>

    <p>
      Warm regards,<br />
      <strong>Mohmad Ashik M A</strong><br />
      📞 +91 99121 40409
    </p>
  </body>
</html>
        """
        send_email(company_name, email, subject, body_template, attachments)
    
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
    companies = load_production_companies()
    # Collect new scripts
    # new_scripts = input("Enter new script titles separated by commas (or press Enter to skip): ")
    follow_up_or_not = input("Do you want to send follow-up emails? (yes/no): ").strip().lower()
    if follow_up_or_not == 'yes':
        send_follow_up()
    else:
        send_story()

if __name__ == "__main__":
    main()
