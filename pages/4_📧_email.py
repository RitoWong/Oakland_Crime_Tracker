import smtplib
import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(user_name, user_email, subject, message):
    sender_email = 'ritoproject2024@gmail.com'
    sender_password = 'xmcudiqehvtusbcy'
    recipient_email = 'ritoproject2024@gmail.com'

    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = user_email
        msg['To'] = recipient_email
        msg['Subject'] = f"From {user_name}: {subject}"

        # Attach the message body
        email_body = f"Message from {user_name} ({user_email}):\n\n{message}"
        msg.attach(MIMEText(email_body, 'plain'))

        # Connect to the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())

        st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"An error occurred while sending the email: {str(e)}")
    finally:
        # Close the connection to the SMTP server
        server.quit()

def main():
    st.set_page_config(page_title="Recommendations for Improvement", page_icon="📧")
    
    st.title("Recommendations for Improvement")

    # Introduction
    st.markdown("Please leave your comments or suggestions to help us improve this program.")

    # User Information
    user_name = st.text_input("Your Name:")
    user_email = st.text_input("Your Email:")

    # Subject
    subject = st.text_input("Subject:")

    # Message
    message = st.text_area("Message:")

    # Send button
    if st.button("Send Email"):
        if user_name and user_email and subject and message:
            send_email(user_name, user_email, subject, message)
        else:
            st.warning("Please fill in all the fields.")

# Run the app
if __name__ == "__main__":
    main()
