# pages/1_User_Survey.py

import streamlit as st

st.set_page_config(page_title="Quantum Survey")

st.title("🧪 Quantum Interest & Experience Survey")

st.write("Please fill out the following survey to assess your interest and experience in quantum computing. Your responses will be used to calculate your quantum compatibility profile.")

# -----------------------------
# Interest Survey Questions
# -----------------------------
st.header("✨ Interest Survey")

interest_questions = [
    "a1. How interested are you in quantum computing?",
    "a2. Have you read any articles or books about quantum computing?",
    "a3. Do you follow quantum computing news or research?",
    "a4. Do you plan to pursue a career involving quantum computing?",
    "a5. Are you interested in the theoretical foundations of quantum computing?",
]

interest_scores = []
for q in interest_questions:
    score = st.slider(q + " (1-5)", 1, 5, 3, key=q)
    interest_scores.append(score)

# -----------------------------
# Experience Survey Questions
# -----------------------------
st.header("🛠️ Experience Survey")

experience_questions = [
    "b1. Have you used Qiskit or any quantum computing framework in Python?",
    "b2. Can you write a basic quantum circuit using Python?",
    "b3. Have you ever simulated a quantum circuit using Python?",
    "b4. Have you used IBM Quantum Lab or any cloud quantum services?",
    "b5. Do you understand the basics of Python required for quantum programming?",
]

experience_scores = []
for q in experience_questions:
    score = st.slider(q + " (1-5)", 1, 5, 3, key=q)
    experience_scores.append(score)

# -----------------------------
# Name & Submission
# -----------------------------
st.header("📇 Your Information")
user_name = st.text_input("Enter your name")

if st.button("Submit"):
    if user_name.strip() == "":
        st.warning("Please enter your name.")
    else:
        avg_interest = sum(interest_scores) / len(interest_scores)
        avg_experience = sum(experience_scores) / len(experience_scores)

        # Normalize to 0–1
        interest_normalized = (avg_interest - 1) / 4
        experience_normalized = (avg_experience - 1) / 4

        if 'users' not in st.session_state:
            st.session_state.users = []

        st.session_state.users.append({
            "name": user_name.strip(),
            "interest": interest_normalized,
            "experience": experience_normalized
        })

        st.success(f"Thanks, {user_name}! You've been added to the matcher.")
        st.balloons()