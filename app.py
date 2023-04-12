
import requests
import openai
import json
from flask import Flask, render_template, request, jsonify, session
import os


from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain import LLMMathChain
from langchain.utilities import BingSearchAPIWrapper
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import AzureChatOpenAI



os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_KEY"] = "YOUR KEY"
os.environ["OPENAI_API_BASE"] = "https://ENDPOINT.openai.azure.com/"
os.environ["OPENAI_API_VERSION"] = "2023-03-15-preview"
os.environ["LANGCHAIN_HANDLER"] = "langchain"

os.environ["BING_SUBSCRIPTION_KEY"] = "BING KEY"
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


llm = AzureChatOpenAI(
                openai_api_base=os.environ["OPENAI_API_BASE"],
                openai_api_version=os.environ["OPENAI_API_VERSION"],
                deployment_name="chat",
                openai_api_key=os.environ["OPENAI_API_KEY"],
                openai_api_type = "azure",
            ) 

search = BingSearchAPIWrapper()
llm_math_chain = LLMMathChain(llm=llm, verbose=True)

app = Flask(__name__)
app.secret_key = os.urandom(24)


# define a function to calculate nth fibonacci number
def fib(n):
    if n <= 1:
        return n
    else:
        return(fib(n-1) + fib(n-2))

# define a function which sorts the input string alphabetically
def sort_string(string):
    return ''.join(sorted(string))

              
# define a function to turn a word in to an encrypted word
def encrypt(word):
    encrypted_word = ""
    for letter in word:
        encrypted_word += chr(ord(letter) + 1)

    return encrypted_word
# define a function to turn a word in to an decrypted word
# return direct means that the output of the function will be returned after max iterations reached??
def decrypt(word):
    decrypted_word = ""
    for letter in word:

        decrypted_word += chr(ord(letter) - 1)
    return decrypted_word

# return direct means that the output of the function will be returned after max iteration reached??


tools = [
    Tool(
        name = "Fibonacci",
        func= lambda n: str(fib(int(n))),
        description="use when you want to calculate the nth fibonacci number"
        # return_direct=True
    ),
    Tool(
        name = "Sort String",
        func= lambda string: sort_string(string),
        description="use when you want to sort a string alphabetically"
        # return_direct=True
    ),
    Tool(
        name = "Encrypt",
        func= lambda word: encrypt(word),
        description="use when you want to encrypt a word"
        # return_direct=True
    ),
    Tool(
        name = "Decrypt",
        func= lambda word: decrypt(word),
        description="use when you want to decrypt a word"
        # return_direct=True
    ),
    Tool(
        name = "Search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
        # return_direct=True
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math"
        # return_direct=True
    )
    ]





agent_chain = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)





@app.route('/')
def home():
    if 'chat_log' not in session:
        session['chat_log'] = [{
            'role': 'system',
            'content': 'You are an assistant and you will help people answering their questions',
        }]
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def get_response_from_api():
    print(request.data, flush=True)
    rq = json.loads(request.data)
    message = rq["message"]
    
    answer = agent_chain.run(input=message)
    response = {"response":answer}
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)

