import requests

# initialize the Keras REST API endpoint URL along with the input
# image path
KERAS_REST_API_URL = "http://5a3099998dca.ngrok.io/predict"     #주소 바꿔주기
IMAGE_PATH = "IMG_3495.JPG"
# load the input image and construct the payload for the request
image = open(IMAGE_PATH, "rb").read()
payload = {"photo": image}

# post 요청 보냄 
r = requests.post(KERAS_REST_API_URL, files=payload).json()

# ensure the request was sucessful
if r["success"]:
	print(r["content"])

# otherwise, the request failed
else:
    print("Request failed")