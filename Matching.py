# Home.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import networkx as nx
from PIL import Image

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
            vec1 = user_vectors[name1].reshape(1, -1)
            vec2 = user_vectors[name2].reshape(1, -1)
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

def create_visualization(users, match_scores, threshold=0.3):
    fig = plt.figure(figsize=(12, 8), facecolor='black')
    ax = fig.add_subplot(111, facecolor='black')

    cmap = LinearSegmentedColormap.from_list("quantum", [(0.7, 0, 1, 0.2), (0.7, 0, 1, 0.8), (1, 0, 1, 1)])
    G = nx.Graph()

    for user in users:
        G.add_node(user['name'])

    for match, score in match_scores.items():
        if score >= threshold:
            u1, u2 = match.split(" ↔ ")
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
# STREAMLIT UI
# -----------------------------


st.set_page_config(page_title="Quantum Matcher", layout="wide")
st.title("Entangle@UNC")


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

# Compute match scores
st.subheader("Match Scores")
match_scores = compute_match_scores(user_vectors)

# Display the network graph first
threshold = st.slider("Match Strength Threshold", min_value=0.0, max_value=1.0, value=0.3)
fig = create_visualization(st.session_state.users, match_scores, threshold)
st.pyplot(fig)

# Display the bar chart next
plot_scores(match_scores)

# Show raw match scores in an expander
with st.expander("📊 View Raw Match Scores"):
    for match, score in sorted(match_scores.items(), key=lambda x: x[1], reverse=True):
        st.write(f"**{match}**: {score:.3f}")