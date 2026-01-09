import streamlit as st
import os
import google.generativeai as genai

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="Receipt Nagger",
    page_icon="💸",
    layout="centered"
)

# ---------------- API CONFIG ----------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- STYLING ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #EEF2FF, #FDF2F8);
}
h1 {
    color: #5B21B6;
}
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

# ---------------- UI ----------------
st.title("💸 Receipt Nagger")
st.caption("Turn unclear expense notes into clean, professional emails")

expense_text = st.text_area("Paste expense details:", height=120)
tone = st.radio(
    "Choose email tone:",
    ["Polite", "Strict"],
    horizontal=True
)

# ---------------- GENERATE EMAIL ----------------
if st.button("Generate Email"):
    if expense_text.strip():
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
                response = model.generate_content(prompt)
                output = response.text

                st.markdown(
                    f"<div class='result-card'>{output.replace(chr(10), '<br>')}</div>",
                    unsafe_allow_html=True
                )

                st.subheader("✏️ Edit & Copy")
                final_email = st.text_area(
                    "Final Email:",
                    value=output,
                    height=220
                )

                st.info("👉 Select and copy the email above")

            except Exception as e:
                st.error(f"Error: {e}")

    else:
        st.warning("Please enter expense details.")

# ---------------- SIDEBAR ----------------
st.sidebar.success(
    "✔ Saves time\n\n"
    "✔ Reduces follow-ups\n\n"
    "✔ Professional emails"
)
