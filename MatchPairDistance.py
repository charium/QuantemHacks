# -----------------------------
# IMPORTS
# -----------------------------
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from sklearn.metrics.pairwise import cosine_similarity
# -----------------------------
# SIMULATED USER DATA
# -----------------------------
USERS = [
    {"name": "Alice", "experience": 0.2, "interest": 0.6},
    {"name": "Bob", "experience": 0.8, "interest": 0.5},
    {"name": "Charlie", "experience": 0.5, "interest": 0.9},
]
# -----------------------------
# FUNCTIONS TO ENCODE USERS AND EXTRACT STATEVECTORS
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
    return state.data.real  # use real part only for similarity calc

# -----------------------------
# CREATE VECTOR EMBEDDINGS
# -----------------------------
user_vectors = {}
for user in USERS:
    theta, phi = map_user_to_params(user)
    vec = get_user_statevector(theta, phi)
    user_vectors[user["name"]] = vec

# -----------------------------
# COMPUTE COSINE SIMILARITIES (HIGHER = MORE SIMILAR)
# -----------------------------
match_scores = {}
names = list(user_vectors.keys())

for i in range(len(names)):
    for j in range(i + 1, len(names)):
        name1, name2 = names[i], names[j]
        vec1, vec2 = user_vectors[name1].reshape(1, -1), user_vectors[name2].reshape(1, -1)
        similarity = cosine_similarity(vec1, vec2)[0][0]
        key = f"{name1} :left_right_arrow: {name2}"
        match_scores[key] = similarity
        print(f"Match {key}: {similarity:.3f}")

# -----------------------------
# BAR CHART OF MATCHING RESULTS
# -----------------------------
names = list(match_scores.keys())
scores = list(match_scores.values())
plt.figure(figsize=(10, 5))
plt.barh(names, scores, color='teal')
plt.xlabel("Quantum Vector Similarity (Cosine Score)")
plt.title("Compatibility Between Participants (Vector-Based)")
plt.grid(True, axis='x')
plt.show()