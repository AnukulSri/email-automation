import streamlit as st
import smtplib
from email.message import EmailMessage
import re

# Function to sanitize input text (remove non-ASCII characters and non-printable characters)
def sanitize_input(text):
    # Replace non-breaking spaces with regular spaces and remove non-ASCII characters
    text = text.replace("\xa0", " ")  # Replace non-breaking spaces
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
    text = re.sub(r'[\r\n]+', ' ', text)  # Replace line breaks with a space
    return text.strip()

# Function to send email
def send_email(sender_email, sender_password, recipients, subject, body):
    try:
        # Sanitize inputs to avoid non-breaking spaces and other invisible characters
        sender_email = sanitize_input(sender_email)
        subject = sanitize_input(subject)
        body = sanitize_input(body)
        recipients = [sanitize_input(email) for email in recipients]

        # Ensure all inputs are Unicode and properly encoded
        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = subject

        # Explicitly encode message body as UTF-8
        msg.set_content(body, charset="utf-8")
        
        # Ensure the payload is UTF-8 encoded
        msg.set_payload(msg.get_payload(), charset="utf-8")
        payload = msg.get_payload()
        payload_utf8 = payload.encode('utf-8')  # Explicit UTF-8 encoding for payload
        msg.set_payload(payload_utf8)

        # Connect to SMTP server and send email
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()  # Start TLS for security
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)

        return "Emails sent successfully!"
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.title("📧 Bulk Email Automation App")
st.markdown("""
### Send Emails to Multiple Recipients  
Fill in the fields below with your email details and recipient emails.
""")

# Input fields
with st.form("email_form"):
    sender_email = st.text_input("Your Email", placeholder="your_email@gmail.com")
    sender_password = st.text_input("Your App Password", type="password", placeholder="App Password")
    recipients_input = st.text_area("Recipient Emails (comma-separated)", placeholder="example1@gmail.com, example2@gmail.com")
    subject = st.text_input("Subject", placeholder="Subject of the email")
    body = st.text_area("Email Body", placeholder="Write your email here...")

    # Submit button
    submitted = st.form_submit_button("Send Emails")

# Handle submission
if submitted:
    if not sender_email or not sender_password or not subject or not body:
        st.error("All fields except recipients are required!")
    elif not recipients_input:
        st.error("Please provide recipient emails!")
    else:
        try:
            # Handle recipients from text area
            recipients = [
                sanitize_input(email)  # Sanitize non-breaking spaces and non-ASCII characters
                for email in recipients_input.split(",")
                if email.strip()
            ]

            if not recipients:
                st.error("No valid recipients found!")
            else:
                # Clean up subject and body to handle special characters
                subject = sanitize_input(subject)
                body = sanitize_input(body)

                # Send the emails
                result = send_email(sender_email, sender_password, recipients, subject, body)
                if "successfully" in result.lower():
                    st.success(result)
                else:
                    st.error(result)

        except Exception as e:
            st.error(f"An error occurred: {e}")
