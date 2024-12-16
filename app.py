import streamlit as st
import boto3
import json
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수에서 설정 가져오기
AWS_REGION = os.getenv('AWS_REGION', '')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
DEFAULT_KNOWLEDGE_BASE_ID = os.getenv('KNOWLEDGE_BASE_ID', '')

# 클라이언트 생성 전 인증 정보 확인
if not all([AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY]):
    st.error("AWS 인증 정보가 올바르게 설정되지 않았습니다. .env 파일을 확인해주세요.")
    st.stop()

# Bedrock 클라이언트 설정
bedrock = boto3.client(
    service_name='bedrock-agent-runtime',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# 페이지 설정
st.set_page_config(
    page_title="Bedrock Knowledge Base Q&A",
    page_icon="🤖",
    layout="wide"
)

# CSS 스타일 적용
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 메인 타이틀
st.title("🤖 Bedrock Knowledge Base Q&A")

# 사이드바 설정
with st.sidebar:
    st.header("설정")
    knowledge_base_id = st.text_input(
        "Knowledge Base ID",
        value=DEFAULT_KNOWLEDGE_BASE_ID,
        help="사용할 Knowledge Base의 ID를 입력하세요"
    )

# 메인 컨테이너
main_container = st.container()

with main_container:
    # 사용자 입력
    user_question = st.text_input(
        "질문을 입력하세요:",
        placeholder="궁금한 내용을 입력해주세요..."
    )

    # 답변 생성 버튼
    if st.button("답변 받기", key="generate"):
        if user_question and knowledge_base_id:
            with st.spinner("답변을 생성하고 있습니다..."):
                try:
                    # Bedrock Knowledge Base API 호출
                    response = bedrock.retrieve_and_generate(
                        input={
                            'text': user_question
                        },
                        retrieveAndGenerateConfiguration={
                            'type': 'KNOWLEDGE_BASE',
                            'knowledgeBaseConfiguration': {
                                'knowledgeBaseId': knowledge_base_id,
                                'modelArn': f'arn:aws:bedrock:{AWS_REGION}::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0'
                            }
                        }
                    )

                    # 답변 표시
                    st.markdown("### 답변")
                    answer = response['output']['text']
                    st.write(answer)

                    # 참고 문서 표시
                    if 'citations' in response:
                        st.markdown("### 참고 문서")
                        for idx, citation in enumerate(response['citations'], 1):
                            with st.expander(f"참고 문서 {idx}"):
                                st.markdown(f"**내용:**\n{citation['content']}")
                                st.markdown(f"**출처:** {citation['location']}")

                except Exception as e:
                    st.error(f"오류가 발생했습니다: {str(e)}")
        else:
            st.warning("질문과 Knowledge Base ID를 모두 입력해주세요.")

    # 히스토리 표시
    if st.session_state.get('history'):
        st.markdown("### 이전 대화")
        for q, a in st.session_state.history:
            st.text(f"Q: {q}")
            st.text(f"A: {a}")
            st.markdown("---")
