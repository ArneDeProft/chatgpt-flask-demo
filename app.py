import requests
# import openai
import json
from flask import Flask, render_template, request, jsonify, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# openai.api_key = os.environ["OPENAI_API_KEY"]
# openai.api_base =  os.environ["OPENAI_API_BASE"] # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/

deployment_id = "chatgpt"
url = os.environ["OPENAI_API_BASE"] + "/openai/deployments/" + deployment_id + "/completions?api-version=2023-03-15-preview" 

def askgpt(question):
    session['chat_log'].append({'role': 'user', 'content': question})
    response = openai.ChatCompletion.create(engine=deployment_id, messages=session['chat_log'])
    answer = response.choices[0]['message']['content']
    session['chat_log'].append({'role': 'assistant', 'content': answer})
    session.modified = True
    return  answer

def askgptAPI(question):
    r = requests.post(url, 
      headers={
        "api-key": os.environ["OPENAI_API_KEY"],
        "Content-Type": "application/json"
      },
      json = question
    )
    print(json)

    response = json.loads(r.text)
    formatted_response = json.dumps(response, indent=4) 
    print(formatted_response)
    return formatted_response


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def get_response_from_api():
    print(request.data, flush=True)
    rq = json.loads(request.data)
    message = rq["prompt"]
    print("message:" + message)
    answer = askgptAPI(message)
    print (answer)
    response = {"response":answer}
    return response
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)
