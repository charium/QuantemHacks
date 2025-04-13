# Quantum Collaborator Matcher - UNC Hackathon Project
# Optimized version for qBraid with English comments only# -----------------------------
# IMPORTS
# -----------------------------
# MatchPair.py

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import Aer

def run_matching(user_data):
    USERS = []

    for name, scores in user_data.items():
        USERS.append({
            "name": name,
            "experience": scores["experience"],
            "interest": scores["interest"]
        })

    def map_user_to_params(user):
        theta = np.pi * user["experience"]
        phi = np.pi * user["interest"]
        return theta, phi

    def prepare_user_circuit(theta, phi):
        qc = QuantumCircuit(1)
        qc.ry(theta, 0)
        qc.rz(phi, 0)
        return qc

    def compare_users(user1, user2):
        theta1, phi1 = map_user_to_params(user1)
        theta2, phi2 = map_user_to_params(user2)
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
        match_prob = counts.get('11', 0) / 1024
        return match_prob, counts

    match_scores = {}
    for i in range(len(USERS)):
        for j in range(i + 1, len(USERS)):
            user1 = USERS[i]
            user2 = USERS[j]
            score, _ = compare_users(user1, user2)
            key = f"{user1['name']} ⟷ {user2['name']}"
            match_scores[key] = score
            print(f"Match {key}: {score:.3f}")

    # Optional: Plot chart
    names = list(match_scores.keys())
    scores = list(match_scores.values())
    plt.figure(figsize=(10, 5))
    plt.barh(names, scores, color='purple')
    plt.xlabel("Quantum Match Score (Probability of |11⟩)")
    plt.title("Compatibility Between Participants")
    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.grid(True, axis='x')
    plt.tight_layout()
    plt.show()

    return match_scores