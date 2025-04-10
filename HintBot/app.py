import streamlit as st
from google import genai  # Gemini Client
from engine import get_ast_warnings, execute_code
import re

st.title("💡 HintBot — Learn to Debug Step by Step")

code_input = st.text_area("Paste your Python code here", height=300)

# Button to analyze code
if st.button("Analyze"):
    if not code_input.strip():
        st.warning("Please paste some code to analyze.")
    else:
        with st.spinner("Analyzing..."):
            st.session_state['ast_hints'] = get_ast_warnings(code_input)
            st.session_state['runtime_hints'], st.session_state['traceback'] = execute_code(code_input)
            st.session_state['show_ast'] = 1
            st.session_state['show_runtime'] = 1
            st.session_state['analyzed'] = True

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

    st.subheader("💡 Suggested Code & Explanation")

    try:
        with st.spinner("Fetching corrected code and explanation..."):
            client = genai.Client(api_key="AIzaSyAUPjyd-IZz-INHYHjQGv7l_J8qxgAHsk8")  # Your key here

            # Prompt for corrected code
            prompt_code = f"""You are an expert Python developer.

Fix the following Python code and return only the corrected version as raw code (no markdown, no explanation, no triple backticks).

Code:
{code_input}
"""
            response_code = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt_code
            )
            suggested_code = response_code.text.strip() if response_code.text else "# No suggestions available."

            # Remove markdown wrapping if Gemini adds it anyway
            suggested_code = re.sub(r"^```python|```$", "", suggested_code, flags=re.MULTILINE).strip()

            # Prompt for explanation
            prompt_explain = f"""You are an expert Python tutor.

Explain the bugs and issues in the following code and how they were fixed. Be concise and beginner-friendly.

Code:
{code_input}
"""
            response_explain = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt_explain
            )
            explanation = response_explain.text.strip() if response_explain.text else "No explanation available."

    except Exception as e:
        suggested_code = f"# Error: {str(e)}"
        explanation = "Could not fetch explanation due to error."

    with st.expander("🛠️ See Suggested Code"):
        st.text(suggested_code)

    with st.expander("📘 Explain Fix"):
        st.markdown(explanation)

    st.caption("HintBot helps you *learn* — not just fix.")
