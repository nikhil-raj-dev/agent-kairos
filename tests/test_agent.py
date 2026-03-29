import sys
sys.path.append('../')
from app.agent.agent import run_agent

print("\n--- Agent-Kairos ---\n")

while True:
    query = input("You: ")

    if query.lower() == "exit":
        break

    response = run_agent(query)

    print("\nAgent-Kairos:", response, "\n")