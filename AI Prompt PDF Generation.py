from flask import Flask, render_template, request, jsonify
from hugchat import hugchat
from hugchat.login import Login
import os

app = Flask(__name__)

email = os.environ['email']
passwd = os.environ['passwd']

try:
  sign = Login(email, None)
  cookies = sign.loadCookiesFromDir("./cookies_snapshot")
except:
  sign = Login(email, passwd)
  cookies = sign.login()
  sign.saveCookiesToDir("./cookies_snapshot")

# Create a ChatBot instance
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())


@app.route('/')
def index():
  return render_template('index3.html')


@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
  prompt = request.form.get('prompt')

  query_result = chatbot.query(prompt)

  response_text = query_result["text"]

  formatted_response = format_response(response_text)

  return jsonify({'response_text': formatted_response})


def format_response(text):
  lines = text.split('\n')
  formatted_lines = []

  is_list = False
  list_item_count = 0

  for line in lines:
    # Check if it's a list item (e.g., "1. This is an item")
    if line.strip().startswith(('#', '*', '-', '1.', '2.', '3.')):
      is_list = True
      list_item_count += 1
      formatted_lines.append(
        f'<div style="text-align: right; margin-right: 10px;">{list_item_count}.</div> {line}'
      )
    elif is_list:
      formatted_lines.append(
        f'<div style="text-align: right; margin-right: 10px;"></div> {line}')
    else:
      formatted_lines.append(f'<h3>{line}</h3>')

  formatted_response = '\n'.join(formatted_lines)
  return formatted_response


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
