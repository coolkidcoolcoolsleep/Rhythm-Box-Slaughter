from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello Flask World'


if __name__ == '__main__':
    app.run()
# import json
# import tensorflow as tf
# from flask import Flask, redirect, url_for, request, render_template, session
# import numpy as np
# import urllib.request
# import cv2
#
# app = Flask(__name__)
#
# # main에서는 index만 보이게
# @app.route('/', methods=['GET'])
# def main():
#     return render_template('index.html')
#
# @app.route('/model', methods=['GET'])
# def model():
#     if request.method == 'GET':
#         # 1. url을 입력으로 받음
#         url = request.args.get('url')
#         # 2. url을 이미지로 변환
#         image = url_to_image(url)
#         # 3. keras 모델의 input으로 사용
#         result_file = test_model(image)
#         # 4. json 형태로 리턴
#         result_dict = {'url' : url, 'result' : encode_image(result_file)}
#
#     return json.dumps(result_dict)
#
#
# def url_to_image(url):
#     resp = urllib.request.urlopen(url)
#     image = np.asarray(bytearray(resp.read()), dtype="uint8")
#     image = cv2.imdecode(image, cv2.IMREAD_COLOR)
#
#     return image
#
#
# model = load_model('./model_complete.h5', custom_objects={'tf': tf})
# model.load_weights('./model_weights.h5')
# model._make_predict_function()  # predict 할 때 매번 쓰기 위해 사용하는 함수
#
#
# def test_model(image):
#     output = model.predict(image)
#
#     filename = 'temp.png'
#     cv2.imwrite(filename, image)
#
#     return filename
#
# result_dict = {'url' : url, 'result' : encode_image(result_file)}
#
# return json.dumps(result_dict)