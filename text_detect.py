import io
from google.cloud import vision

client=vision.ImageAnnotatorClient()

#추후에 predict 함수와 합쳐서(정보 취합한뒤 db에서 정보 가져오는 방식으로
def detect_text(input_image):
    image=vision.Image(content=input_image)
    response=client.text_detection(image=image)
    texts=response.text_annotations
    print("texts: ")
    for text in texts:
        print(text.description)


