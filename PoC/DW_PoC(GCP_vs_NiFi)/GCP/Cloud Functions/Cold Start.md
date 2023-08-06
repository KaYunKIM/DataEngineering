# Cloud Functions cold start 문제

👉  https://stalker5217.github.io/cloud/coldStart/



## 1. Cloud Functions = Severless fuction

- 즉,  Auto Scaling으로 트래픽에 맞는 인스턴스 수를 조정하여 함수 제공





## 2. GCP Cloud Functions의 인스턴스 시작 조건:

- 함수 배포하는 경우
- 트래픽 처리 위해 인스턴스 확장/대체의 경우





## 3. GCP Cloud Functions cold start

- 새로운 인스턴스가 시작되면 내부에서 함수가 실행될 수 있도록 소스 코드 로드와 같은 여러가지 환경을 구성하는 작업을 수행함.
- 따라서, 인스턴스 처음 호출 시, 느리게 동작하는 문제 발생!





## 4. Functions Optimization

⇒ 함수 동작 시간을 줄이기 위한 최적화 방법

- 불필요한 dependency 제거
- Global variable을 사용한 재사용
- Lazy Initialization(실제 해당 객체 사용 시 초기화)
- Keep Alive
