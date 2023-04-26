import requests
# import openai
import json
from flask import Flask, render_template, request, jsonify, session
import os

global accesstoken = "empty"

app = Flask(__name__)
app.secret_key = os.urandom(24)

print(os.environ["OPENAI_API_KEY"])
print(os.environ["OPENAI_API_BASE"]) # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/

deployment_id = "chatgpt"
url = os.environ["OPENAI_API_BASE"] + "/openai/deployments/" + deployment_id + "/chat/completions?api-version=2023-03-15-preview" 
print(url)
def askgpt(question):
    session['chat_log'].append({'role': 'user', 'content': question})
    response = openai.ChatCompletion.create(engine=deployment_id, messages=session['chat_log'])
    answer = response.choices[0]['message']['content']
    session['chat_log'].append({'role': 'assistant', 'content': answer})
    session.modified = True
    return  answer

def askgptAPI(question):
    print("q")
    print(question)
    r = requests.post(url, 
      headers={
        "api-key": os.environ["OPENAI_API_KEY"],
        "Content-Type": "application/json"
      },
      json = question
    )
    print(json)

    response = json.loads(r.text)
    print(response)
    return response


@app.route('/')
def home():
    accesstoken = request.headers.get('x-ms-token-aad-access-token')
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def get_response_from_api():
    print(request.data, flush=True)
    rq = json.loads(request.data)
    message = rq["prompt"]
    payload = '{"messages":[{"role": "system", "content": "'+ message+'"}]}'
    payload = json.loads(payload)
    print("message:" + message)
    print(payload)
    answer = askgptAPI(payload)
    answer = answer["choices"][0]["message"]["content"]
    print (answer)
    response = {"response":answer}
    return response
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)
