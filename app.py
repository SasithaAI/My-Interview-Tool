
import streamlit as st
from openai import OpenAI
from streamlit_js_eval import streamlit_js_eval



st.set_page_config(page_title="MyStreamLit Chat",page_icon="🇱🇰")
st.title("This Is  My  Chat Box ")

# Initialize session state variable to track setup completion
if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False

# Initialize User Interaction Count
if "user_interaction_Count" not in st.session_state:
    st.session_state.user_interaction_Count = 0

# Initialize User Feed Back Display
if "user_Feedback_Display" not in st.session_state:
    st.session_state.user_Feedback_Display = False

# Initialize User Feed Back Messages State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize  User Interaction Complete State 
if "chat_complete" not in st.session_state:
    st.session_state.chat_complete = False

# Helper function to update session state
def complete_setup():
    st.session_state.setup_complete = True

# Helper function to Display Feed back state
def show_feedback():
    st.session_state.user_Feedback_Display = True



if not st.session_state.setup_complete:

    # Personal Information Section
    st.subheader('Personal information', divider='rainbow')

    if "name" not in st.session_state:
        st.session_state["name"] = ""
    if "experience" not in st.session_state:
        st.session_state["experience"] = ""
    if "skills" not in st.session_state:
        st.session_state["skills"] = ""

    # Input fields for collecting user's personal information
    st.session_state["name"] = st.text_input(label = "Name", max_chars = 40, placeholder = "Enter your name")

    st.session_state["experience"] = st.text_area(label = "Expirience", value = "", height = None, max_chars = 200, placeholder = "Describe your experience")

    st.session_state["skills"] = st.text_area(label = "Skills", value = "", height = None, max_chars = 200, placeholder = "List your skills")



    # Test labels for personal information
    st.write(f"**Your Name**: {st.session_state['name']}")
    st.write(f"**Your Experience**: {st.session_state['experience']}")
    st.write(f"**Your Skills**: {st.session_state['skills']}")

    # Company and Position Section
    st.subheader('Company and Position', divider = 'rainbow')

    if "level" not in st.session_state:
        st.session_state["level"] = "Junior"
    if "position" not in st.session_state:
        st.session_state["position"] = "Data Scientist"
    if "company" not in st.session_state:
        st.session_state["company"] = "Amazon"

    #Field for selecting the job level, position and company
    col1, col2 = st.columns(2)
    with col1:
        st.session_state["level"]  = st.radio(
        "Choose level",
        key="visibility",
        options=["Junior", "Mid-level", "Senior"],
        )

    with col2:
        st.session_state["position"] = st.selectbox(
        "Choose a position",
        ("Data Scientist", "Data engineer", "ML Engineer", "BI Analyst", "Financial Analyst"))

    st.session_state["company"] = st.selectbox(
        "Choose a Company",
        ("Amazon", "Meta", "Udemy", "365 Company", "Nestle", "LinkedIn", "Spotify")
    )

    # Test labels for company and position information
    st.write(f"**Your information**: {st.session_state['level']} {st.session_state['position']} at {st.session_state['company']}")


    # A button to complete the setup stage and start the interview
    if st.button("Start Interview", on_click=complete_setup):
        st.write("Setup complete. Starting interview...")

# Interview stage
if st.session_state.setup_complete and not st.session_state.user_Feedback_Display and not st.session_state.chat_complete :
    # Display a welcome message and prompt the user to introduce themselves
    st.info(
        """
        Start by introducing yourself.
        """,
        icon = "👋"
    )



# Open AI Codes 

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "opennai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"


# Initializing the 'messages' list 
if not st.session_state.messages:
    st.session_state.messages = [{"role":"system", "content": f"You are an HR executive that interviews an interviewee called {st.session_state['name']} with expirience {st.session_state['experience']} and skills {st.session_state['skills']}. You should interview him for the position {st.session_state['position']} for level of {st.session_state['level']} at the company {st.session_state['company']}"}]


# Looping through the 'messages' list to display each message except system messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
# Input field for the user to send a new message

if st.session_state.user_interaction_Count < 5:
    if prompt := st.chat_input("Your answer.",max_chars= 500):
        # Appending the user's input to the 'messages' list in session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display the user's message in a chat bubble
        with st.chat_message("user"):
            st.markdown(prompt)
    
        # Assistant's response
        if st.session_state.user_interaction_Count < 4:
            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True, # This line enables streaming for real-time response
                )
                # Display the assistant's response as it streams
                response = st.write_stream(stream)
            # Append the assistant's full response to the 'messages' list
            st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.user_interaction_Count+=1

    if st.session_state.user_interaction_Count > 5:
        with st.chat_message("assistant"):
         stream = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages={"role": "assistant","content":"please provide a polite joke"},
                    stream=True, # This line enables streaming for real-time response
                )
                # Display the assistant's response as it streams
        lastresponse = st.write_stream(stream)
        # Append the assistant's full response to the 'messages' list
        st.session_state.messages.append({"role": "assistant", "content": lastresponse})
    st.session_state.chat_complete = True

# Show "Get Feedback" 
if st.session_state.chat_complete and not st.session_state.user_Feedback_Display:
    if st.button("Get Feedback", on_click=show_feedback):
        st.write("Fetching feedback...")

# Show feedback screen
if st.session_state.user_Feedback_Display:
    st.subheader("Feedback")

    conversation_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])

    # Initialize new OpenAI client instance for feedback
    feedback_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Generate feedback using the stored messages and write a system prompt for the feedback
    feedback_completion = feedback_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """You are a helpful tool that provides feedback on an interviewee performance.
             Before the Feedback give a score of 1 to 10.
             Follow this format:
             Overal Score: //Your score
             Feedback: //Here you put your feedback
             Give only the feedback do not ask any additional questins.
              """},
            {"role": "user", "content": f"This is the interview you need to evaluate. Keep in mind that you are only a tool. And you shouldn't engage in any converstation: {conversation_history}"}
        ]
    )

    st.write(feedback_completion.choices[0].message.content)

    # Button to restart the interview

    if st.button("Restart Interview", type="primary"):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")
