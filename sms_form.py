import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

st.title('Sign up to be on the texting list for Melinda Smith Photography!')

credentials = {
    "type": st.secrets.sheets_credentials.type,
    "project_id": st.secrets.sheets_credentials.project_id,
    "private_key_id": st.secrets.sheets_credentials.private_key_id,
    "private_key": st.secrets.sheets_credentials.private_key,
    "client_email": st.secrets.sheets_credentials.client_email,
    "client_id": st.secrets.sheets_credentials.client_id,
    "auth_uri": st.secrets.sheets_credentials.auth_uri,
    "token_uri": st.secrets.sheets_credentials.token_uri,
    "auth_provider_x509_cert_url": st.secrets.sheets_credentials.auth_provider_x509_cert_url,
    "client_x509_cert_url": st.secrets.sheets_credentials.client_x509_cert_url
}

# Set up credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
client = gspread.authorize(creds)

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def email_check(email):
 
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False

success_message = ""
error_message = ""

container = st.empty()

with container.container():
    first_name_value = st.text_input("First Name")
    first_name_value =first_name_value.title()

    last_name_value = st.text_input("Last Name")
    last_name_value =last_name_value.title()

    help_msg = "Phone number should consist of 10 digits and no special characters such as (,),-"

    phone_value = st.text_input("Phone Number", max_chars=10, help=help_msg)

    email_value = st.text_input("Email (optional)")

    contact = [first_name_value, last_name_value, phone_value, email_value]

    if st.button("Submit"):
        if first_name_value and phone_value and last_name_value and len(phone_value)>9:
            if email_value:
                if email_check(email_value) == False:
                    error_message = f"Please enter a valid email to submit."
                    email_value = ""
            if not error_message:
                # Open the Google Sheet by title
                sheet = client.open("contacts sheet")
                
                # Select the worksheet where you want to add the row
                worksheet = sheet.get_worksheet(0)  # Use the index (0-based) or title of the worksheet

                # Append the row to the worksheet
                worksheet.append_row(contact)
                
                container.empty()

                success_message = "Thanks for signing up! Your info has been saved."
        else:
            if phone_value.isnumeric() == False or len(phone_value)<10:
                missing_value = "10 digit phone number"
                phone_value = ""
            elif email_check(email_value) == False:
                missing_value = "valid email"
            elif not first_name_value:
                missing_value = "first name"
            elif not last_name_value:
                missing_value = "last name"
            else:
                missing_value = "phone number"
            error_message = f"Please enter a {missing_value} to submit."

if success_message:     
    st.success(success_message)

if error_message:
    st.error(error_message)