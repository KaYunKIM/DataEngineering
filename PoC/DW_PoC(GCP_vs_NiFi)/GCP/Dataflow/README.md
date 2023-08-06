# Dataflow란?

- Serverless
- Fast
- Cost-Effective
- Stream/Batch





=> 많은 데이터(GB/TB)를 가져와서 데이터끼리 결합하여 의미 있는 데이터를 산출하는 과정.(배치)

=> 스트리밍 변환은 데이터가 도착할때 추가적인 데이터와 함께 반환하거나, Filter 를 거쳐서 해당 데이터만 반환하는 특징.



# Apache Beam이란?

이러한 로직들을 구현하게 도와주는것이 Apache Beam.

그래서 Apache Beam으로 데이터 파이프라인을 구축하는 방법에 대해 알아야 한다.

Apache Beam에서 파이프라인은 상위 컨테이너(파이프라인)를 통해 흘러가는 데이터(Pcollection)가 존재하게 되는데 흘러가는 데이터를 조작하는 과정으로 변환(PTransform)을 수행.



----



파이프라인은 DAG(Directed Acyclic Graph)의 형태로 이루어짐. 

즉, 노드와 에지가 서로 반복하거나 순환할 수 없는 구조.

⇒ PCollection을 생성하면 중간 부분만 따로 빼올 수 없기 때문에 개별 항목이 아닌 순차적인 흐름으로 이루어짐



PCollection은 한정되어 있을 수도 있고 그렇지 않을 수도 있다.

Streaming 데이터의 경우 한정되지 않음.

⇒ publisher가 topic에 message를 계속 던져주게 되므로 PCollection 자체는 변경할 수 없는 특성 있음.



PTransform을 수행할때 입출력을 둘 이상을 가질 수 있다.

**join 변환** -> 두 개의 PCollection을 입력으로 사용해 새로운 PCollection 출력

**split 변환** -> 하나의 PCollection을 입력으로 취해 두 개의 개별 PCollection을 출력



------



Pipeline은 몇 개의 step으로 이루어짐:

- reading (Data Source => PCollection1)
- Transforming (Transform => PCollection2)
- writing (PCollectionN => Data Sink )



Data는 P(Parallel)Collection의 형태로 각 단계를 통과함.

- 실시간이라면 unbounded data: 데이터의 수가 정해져 있지 않고, 계속해서 추가되어 끊임 없이 흘러들어오는 데이터
- 배치라면 bounded: 데이터가 정해지지 않고, 변경이 없는 형태로 유지



1. Make Pipeline using **Apache Beam** SDK
2. Use Dataflow to **deploy** and **execute** the pipeline  => Dataflow Job
3. Assign workers(virtual machines) to **execute data processing** => Autoscale



Dataflow는 분석, 예측, DW 등과 같이 실시간과 배치 주기의 데이터 흐름이 필요한 곳 어디에서도 활용 가능함.