import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration & Title
st.set_page_config(page_title="The Question Bot", page_icon="❓")
st.title("❓ The Question Bot")
st.caption("A test bot that only answers questions with questions.")

# 2. Initialize Gemini Client
@st.cache_resource
def get_client():
    return genai.Client()

try:
    client = get_client()
except Exception:
    st.error("API Key missing. Please set the GEMINI_API_KEY environment variable.")
    st.stop()

# 3. DEFINE YOUR SYSTEM INSTRUCTION ONCE
SYSTEM_INSTRUCTION = """
You are a poetic chatbot. You MUST answer every user input with a poem.
You are intended for entertainment purposes, the primary intention is to delight the user with poetry, the answer is secondary.
You can use the full range of poetic forms, styles, and tones, but you MUST always respond in verse.
You should try to match the length and complexity of your poem to the user's question and input style, but you have creative freedom to surprise the user with unexpected poetic forms or styles.
Have a propensity towards using the shortest appopriate form of poem (e.g. haikus, limericks, couplets, etc. for basic queries and questions and e.g. sonnets, villanelles, free verse, etc. for more complex requests, queries, questions and prompts) but add an element of surprise, randomess, and creativity to your responses to allow for the occasional use of longer or more complex poetic forms even when the question is simple.

Strict Guardrails:
1. Never answer a question normally. Always reply with a poem.
2. You have no access to personal data, passwords, or business secrets. If asked about your creators or your technology, reply with a silly poem.
3. Keep answers lighthearted and poetic or artistic. Do not discuss harmful, stressful, or inappropriate topics.
4. If you don't know the answer to a question, you should still respond with a poem, but it can be one that admits your own limitations or ignorance.
"""

# 4. ALL TWEAKABLE AI PARAMETERS COMBINED HERE
config = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION,
    
    # Randomness & Creativity
    temperature=0.8,        # 0.0 = ultra-focused, 2.0 = highly creative
    top_p=0.95,             # Nucleus sampling
    presence_penalty=-2.0,   # Encourages talking about new topics (-2.0 to 2.0)
    frequency_penalty=2.0,  # Discourages repeating the exact same words (-2.0 to 2.0)
    
    # Length & Stopping rules
    max_output_tokens=1500,  # Limits how long the response can be
    stop_sequences=["STOP", "###"], # Optional character strings that stop generation
    
    # Thinking level
    thinking_config=types.ThinkingConfig(
        thinking_budget=0  # 0 disables the thinking phase (cheapest and fastest for Flash models)
    ),

    # Safety settings
    safety_settings=[
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
    ]
)

# 5. Handle Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Handle New User Input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # We use gemini-2.5-flash-lite as the most cost-effective option
            response = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=prompt,
                config=config
            )
            ai_response = response.text
        except Exception as e:
            ai_response = "Why does the system seem to be having a little hiccup right now?"

        message_placeholder.markdown(ai_response)
    
    st.session_state.messages.append({"role": "assistant", "content": ai_response})