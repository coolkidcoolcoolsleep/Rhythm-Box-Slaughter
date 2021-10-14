# 리듬박스 학살
웹캠(모바일 디바이스의 카메라)를 활용해 bpm 에 따라 만들어지는 랜덤 리듬 박스에 맞춰서 탁구채를 일치시키는 리듬 게임.

## 브랜치 목록
### random_rhythm_box
랜덤으로 player 숫자, 게임 난이도에 따라 다른 랜덤 리듬 박스를 생성하는 모듈
### develop
multi color detection 기능 개발과 opencv 를 활용해 꾸미기 기능을 만드는 중.
현재까지 png 이미지의 선글라스를 화면에 띄우는 것 진행중
### managers
점수 합산 및 계산, 우승자 선정 모듈을 만드는 폴더. 
지금까지 랜덤 리듬박스와 color detection box 를 같은 화면에 만드는 기능 완성함.
### app/camera_access
앱에서 디바이스의 카메라와 갤러리 접근권한을 얻는 기능을 만듦.
### app/application
비어있는 액티비티: 앱 설계 초기에 만든 프로젝트이나 제대로된 기능이 삽입되어 있지는 않다.


##### 기타
TFlite 의 posenet_estimation 을 실행해보았음
