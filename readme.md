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
```bash
git clone <repository-url>
cd <repository-name>
```

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

## 📝 License

MIT License

## 👥 Contributors

- Jungkon Kim