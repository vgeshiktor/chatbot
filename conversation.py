from utils import get_openai_api_key
from autogen import ConversableAgent

OPENAI_API_KEY = get_openai_api_key()
llm_config = {"model": "text-davinci-003"}

agent = ConversableAgent(
    name="chatbot",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

reply = agent.generate_reply(messages=[{"content": "Tell me a joke.", "role": "user"}])
print(reply)
