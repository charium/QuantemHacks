#Encodes quantum states based on user info
#We should look more itno this to figure out what it's actually doing lol

from qiskit import QuantumCircuit
import numpy as np

def encode_user(user):
    circuit = QuantumCircuit(1)
    theta = np.pi * len(user["interests"]) / 10
    phi = np.pi * (sum(user["location"]) / 360)

    circuit.ry(theta, 0)
    circuit.rz(phi, 0)
    return circuit