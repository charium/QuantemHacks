import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import networkx as nx
from qiskit import QuantumCircuit
from qiskit_aer import Aer
import numpy as np
from math import acos, pi
import random

# -----------------------------
# Initialization
# -----------------------------
st.set_page_config(page_title="Quantum Dating", layout="wide")
random.seed(42)

if "users" not in st.session_state:
    st.session_state.users = [
        {"name": name, "experience": random.random(), "interest": random.random()}
        for name in ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi",
                     "Ivan", "Judy", "Karl", "Leo", "Mallory", "Nina", "Oscar", "Peggy"]
    ]

# -----------------------------
# Core Functions
# -----------------------------
def map_user_to_params(user):
    theta = np.pi * user["experience"]
    phi = np.pi * user["interest"]
    return theta, phi

def compare_users(user1, user2):
    theta1, phi1 = map_user_to_params(user1)
    theta2, phi2 = map_user_to_params(user2)

    vec1 = np.array([
        np.cos(theta1/2),
        np.exp(1j*phi1) * np.sin(theta1/2)
    ])
    vec2 = np.array([
        np.cos(theta2/2),
        np.exp(1j*phi2) * np.sin(theta2/2)
    ])

    dot_product = np.abs(np.dot(vec1.conj(), vec2))
    angle = acos(min(dot_product, 1.0))
    classical_similarity = 1 - (angle / pi)

    qc = QuantumCircuit(2, 2)
    qc.ry(theta1, 0)
    qc.rz(phi1, 0)
    qc.ry(theta2, 1)
    qc.rz(phi2, 1)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    simulator = Aer.get_backend("qasm_simulator")
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts()
    quantum_match_prob = counts.get('11', 0) / 1024

    final_similarity = (classical_similarity + quantum_match_prob) / 2
    return final_similarity

def calculate_match_scores(users):
    match_scores = {}
    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            user1, user2 = users[i], users[j]
            sim = compare_users(user1, user2)
            key = f"{user1['name']} :left_right_arrow: {user2['name']}"
            match_scores[key] = sim
    return match_scores

def create_visualization(users, match_scores, threshold=0.3):
    fig = plt.figure(figsize=(12, 8), facecolor='black')
    ax = fig.add_subplot(111, facecolor='black')

    cmap = LinearSegmentedColormap.from_list("quantum", [(0.7, 0, 1, 0.2), (0.7, 0, 1, 0.8), (1, 0, 1, 1)])
    G = nx.Graph()

    for user in users:
        G.add_node(user['name'])

    for match, score in match_scores.items():
        if score >= threshold:
            u1, u2 = match.split(" :left_right_arrow: ")
            G.add_edge(u1, u2, weight=score)

    pos = nx.spring_layout(G, k=1, iterations=50)
    edges = G.edges()
    weights = [G[u][v]['weight'] * 3 for u, v in edges]
    edge_colors = [G[u][v]['weight'] for u, v in edges]

    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, edge_cmap=cmap, width=weights, ax=ax)
    nx.draw_networkx_nodes(G, pos, node_color='white', node_size=3000, alpha=0.7, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='white', ax=ax)

    ax.set_title("Quantum Compatibility Network", color='white')
    ax.set_axis_off()
    return fig

# -----------------------------
# Streamlit Interface
# -----------------------------
st.title("🔍 Quantum Dating Compatibility")
st.write("This app simulates dating compatibility between users using quantum state overlaps.")

# Sidebar to add/remove users
st.sidebar.header("👥 Manage Participants")

# Add user
new_user = st.sidebar.text_input("Add new user:")
if st.sidebar.button("Add User") and new_user:
    if new_user not in [u['name'] for u in st.session_state.users]:
        st.session_state.users.append({
            "name": new_user,
            "experience": random.random(),
            "interest": random.random()
        })

# Remove users
remove_list = st.sidebar.multiselect(
    "Remove selected users:",
    options=[user["name"] for user in st.session_state.users]
)
if st.sidebar.button("Remove Selected"):
    st.session_state.users = [u for u in st.session_state.users if u["name"] not in remove_list]

# Simulation threshold
threshold = st.slider("Match Strength Threshold", min_value=0.0, max_value=1.0, value=0.3)

# Main visualization
match_scores = calculate_match_scores(st.session_state.users)
fig = create_visualization(st.session_state.users, match_scores, threshold)
st.pyplot(fig)

with st.expander("📊 View Raw Match Scores"):
    for match, score in sorted(match_scores.items(), key=lambda x: x[1], reverse=True):
        st.write(f"**{match}**: {score:.3f}")