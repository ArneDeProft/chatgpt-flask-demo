import requests
import openai
import json
from flask import Flask, render_template, request, jsonify, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

print(os.environ["OPENAI_API_KEY"])
print(os.environ["OPENAI_API_BASE"])

openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_base =  os.environ["OPENAI_API_BASE"] # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/

openai.api_type = 'azure'
openai.api_version = "2023-03-15-preview"

deployment_id = "chat"
def get_response(prompt):
    print("PROMPT"+prompt,flush=True)
    completion=openai.Completion.create(
        engine=deployment_id,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.6,
    )
    message=completion.choices[0].text
    print("MESSAGE:"+message,flush=True)
    return message
def askgpt(question):
    session['chat_log'].append({'role': 'user', 'content': question})
    response = openai.ChatCompletion.create(engine='chat', messages=session['chat_log'])
    answer = response.choices[0]['message']['content']
    session['chat_log'].append({'role': 'assistant', 'content': answer})
    session.modified = True
    return  answer
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
    #answer = get_response(message)
    answer = askgpt(message)
    response = {"response":answer}
    return response
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)
