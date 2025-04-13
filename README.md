# 💫 Entangle@UNC – Quantum Matcher

**Entangle@UNC** is an interactive Streamlit web application that uses quantum state encoding to analyze and visualize compatibility between users based on their self-reported experience and interest levels.

---

## 🔍 Overview

This app maps user inputs (experience and interest) into quantum states using Qiskit's `QuantumCircuit` and `Statevector`. By comparing these statevectors via cosine similarity, it calculates match scores and visualizes relationships using bar charts and a dynamic network graph.

---
##Usage
Visit our deployed webpage: [entangled@unc](https://qentangled.streamlit.app/Survey)

The website it prepopulated with data. To enter custom data, click 'survey' in the lefthand sidebar and answer each question. Once the answers are submitted! They automatically update in the 'matching' section. You can view the raw match score in the bottom. 

## 📦 Features

- **Quantum State Encoding** – Converts user attributes into quantum statevectors.
- **Cosine Similarity Scoring** – Measures how aligned two users are in the quantum state space.
- **Interactive Threshold Slider** – Filters connections in the compatibility network.
- **Graphical Visualization** – Displays matches using:
  - A **bar chart** of similarity scores
  - A **network graph** showing quantum entanglement potential
- **Live Interface** – Add, update, and view simulated user data interactively.

---

## 🧪 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Quantum Computing**: [Qiskit](https://qiskit.org/)
- **Visualization**: Matplotlib, NetworkX
- **Similarity Metrics**: Scikit-learn's `cosine_similarity`

---

## 💡 Future Ideas

  - Add user login and cookies for real-time participation.
  - Export match data and visualizations.
  - Simulate each user's qubit in read time
  - If you have any suggestions message the dev team on github!

## License
This project is licensed under the terms of the MIT license

