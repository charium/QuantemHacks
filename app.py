import streamlit as st

authors = ["Akshan Sameullah, Lila Anafi, Milena Páez Silva, and Chloe Hall"]
st.set_page_config(page_title="Entagle! ", page_icon="🧠")

st.title("🧠 Find your best match")
st.markdown("This survey assesses your **interest** and **experience** in quantum computing to help match potential collaborators.")

value = 5  # Normalization factor

st.footer("Created by " + ", ".join(authors))
# Define survey questions
interest_questions = [
    "a1. How interested are you in quantum computing? (1-5)",
    "a2. Have you read any articles or books about quantum computing? (1-5)",
    "a3. Do you follow quantum computing news or research? (1-5)",
    "a4. Do you plan to pursue a career involving quantum computing? (1-5)",
    "a5. Are you interested in the theoretical foundations of quantum computing? (1-5)",
]

experience_questions = [
    "b1. Have you used Qiskit or any quantum computing framework in Python? (1-5)",
    "b2. Can you write a basic quantum circuit using Python? (1-5)",
    "b3. Have you ever simulated a quantum circuit using Python? (1-5)",
    "b4. Have you used IBM Quantum Lab or any cloud quantum services? (1-5)",
    "b5. Do you understand the basics of Python required for quantum programming? (1-5)",
]

# User session dictionary
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# Input for number of users
st.header("Settings")
num_users = st.number_input("How many users to collect?", min_value=1, max_value=10, step=1)

# Loop for user survey
for i in range(num_users):
    with st.expander(f"User {i+1} Survey", expanded=(i == 0)):
        name = st.text_input(f"👤 Enter your name", key=f"name_{i}")
        
        i_responses = {}
        st.subheader("📈 Interest Questions")
        for q in interest_questions:
            i_responses[q] = st.slider(q, 1, 5, 3, key=f"i_{i}_{q}")
        
        e_responses = {}
        st.subheader("🧪 Experience Questions")
        for q in experience_questions:
            e_responses[q] = st.slider(q, 1, 5, 3, key=f"e_{i}_{q}")
        
        if st.button("Submit Responses", key=f"submit_{i}") and name:
            i_score = sum(i_responses.values()) / value**2 
            e_score = sum(e_responses.values()) / value**2
            
            st.session_state.user_data[name] = {
                "interest": round(i_score, 2),
                "experience": round(e_score, 2)
            }
            if name not in st.session_state.user_data:
                st.error("Please enter your name before submitting.")
            else: 
                st.success(f"✅ Data submitted for {name}")
               

# Show collected data
if st.session_state.user_data:
    st.header("📊 Collected Data")
    for user, scores in st.session_state.user_data.items():
        st.write(f"**{user}**: Interest = {scores['interest']}, Experience = {scores['experience']}")
    
from MatchPair import run_matching

if st.button("🧠 Run Quantum Matching"):
    if st.session_state.user_data:
        match_scores = run_matching(st.session_state.user_data)
        
        st.header("🔗 Match Results")
        for pair, score in match_scores.items():
            st.write(f"**{pair}**: {round(score, 3)}")

        # Optional: Show as a bar chart
        st.bar_chart(match_scores)
    else:
        st.warning("No user data to match!")
