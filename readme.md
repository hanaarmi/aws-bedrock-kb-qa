# AWS Bedrock Knowledge Base Q&A

AWS Bedrock Knowledge Base와 Streamlit을 활용한 Q&A 애플리케이션입니다.

## 🚀 Features

- AWS Bedrock Knowledge Base를 활용한 질의응답
- Claude 3.5 Sonnet 모델 기반 응답 생성
- 참고 문서 및 출처 표시
- 대화 히스토리 관리

## 🔧 Prerequisites

- Python 3.12+
- AWS 계정
- OpenSearch Serverless 설정
- AWS Bedrock Knowledge Base 설정

## 📦 Installation

1. 저장소 클론
bash
git clone <repository-url>
cd <repository-name>

2. 의존성 설치
```bash
pipenv install
```

3. 환경 변수 설정
```bash
cp .env.example .env
```
다음 환경 변수를 설정하세요:
- AWS_REGION
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- KNOWLEDGE_BASE_ID

## 🏃‍♂️ Running the Application

```bash
streamlit run app.py
```

## 🔍 OpenSearch Serverless 설정 가이드

### 1. OpenSearch Collection 생성
1. AWS OpenSearch Serverless 콘솔 접속
2. Create Collection 선택
3. Security Configuration
   - "Edit" 선택
   - "Do not set domain level access policy" 선택

### 2. 인덱스 생성
OpenSearch 대시보드에서 Dev Tools를 열고 다음 명령어를 실행:

```json
PUT /saitalab
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 2,
    "knn.space_type": "cosinesimil",
    "knn": "true",
    "analysis": {
      "tokenizer": {
        "nori_user_dict": {
          "type": "nori_tokenizer",
          "decompound_mode": "mixed",
          "user_dictionary_rules": ["형태소", "분석기"]
        }
      },
      "filter": {
        "nori_part_of_speech": {
          "type": "nori_part_of_speech",
          "lowercase": {
            "type": "lowercase"
          }
        }
      },
      "analyzer": {
        "nori_analyzer": {
          "type": "custom",
          "tokenizer": "nori_user_dict",
          "filter": ["lowercase", "nori_part_of_speech"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text"
      },
      "meta": {
        "type": "text"
      },
      "image": {
        "type": "binary"
      },
      "content_vector": {
        "type": "knn_vector",
        "dimension": 1024
      }
    }
  }
}
```

## 📝 License

MIT License

## 👥 Contributors

- Jungkon Kim