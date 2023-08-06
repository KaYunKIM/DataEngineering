Airflow DAG의 Record Count가 계속해서 누적됨에 따라 

DAG run 개수를 조절하기 위한 코드 개발 및 배치용 DAG 생성

- 주기: 한 달(31일)

- 매일 배치로 돌면서 최근 31일을 제외한 나머지 dag run 삭제

  => DB log 저장 용량 최적화 