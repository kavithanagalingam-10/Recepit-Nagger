import streamlit as st
import google.generativeai as genai

# Page setup
st.set_page_config(page_title="Receipt Nagger", page_icon="💸", layout="centered")

# ✅ GENERATIVE AI CONFIG (FIXED)
genai.configure(api_key="AIzaSyD9RTmSpAAtlfyqSXqvR4G4Fdyn5jXD2fg")
model = genai.GenerativeModel("gemini-2.5-flash")

# Styling
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #EEF2FF, #FDF2F8); }
h1 { color: #5B21B6; }
div.stButton > button {
    background: linear-gradient(to right, #6366F1, #A855F7);
    color: white;
    font-size: 18px;
    border-radius: 10px;
    width: 100%;
}
.result-card {
    background: white;
    border-left: 6px solid #6366F1;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# UI
st.title("💸 Receipt Nagger")
st.caption("Turn unclear expense notes into clean, professional emails")

expense_text = st.text_area("Paste expense details:", height=120)
tone = st.radio("Choose email tone:", ["Polite", "Strict"], horizontal=True)

if st.button("Generate Email"):
    if expense_text:
        with st.spinner("Analyzing expenses..."):

            prompt = f"""
You are Receipt Nagger, an expense assistant.

Tasks:
1. Detect missing details (date, client, receipt, purpose).
2. Understand expense type (coffee, travel, food, etc.).
3. Follow company rules and use very simple English.
4. Create a clear subject line.
5. Write a {tone} professional email.
6. Handle multiple expenses if mentioned.
7. Keep the email editable and easy to copy.

Expense text:
{expense_text}
"""

            try:
                # ✅ GENERATIVE AI CALL (FIXED)
                response = model.generate_content(prompt)
                output = response.text

                st.markdown(
                    f"<div class='result-card'>{output.replace(chr(10), '<br>')}</div>",
                    unsafe_allow_html=True
                )

                st.subheader("✏️ Edit & Copy")
                final_email = st.text_area("Final Email:", value=output, height=220)

                # Copy to clipboard JS (UNCHANGED)
                st.write("""
                <script>
                function copyToClipboard() {
                    const text = document.querySelector('textarea').value;
                    navigator.clipboard.writeText(text).then(() => {
                        alert('Email copied to clipboard!');
                    }).catch(err => {
                        console.error('Failed to copy:', err);
                    });
                }
                </script>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Copy to Clipboard", use_container_width=True):
                        st.write(f"""
                        <script>
                        navigator.clipboard.writeText({repr(final_email)});
                        </script>
                        """, unsafe_allow_html=True)
                        st.success("✅ Email copied to clipboard!")

            except Exception as e:
                if "503" in str(e):
                    st.warning("AI is busy. Please try again in a few seconds.")
                else:
                    st.error(e)
    else:
        st.warning("Please enter expense details.")

# Sidebar
st.sidebar.success("✔ Saves time\n✔ Reduces follow-ups\n✔ Professional emails")