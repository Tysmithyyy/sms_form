import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.title('Sign up for my texting list!')

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

success_message = ""

container = st.empty()

with container.container():
    name_value = st.text_input("Name")

    phone_value = st.text_input("Phone Number", max_chars=10)

    contact = [name_value, phone_value]

    if st.button("Submit"):
        # Open the Google Sheet by title
        sheet = client.open("contacts sheet")

        # Select the worksheet where you want to add the row
        worksheet = sheet.get_worksheet(0)  # Use the index (0-based) or title of the worksheet

        # Append the row to the worksheet
        worksheet.append_row(contact)
        
        container.empty()

        success_message = "Thanks for signing up! Your number has been saved."

if success_message:     
    st.success(success_message)