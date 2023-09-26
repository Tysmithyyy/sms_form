import streamlit as st
from csv import writer

st.title('Sign up for my texting list!')

success_message = ""

container = st.empty()

with container.container():
    name_value = st.text_input("Name")

    phone_value = st.text_input("Phone Number", max_chars=10)

    contact = [name_value, phone_value]

    if st.button("Submit"):
        with open('./static/contacts.csv', 'a') as f_object:
        
            # Pass this file object to csv.writer()
            # and get a writer object
            writer_object = writer(f_object)
        
            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow(contact)
        
            # Close the file object
            f_object.close()
        
        container.empty()

        success_message = "Thanks for signing up! Your number has been saved."

if success_message:     
    st.success(success_message)