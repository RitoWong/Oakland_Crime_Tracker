import smtplib
import streamlit as st
import os
from PIL import Image
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

def send_email(recipient_email, subject, message, screenshot_path):
    sender_email = 'ritoproject2024@gmail.com'
    sender_password = 'xmcudiqehvtusbcy'

    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach the message body
        msg.attach(MIMEText(message, 'plain'))

        # Attach the screenshot image if it exists
        if os.path.exists(screenshot_path):
            with open(screenshot_path, 'rb') as f:
                img = MIMEImage(f.read())
            img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(screenshot_path))
            msg.attach(img)
        else:
            reminder_message = "Please go to the City Navigation app to create a screenshot."
            msg.attach(MIMEText(reminder_message, 'plain'))

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

# Create the Streamlit app
def main():
    st.set_page_config(page_title="Oakland Crime Tracker", page_icon="📌")
    
    st.title("Email Sender")

    # Recipient Email
    recipient_email = st.text_input("Recipient Email:")

    # Subject
    subject = st.text_input("Subject:")

    # Message
    message = st.text_area("Message:")

    # Screenshot
    screenshot_path = "screenshot.jpg"
    screenshot = Image.open(screenshot_path)
    st.image(screenshot, caption='Screenshot', use_column_width=True)

    # Check if screenshot exists
    if not os.path.exists(screenshot_path):
        st.warning("No screenshot found. Please go to the City Navigation app to create a screenshot.")

    # Send button
    if st.button("Send Email"):
        if recipient_email and subject and message:
            send_email(recipient_email, subject, message, screenshot_path)
        else:
            st.warning("Please fill in all the fields.")

# Run the app
if __name__ == "__main__":
    main()