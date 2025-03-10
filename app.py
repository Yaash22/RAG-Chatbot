import streamlit as st
import numpy as np
from rag_backend import init_db, save_to_db, load_from_db, process_query

def main():
    st.set_page_config(page_title="RAG based AI ChatBot model", page_icon="🤖", layout="wide")

    # Custom CSS for styling
    st.markdown("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
    }
    .chat-message.user {
        background-color: #2b313e
    }
    .chat-message.bot {
        background-color: #475063
    }
    .chat-message .avatar {
      width: 20%;
    }
    .chat-message .avatar img {
      max-width: 78px;
      max-height: 78px;
      border-radius: 50%;
      object-fit: cover;
    }
    .chat-message .message {
      width: 80%;
      padding: 0 1.5rem;
      color: #fff;
    }
    .stButton>button {
        background-color: #a8baba;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #a8baba;
    }
    .sidebar .element-container {
        background-color: #a8baba;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .new-chat-button {
        border: none;
        background: #a8baba;
        color: #a8baba;
        cursor: pointer;
        font-size: 1.5em;
    }
    .new-chat-button:hover {
        color: #a8baba;
    }
    .sidebar-title {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("RAG based AI Chat Model")

    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

    if st.button("New User"):
        st.session_state.user_id = np.random.randint(1000, 9999)
        st.session_state.conversation = []
        st.session_state.messages = []
        st.experimental_rerun()

    if st.session_state.user_id is None:
        st.write("Please click 'New User' to start a new conversation.")
        return

    st.session_state.conversation = load_from_db(st.session_state.user_id)
    
    sidebar_title_col, new_chat_col = st.sidebar.columns([3, 1])
    
    with sidebar_title_col:
        st.sidebar.header("Chat History")
    
    with new_chat_col:
        if st.sidebar.button("➕", key="new_chat", help="Start a new chat"):
            st.session_state.messages = []
            st.session_state.conversation = []
            st.experimental_rerun()

    for i, (user_q, bot_a) in enumerate(st.session_state.conversation):
        with st.sidebar.expander(f"Q: {user_q}", expanded=False):
            st.write(f"A: {bot_a}")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is your question?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # Process the query using backend functions
            bot_response = process_query(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for chunk in bot_response.split():
                    full_response += chunk + " "
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.session_state.conversation.append((prompt, full_response))
            save_to_db(st.session_state.user_id, prompt, full_response)
            
        except Exception as e:
            with st.chat_message("assistant"):
                st.markdown(f"Error processing your query: {str(e)}")

if __name__ == '__main__':
    init_db()
    main()