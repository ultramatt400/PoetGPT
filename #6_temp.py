    Debug version:

    if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Send content to the Gemini API
            response = client.models.generate_content(
                model='gemini-2.5-flash',  # Tweak this to gemini-1.5-flash if you still get an error
                contents=prompt,
                config=config
            )
            ai_response = response.text
        except Exception as e:
            # THIS IS THE DEBUG LINE -> Prints the exact API error in your VS Code terminal
            print(f"DEBUG ERROR: {e}")
            ai_response = "Why does the system seem to be having a little hiccup right now?"

        message_placeholder.markdown(ai_response)
    
    st.session_state.messages.append({"role": "assistant", "content": ai_response})