from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Set the endpoint URLs and your RapidAPI Key
generate_url = "https://arimagesynthesizer.p.rapidapi.com/generate"
get_url = "https://arimagesynthesizer.p.rapidapi.com/get"
rapidapi_key = "YOUR_API_KEY"


@app.route('/')
def index():
  return render_template('image.html')


@app.route('/generate_image', methods=['POST'])
def generate_image():
  data = json.loads(request.data)  # Retrieve JSON data from the request

  text = data.get('text')
  print(text)

  if not text:
    return jsonify({'error': "Text input is empty."})

  # Create a payload for the generate request
  generate_payload = {
    "prompt": text,
    "id": "12345",
    "width": "768",
    "height": "768",
    "inferenceSteps": "50",
    "guidanceScale": "7.5",
    "img2img_strength": "0.75"
  }

  generate_headers = {
    "content-type": "application/x-www-form-urlencoded",
    "X-RapidAPI-Key": rapidapi_key,
    "X-RapidAPI-Host": "arimagesynthesizer.p.rapidapi.com"
  }

  # Send the generate request to get a hash
  generate_response = requests.post(generate_url,
                                    data=generate_payload,
                                    headers=generate_headers)
  generate_data = generate_response.json()
  print(generate_data)

  if 'hash' in generate_data:
    hash_value = generate_data['hash']

    # Create a payload for the get request using the obtained hash
    get_payload = {"hash": hash_value, "returnType": "image"}

    get_headers = {
      "X-RapidAPI-Key": rapidapi_key,
      "X-RapidAPI-Host": "arimagesynthesizer.p.rapidapi.com"
    }

    # Send the get request to fetch the image
    get_response = requests.get(get_url,
                                headers=get_headers,
                                params=get_payload)

    if get_response.status_code == 200:
      image_data = get_response.content
      image_file_name = "image.png"  # You can customize the file name
      with open(image_file_name, "wb") as image_file:
        image_file.write(image_data)
      return jsonify({'image_url': get_response.url})
    else:
      return jsonify({'error': "Failed to fetch the image."})
  else:
    return jsonify(
      {'error': "Failed to generate a hash for the given prompt."})


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
