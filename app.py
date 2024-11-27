import streamlit as st
import smtplib
from email.message import EmailMessage

# Function to send email
def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        # Create email
        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.set_content(body, charset="utf-8")  # Set UTF-8 encoding

        # Connect to SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()  # Secure connection
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)

        return "Email sent successfully!"
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.title("📧 Email Automation App")
st.markdown("""
### Send Emails Easily with This App  
Fill in the fields below to send an email. Make sure to use your App Password for authentication.
""")

# Input fields
with st.form("email_form"):
    sender_email = st.text_input("Your Email", placeholder="your_email@gmail.com")
    sender_password = st.text_input("Your App Password", type="password", placeholder="App Password")
    recipient_email = st.text_input("Recipient Email", placeholder="recipient_email@example.com")
    subject = st.text_input("Subject", placeholder="Subject of the email")
    body = st.text_area("Email Body", placeholder="Write your email here...")

    # Submit button
    submitted = st.form_submit_button("Send Email")

# Send email if form is submitted
if submitted:
    if not sender_email or not sender_password or not recipient_email or not subject or not body:
        st.error("All fields are required!")
    else:
        # Clean up inputs to remove invisible characters like \xa0
        sender_email = sender_email.strip().replace("\xa0", " ")
        sender_password = sender_password.strip().replace("\xa0", " ")
        recipient_email = recipient_email.strip().replace("\xa0", " ")
        subject = subject.strip().replace("\xa0", " ")
        body = body.strip().replace("\xa0", " ")

        # Send email
        result = send_email(sender_email, sender_password, recipient_email, subject, body)
        if "successfully" in result.lower():
            st.success(result)
        else:
            st.error(result)
