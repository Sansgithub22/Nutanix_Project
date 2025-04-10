import streamlit as st
from google import genai
from engine import get_ast_warnings, execute_code
import re

st.title("💡 HintBot — Learn to Debug Step by Step")

code_input = st.text_area("Paste your Python code here", height=300)

if st.button("Analyze"):
    if not code_input.strip():
        st.warning("Please paste some code to analyze.")
    else:
        with st.spinner("Analyzing..."):
            st.session_state['ast_hints'] = get_ast_warnings(code_input)
            st.session_state['runtime_hints'], st.session_state['traceback'], st.session_state['output'] = execute_code(code_input)
            st.session_state['analyzed'] = True
            st.session_state['show_ast'] = 1
            st.session_state['show_runtime'] = 1

            try:
                if st.session_state['runtime_hints'] or st.session_state['ast_hints']:
                    client = genai.Client(api_key="Your API KEY here")

                    fix_prompt = f"Correct the following Python code. Return only the corrected code without explanation:\n\n{code_input}"
                    fix_response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=fix_prompt
                    )
                    st.session_state['suggested_code'] = fix_response.text.strip("`")

                    explain_prompt = f"Explain the issues and fixes in this Python code:\n\n{code_input}"
                    explain_response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=explain_prompt
                    )
                    st.session_state['explanation'] = explain_response.text

                    readability_prompt = f"""Evaluate the readability of the following Python code. 
                    Give a readability score between 0 (hard to read) and 10 (very easy to read), and briefly justify the score.

                    Code:
                    {code_input}
                    """
                    readability_response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=readability_prompt
                    )
                    st.session_state['readability'] = readability_response.text
                else:
                    st.session_state['suggested_code'] = "✅ No more suggested fixes."
                    st.session_state['explanation'] = "✅ No more error explanations."

                    client = genai.Client(api_key="AIzaSyAUPjyd-IZz-INHYHjQGv7l_J8qxgAHsk8")
                    readability_prompt = f"""Evaluate the readability of the following Python code. 
                    Give a readability score between 0 (hard to read) and 10 (very easy to read), and briefly justify the score.

                    Code:
                    {code_input}
                    """
                    readability_response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=readability_prompt
                    )
                    st.session_state['readability'] = readability_response.text
                    
            except Exception as e:
                st.session_state['suggested_code'] = f"# Error: {str(e)}"
                st.session_state['explanation'] = ""

# Display results
if st.session_state.get('analyzed'):
    st.subheader("📘 Static Hints")
    ast_hints = st.session_state.get('ast_hints', [])
    if ast_hints:
        for i in range(st.session_state['show_ast']):
            st.info(f"Hint {i+1}: {ast_hints[i]}")
        if st.session_state['show_ast'] < len(ast_hints):
            if st.button("🔍 Reveal Next Static Hint"):
                st.session_state['show_ast'] += 1
    else:
        st.success("No static issues found.")

    st.subheader("🔍 Runtime Hints")
    runtime_hints = st.session_state.get('runtime_hints', [])
    if runtime_hints:
        for i in range(st.session_state['show_runtime']):
            st.warning(f"Hint {i+1}: {runtime_hints[i]}")
        if st.session_state['show_runtime'] < len(runtime_hints):
            if st.button("🔍 Reveal Next Runtime Hint"):
                st.session_state['show_runtime'] += 1

        st.markdown("📄 **Traceback** (if needed)")
        with st.expander("See Full Traceback"):
            st.code(st.session_state.get('traceback', ''), language="python")
    else:
        st.success("Your code ran without errors!")
        # ✅ Show terminal-like output
        if st.session_state.get('output'):
            st.subheader("📤 Program Output")
            st.code(st.session_state['output'], language="text")
    

    # Always show these two sections
    st.subheader("💡 Suggested Code")
    with st.expander("🛠️ See Suggested Code"):
        st.code(st.session_state.get('suggested_code', ''), language="python")

    st.subheader("🧠 Explain Fix")
    with st.expander("📘 Explain Fix"):
        st.markdown(st.session_state.get('explanation', ''))

    st.subheader("📊 Readability Score")
    st.markdown(st.session_state.get('readability', ''))

    st.caption("HintBot helps you *learn* — not just fix.")
