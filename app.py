import streamlit as st
import requests
import json

def get_bot_response(user_input):
    url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {"sender": "user", "message": user_input}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        response_json = response.json()  # Directly get JSON response
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the Rasa server: {e}")
        return  # Exit the function if there's an error
    
    print(response_json)  # Debug: Check the response structure
    
    for res in response_json:
        for key, value in res.items():
            if key == 'image':
                st.chat_message("AI").image(value)
                st.session_state.messages.append({"role": "AI", "image": value})
            elif key == 'text':
                st.chat_message("AI").write(value)
                st.session_state.messages.append({"role": "AI", "message": value})
            elif key == 'attachment':
                values = value['payload']['src']
                st.chat_message("AI").video(values)
                st.session_state.messages.append({"role": "AI", "video": values})

def CreateApp():
    st.title("Welcome to Simple Rasa ChatBot With Streamlit")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "AI", "message": "How can I help you?"}]

    for msg in st.session_state.messages:
        role = msg["role"]
        if "image" in msg:
            with st.chat_message(role):
                st.image(msg["image"])
        elif "video" in msg:
            with st.chat_message(role):
                st.video(msg["video"])
        elif "message" in msg:
            with st.chat_message(role):
                st.write(msg["message"])

    user_input = st.chat_input()

    if user_input:
        st.chat_message("User").write(user_input)
        st.session_state.messages.append({"role": "User", "message": user_input})
        get_bot_response(user_input)

if __name__ == "__main__":
    CreateApp()