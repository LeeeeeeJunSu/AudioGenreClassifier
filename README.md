> # AudioGenreClassifier
>> ## 2. File 별 설명
>> - Run.py : 프로그램 실행 파일
>> - Module/Classifier.py : 분류기에 대한 구현
>> - Module/FeatureExtractor.py : 특징 추출기에 대한 구현
>> - Module/Util.py : Run.py에서 사용되는 유틸리티 함수들에 대한 구현
>> - Module/Define.py : 프로그램에서 사용되는 상수들에 대한 정의
>> ## 3. 특징 추출기
>> ## 4. 분류기
>> ## 5. Run.py 실행 방법
>> ## 6. To do
>> - README.md 작성
>> - 각 파일 별 주석 정리
>> - Requirement.txt 작성
>> - MFCC, OSC Class를 FeatureExtraction로 통합
>>>> - FeatureExtraction에서 Feature Selection을 결정할 수 있도록 변경
>>>> - FeatureExtraction에서 MFCC, OSC 진행 시 필요한 파라미터를 설정 하는 함수 추가
>>>> - FeatureExtraction에서 extract 함수 진행 시 Feature Selection에 따라 다른 피처를 추출하도록 변경
>>>> - FeatureExtraction에서 extract 함수 반환 값은 dictionary로 변경 ({MFCC: [], OSC: []} 형태)
>> - 각 단계 별 시각화 및 시각화 저장 추가
>> - 진행 상황 출력 추가