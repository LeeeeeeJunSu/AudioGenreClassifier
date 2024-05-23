> # AudioGenreClassifier
>> ## 1. File 별 설명
>> - Run.py : 프로그램 실행 파일
>> - Module/Classifier.py : 분류기에 대한 구현
>> - Module/FeatureExtractor.py : 특징 추출기에 대한 구현
>> - Module/Util.py : Run.py에서 사용되는 유틸리티 함수들에 대한 구현
>> - Module/Define.py : 프로그램에서 사용되는 상수들에 대한 정의
>> ## 2. 특징 추출기
>>>> ### 2.1. MFCC
>>>> ### 2.2. OSC
>> ## 3. 분류기
>>>> ### 3.1. 영향력이 가장 큰 특징을 기준으로 분류
>>>> ### 3.2. SVM을 이용한 분류
>> ## 4. Run.py 실행 방법
>> - Terminal에서 pip install -r requirements.txt 실행
>> - 초기 실행 시 Run.py의 startProcess 변수를 Define.Process.DATA_COLLECTION으로 변경
>> - Terminal에서 python Run.py 실행
>> ## 5. To do
>> - 데이터 수집 단계 검증
>> - 각 단계 별 시각화 및 시각화 저장 추가
>> - MFCC, OSC Class를 FeatureExtraction로 통합
>>>> - FeatureExtraction에서 Feature Selection을 결정할 수 있도록 변경
>>>> - FeatureExtraction에서 MFCC, OSC 진행 시 필요한 파라미터를 설정 하는 함수 추가
>>>> - FeatureExtraction에서 extract 함수 진행 시 Feature Selection에 따라 다른 피처를 추출하도록 변경
>>>> - FeatureExtraction에서 extract 함수 반환 값은 dictionary로 변경 ({MFCC: [], OSC: []} 형태)