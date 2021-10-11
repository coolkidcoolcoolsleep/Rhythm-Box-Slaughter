import flask
import tensorflow as tf
import keras
from keras.models import load_model


# flask 객체
app = Flask(__name__)


# flask router 설정
@app.route("/")
@app.route("/ball")  # 접속 ip혹은 도메인 뒤 붙는 라우터 이름
# def predict():
#     test_datagen = ImageDataGenerator(rescale=1. / 255)
#     test_generator = test_datagen.flow_from_directory("/이미지 경로/exam", target_size=(100, 100), batch_size=100,
#                                                       class_mode='categorical')
#     # 모델 로드
#     new_model = keras.models.load_model('model.h5')
#     new_model.summary()
#     loss, acc = new_model.evaluate_generator(test_generator, steps=5)
#     data = {"success": False}  # dictionary 형태의 데이터를 만들어 놓고 (딕셔너리에 데이터 넣는 방법1 : dictionary_name = {key:value})
#
#     data["loss_accuracy"] = acc  # 호출한 모델의 정확도를 넣습니다. (딕셔너리에 데이터 넣는 방법2 : dictionary_name[key] = value)
#
#     data["success"] = True  # 같은 방식으로 가지고 있는 key의 value를 바꿀수 있습니다.
#
#     return jsonify(str(acc))  # '/exam'으로 요청을 보낸곳으로 값을 반환하는데에 json형태로 만들어 보내는데 jsonify를 하려면 데이터가 str 형태여야 합니다.
#     return flask.render_template('index.html')



# 볼 구분 모델
# @app.route('/ball', methods=['POST'])
# def make_prediction():
#     if request.method == 'POST':
#
#         # 업로드 파일 처리 분기
#         file = request.files['image']
#         if not file: return render_template('index.html', label="No Files")
#
#         # 이미지 픽셀 정보 읽기
#         # 알파 채널 값 제거 후 1차원 Reshape
#         img = misc.imread(file)
#         img = img[:, :, :3]
#         img = img.reshape(1, -1)
#
#         # 입력 받은 이미지 예측
#         prediction = model.predict(img)
#
#         # 예측 값을 1차원 배열로부터 확인 가능한 문자열로 변환
#         label = str(np.squeeze(prediction))
#
#         # 숫자가 10일 경우 0으로 처리
#         if label == '10': label = '0'
#
#         # 결과 리턴
#         return render_template('index.html', label=label)

# 서버 실행
if __name__ == '__main__':
    # terminal에서 python 인터프리터로 .py 파일을 실행하면 무조건 이 부분을 찾아 실행합니다.
    print(("* Loading Keras model and Flask starting server...",
           "please wait until server has fully started"))

    # 모델 로드
    # model.py 선 실행 후 생성
    model = joblib.load('model/model.h5')

    # Flask 서비스 스타트(app.run -> flask 서버 구동)
    # host="0.0.0.0"은 외부에서 해당 서버 ip 주소 접근이 가능하도록 하는 옵션
    app.run(host='0.0.0.0', port=8000, debug=True)
