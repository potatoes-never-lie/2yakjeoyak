import tensorflow as tf     
import numpy as np
import flask
import io
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image
import cv2
from call_openAPI import get_JSON
import dbconn
import base64
import json

app=flask.Flask(__name__)
model=None
kernel=np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
CLASSES=['네렉손서방정','레보트라정','리보테인정','바로소펜','베포탄정','벤즈날정', '비타포린정', '소론도정', '스틸녹스정', '쎄락틸정', '알레그라정180', '위싹정', '티지피파모티딘정', '페니라민정', '후라시닐정']
#client=vision.ImageAnnotatorClient()

def load_model():
	global model
	model = tf.keras.models.load_model('my_model.h5',compile = True)

def apply_sharpfilter(image):				#Apply sharp filter before OCR
	image=cv2.resize(image, dsize=(224,224), interpolation=cv2.INTER_LINEAR)
	image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	return cv2.filter2D(image, -1, kernel)

def prepare_image(image, target):
	image=image.resize(target)
	image=img_to_array(image)
	image=np.expand_dims(image, axis=0)
	image=preprocess_input(image)
	return image
	
@app.route("/search", methods=["GET"])			#직접 검색 모듈(일반의약품만 가능)
def search():
	data={}
	#arglist=("name","formulation","imprint_front","imprint_back","shape","color")
	name="name!=\'0\'" if flask.request.args["name"]=='0' else "name like \'%%{}%%\'".format(flask.request.args["name"]) 
	formulation="formulation!=\'0\'" if flask.request.args["formulation"]=='0' else "formulation=\'{}\'".format(flask.request.args["formulation"]) 
	imprint_front="imprint_front!=\'0\'" if flask.request.args["imprint_front"]=='0' else "imprint_front like \'%%{}%%\'".format(flask.request.args["imprint_front"])
	imprint_back="imprint_back!=\'0\'" if flask.request.args["imprint_back"]=='0' else "imprint_back like \'%%{}%%\'".format(flask.request.args["imprint_back"])
	shape="shape!=\'0\'" if flask.request.args["shape"]=='0' else "shape=\'{}\'".format(flask.request.args["shape"])
	color="color!=\'0\'" if flask.request.args["color"]=='0' else "color=\'{}\'".format(flask.request.args["color"])
	sql="SELECT name FROM pilldb.id_pill where {} and {} and {} and {} and {} and {} and genorpro='일반의약품';".format(name, formulation, imprint_front, imprint_back, shape, color)
	row=db_class.executeAll(sql)
	data["success"]=True
	data["content"]=[]		
	for i in row:
		print(i["name"])
		c=get_JSON(i["name"])
		data["content"].append(c) if c is not None else None
	return flask.jsonify(data)

#전달 방식 예시: curl -G     --data-urlencode "name=후라시닐정"   --data-urlencode "formulation=0"  --data-urlencode "imprint_front=0" --data-urlencode "imprint_back=0" --data-urlencode "shape=0" --data-urlencode "color=하양"  http://127.0.0.1:5000/search


@app.route("/predict", methods=["POST"])#사진으로 검색하면 추론해서 정보 돌려주는 모듈
def predict():
	data={}
	data["success"]=False
	if flask.request.method=="POST":
		if flask.request.json['photo']:
			image=Image.open(io.BytesIO(base64.b64decode(flask.request.json['photo'])))
			image=prepare_image(image, target=(224,224))
			preds=model.predict(image)
			inferred_name=CLASSES[np.argmax(preds)]
			data["content"]=get_JSON(inferred_name)
			data["success"]=True
		'''
		if flask.request.files.get("photo"):
			image=flask.request.files["photo"].read()
			image=Image.open(io.BytesIO(image))
			#inferred_text=detect_text(image)			#text로 하는건 일단 보류!!!!!
			image=prepare_image(image, target=(224,224))
			preds=model.predict(image)
			inferred_name=CLASSES[np.argmax(preds)]
			data["content"]=get_JSON(inferred_name)
			data["success"]=True
		'''
	return flask.jsonify(data)

if __name__=="__main__":
	print("* Loading keras model and Flask starting server..Please wait until server has fully started..")
	db_class=dbconn.Database()
	load_model()
	app.run()

#(echo -n '{"photo": "'; base64 /Users/chaeyeon/Documents/2yakjeoyak/venv/IMG_3495.JPG; echo '"}') | curl -H "Content-Type: application/json" -d @-  http://afd35fd7429d.ngrok.io/predict
'''
curl -G \
    --data-urlencode "name='위싹정'" \
    --data-urlencode "shape='장방형'" \
    http://127.0.0.1:5000/search
'''