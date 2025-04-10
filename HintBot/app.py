import streamlit as st
from engine import get_ast_warnings, execute_code

st.title("💡 HintBot — Debugging Assistant that Trains Your Brain")

code_input = st.text_area("Paste your Python code here", height=300)

if st.button("Analyze"):
    if not code_input.strip():
        st.warning("Please paste some code to analyze.")
    else:
        with st.spinner("Analyzing your code..."):
            ast_hints = get_ast_warnings(code_input)
            runtime_hints, tb = execute_code(code_input)

            st.subheader("📘 Static Hints")
            if ast_hints:
                for h in ast_hints:
                    st.info(h)
            else:
                st.success("No obvious static issues found!")

            st.subheader("🔍 Runtime Hints")
            if runtime_hints:
                for i, h in enumerate(runtime_hints):
                    st.warning(f"Hint {i+1}: {h}")
                with st.expander("See Traceback"):
                    st.code(tb, language="python")
            else:
                st.success("Your code ran without errors!")

        st.caption("HintBot helps you *learn* — not just fix.")
