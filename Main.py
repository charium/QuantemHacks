# Home.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# FUNCTIONS
# -----------------------------
def map_user_to_params(user):
    theta = np.pi * user["experience"]
    phi = np.pi * user["interest"]
    return theta, phi

def get_user_statevector(theta, phi):
    qc = QuantumCircuit(1)
    qc.ry(theta, 0)
    qc.rz(phi, 0)
    state = Statevector.from_instruction(qc)
    return state.data.real

def compute_match_scores(user_vectors):
    match_scores = {}
    names = list(user_vectors.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            name1, name2 = names[i], names[j]
            vec1, vec2 = user_vectors[name1].reshape(1, -1), user_vectors[name2].reshape(1, -1)
            similarity = cosine_similarity(vec1, vec2)[0][0]
            key = f"{name1} ↔ {name2}"
            match_scores[key] = similarity
    return match_scores

def plot_scores(match_scores):
    names = list(match_scores.keys())
    scores = list(match_scores.values())
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(names, scores, color='teal')
    ax.set_xlabel("Quantum Vector Similarity (Cosine Score)")
    ax.set_title("Compatibility Between Participants (Vector-Based)")
    ax.grid(True, axis='x')
    st.pyplot(fig)

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="Quantum Matcher", layout="wide")
st.title("🔮 Quantum Collaborator Matcher")

if 'users' not in st.session_state:
    st.session_state.users = [
        {"name": "Alice", "experience": 0.2, "interest": 0.6},
        {"name": "Bob", "experience": 0.8, "interest": 0.5},
        {"name": "Charlie", "experience": 0.5, "interest": 0.9},
    ]

# -----------------------------
# MAIN DISPLAY
# -----------------------------
st.subheader("Current Users")
st.table(st.session_state.users)

# Encode users into statevectors
user_vectors = {}
for user in st.session_state.users:
    theta, phi = map_user_to_params(user)
    vec = get_user_statevector(theta, phi)
    user_vectors[user["name"]] = vec

# Compute and plot matches
st.subheader("Match Scores")
match_scores = compute_match_scores(user_vectors)
plot_scores(match_scores)