from swarm import Swarm, Agent
import http.client
import json

client = Swarm()

# Example function (same as yours):
def get_order_status(reference_id: str):
    access_token = "gfmSGQ9uhPssz394P5WLQk8isUjpxNLbxuthuoAJkDE.j5CUYLC7iidYRyT6DCgBv-_IUeY7PYU_wjSnbjew9kE"
    conn = http.client.HTTPSConnection("api.salla.dev")
    payload = ''
    headers = {"Authorization": f"Bearer {access_token}"}
    conn.request("GET", f"/admin/v2/orders?reference_id={reference_id}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

agent_a = Agent(
    name="Agent A",
    instructions="You are a helpful agent. Provide helpful and concise answers.",
    functions=[get_order_status],
)

# We’ll keep the entire conversation in this list.
conversation = [
    # Optionally, you can start with a system or user “context” message.
    {"role": "system", "content": "You are a helpful assistant for checking order statuses."},
]

while True:
    # Get user input
    user_input = input("\nYou: ")
    
    # If user types exit/quit, break out of the loop
    if user_input.lower() in ["quit", "exit"]:
        print("Exiting conversation.")
        break

    # Add user’s new message to the conversation
    conversation.append({"role": "user", "content": user_input})

    # Send conversation so far to Swarm
    response = client.run(agent=agent_a, messages=conversation)
    
    # The agent’s reply is the last message
    assistant_message = response.messages[-1]["content"]
    
    # Print the agent’s response
    print(f"Agent: {assistant_message}")
    
    # Append the assistant’s response back to conversation history
    conversation.append({"role": "assistant", "content": assistant_message})