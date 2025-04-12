value = 5

def run_i_survey():
    interest_questions = [
        "a1. How interested are you in quantum computing? (1-5)",
        "a2. Have you read any articles or books about quantum computing? (1-5)",
        "a3. Do you follow quantum computing news or research? (1-5)",
        "a4. Do you plan to pursue a career involving quantum computing? (1-5)",
        "a5. Are you interested in the theoretical foundations of quantum computing? (1-5)",
    ]

    i_responses = {}

     # Ask interest questions
    for question in interest_questions:
        answer = input(question + " ")
        i_responses[question] = answer

    return i_responses

def run_e_survey():
    experience_questions = [
        "b1. Have you used Qiskit or any quantum computing framework in Python? (1-5)",
        "b2. Can you write a basic quantum circuit using Python? (1-5)",
        "b3. Have you ever simulated a quantum circuit using Python? (1-5)",
        "b4. Have you used IBM Quantum Lab or any cloud quantum services? (1-5)",
        "b5. Do you understand the basics of Python required for quantum programming? (1-5)",
    ]

    e_responses = {}


    # Ask experience questions
    for question in experience_questions:
        answer = input(question + " ")
        e_responses[question] = answer

    return e_responses

def quantify_traits(i_responses, e_responses):
    """
    Function to quantify the interest and experience traits based on survey responses.
    """
    i_score = sum(int(a) for a in i_responses.values()) / len(i_responses)
    i_score = i_score/value 
    e_score = sum(int(a) for a in e_responses.values()) / len(e_responses)
    e_score = e_score/value 

    print(f"\nInterest Score: {i_score:.2f}")
    print(f"Experience Score: {e_score:.2f}")
    return i_score, e_score

user_data = {}

# Number of users you want to enter
num_users = int(input("How many users? "))

for _ in range(num_users):
    intrest = float(0.00)
    expereince = float(0.00)

    print("==== Quantum Computing Survey ====\n")

    name = input("What is your name? ")
    
    intrest = run_i_survey()
    experience = run_e_survey()
    i_score, e_score = quantify_traits(intrest, experience)

    print("\nThank you for completing the survey!")
    print(intrest, experience)
    user_data[name] = {
        "interest": i_score,
        "experience": e_score
    }

print("\nCollected Data:")
for name, values in user_data.items():
    print(f"{name}: Interest = {values['interest']}, Experience = {values['experience']}")
