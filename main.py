import os  # Import the os module to interact with the operating system
import json  # Import the json module to work with JSON data

from PIL import Image  # Import the Image class from PIL for image processing
import streamlit as st  # Import Streamlit for building web applications
from streamlit_option_menu import option_menu  # Import option_menu for sidebar navigation

# Assuming 'config.json' is in the working directory
# Set the path for the config file

# config_path = os.path.join('D:/Python Projects/AI Assistant', 'config.json')
config_path = os.path.join(os.path.dirname(__file__), 'config.json')


# Load the config.json file to get configuration settings
with open(config_path, 'r') as f:
    config = json.load(f)  # Read the JSON data into a Python dictionary

# Import functions from gemini_utility module for AI functionality
from AI_Utility import (load_gemini_pro_model,  # Function to load the AI model
                            gemini_pro_response,  # Function to get a response from the AI
                            gemini_pro_vision_response,  # Function for image captioning
                            embeddings_model_response)  # Function for text embeddings

# Get the current working directory
working_dir = os.path.dirname(os.path.abspath(__file__))

# Set up the Streamlit page with a title, icon, and layout
st.set_page_config(
    page_title="Meet AstroMind",  # Set the title of the web page
    page_icon="🧠",  # Set the icon displayed in the browser tab
    layout="centered",  # Center the content on the page
)

# Sidebar for navigation options
with st.sidebar:
    # Create a menu for the app with different options
    selected = option_menu('AstroMind',
                        ['Talk with AI',  # First menu option
                        'Visionary Captions',  # Second menu option
                        'Embedded text',  # Third menu option
                        'Ask the Expert'],  # Fourth menu option
                        menu_icon='robot',  # Icon for the menu
                        icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill'],  # Icons for each option
                        default_index=0  # Set the default selected option
                        )

# Function to translate user roles for Streamlit's chat display
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"  # Change "model" to "assistant" for display
    else:
        return user_role  # Return the role as is if it's not "model"

# Chatbot page: Execute when 'Talk with AI' is selected
if selected == 'Talk with AI':
    model = load_gemini_pro_model()  # Load the AI model for chatting

    # Initialize chat session in Streamlit if not already present
    if "chat_session" not in st.session_state:  # Check if a chat session exists
        st.session_state.chat_session = model.start_chat(history=[])  # Start a new chat session

    # Display the chatbot's title on the page
    st.title("🤖 Interactive Agent")

    # Display the chat history from the session
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):  # Display each message based on its role
            st.markdown(message.parts[0].text)  # Show the text of the message

    # Input field for user's message
    user_prompt = st.chat_input("Ask your AI Assistant...")  # Input box for user queries
    if user_prompt:  # If the user has entered a prompt
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)  # Show user input in chat

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)  # Get the AI's response

        # Display Gemini-Pro's response in the chat
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)  # Show the AI's response text


# Image captioning page: Execute when 'Visionary Captions' is selected
if selected == "Visionary Captions":
    st.title("📷 Pic Insight")  # Set the title for the image captioning page
    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])  # Allow users to upload an image

    if st.button("Generate Caption"):  # Button to generate caption when clicked
        if uploaded_image is not None:  # Check if an image was uploaded
            try:
                image = Image.open(uploaded_image)  # Open the uploaded image
                col1, col2 = st.columns(2)  # Create two columns for layout
                with col1:
                    resized_img = image.resize((800, 500))  # Resize the image for display
                    st.image(resized_img)  # Show the resized image

                default_prompt = "write a short caption for this image"  # Set default prompt for captioning
                caption = gemini_pro_vision_response(default_prompt, image)  # Get the caption from the AI

                with col2:
                    st.info(caption)  # Show the generated caption in the second column

            except Exception as e:  # Handle any errors that occur during image processing
                st.error(f"Error processing the image: {e}")  # Display error message if something goes wrong
        else:
            st.warning("Please upload an image to generate a caption.")  # Warn if no image was uploaded


# Text embedding model page: Execute when 'Embedded text' is selected
if selected == "Embedded text":
    st.title("🔡 Embedded Text")  # Set the title for the text embedding page

    # Text box to enter prompt for embeddings
    user_prompt = st.text_area(label='', placeholder="Enter the text to get embeddings")  # Input box for user text

    if st.button("Get Response"):  # Button to get response when clicked
        response = embeddings_model_response(user_prompt)  # Get the embeddings for the entered text
        st.markdown(response)  # Show the response on the page


# Expert question page: Execute when 'Ask the Expert' is selected
if selected == "Ask the Expert":
    st.title("❓ Ask me a question")  # Set the title for the expert question page

    # Text box to enter prompt for questions
    user_prompt = st.text_area(label='', placeholder="Ask me anything...")  # Input box for user questions

    if st.button("Get Response"):  # Button to get response when clicked
        response = gemini_pro_response(user_prompt)  # Get the response from the AI for the question
        st.markdown(response)  # Show the response on the page