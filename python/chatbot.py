import os
import torch
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain_text_splitters import KonlpyTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
import logging

def question_and_answer(full_text: str, question: str) -> str:
    # 1. API 키 설정
    load_dotenv()
    google_api_key = os.getenv("GOOGLE_API_KEY")
    hf_token = os.getenv("HF_TOKEN")
    if not google_api_key:
        # GOOGLE_API_KEY가 존재하지 않을 시 ValueError 예외 강제 발생
        raise ValueError("⛔ 오류 : GOOGLE_API_KEY가 .env 파일에 설정되지 않음")
    if not hf_token:
        # HF_TOKEN이 존재하지 않을시 ValueError 예외 강제 발생
        raise ValueError("⛔ 오류 : HF_TOKEN .env 파일에 설정되지 않음")

    # 2. 텍스트 분할 (Indexing)
    text_splitter = KonlpyTextSplitter()
    input = Document(page_content=full_text) # 문자열을 Document 객체로 변환
    docs = text_splitter.split_documents([input])
    logging.info(f"문서가 {len(docs)}개의 문장(조각)으로 분할 성공.")

    # 3. 임베딩 모델 준비 (HuggingFace)
    model_name = "nlpai-lab/KURE-v1"

    # NVIDIA GPU가 사용 가능하면 'cuda', 그렇지 않으면 'cpu'
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    logging.info(f"임베딩을 위해 사용하는 디바이스: {device}")

    # HuggingFaceEmbeddings 객체 생성
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': device},
        encode_kwargs={'normalize_embeddings': True}  # 벡터를 정규화하여 성능 향상
    )

    # 4. 벡터화 및 ChromaDB에 저장
    vectorstore = Chroma.from_documents(docs, embeddings)
    logging.info("ChromaDB 메모리 저장 완료")

    # 5. RAG 체인 생성
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, convert_system_message_to_human=True)
    retriever = vectorstore.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False
    )

    # 6. 체인 실행 및 결과 반환
    logging.info(f"질문 {question}에 대한 답변 생성 중...")
    result_dict = qa_chain.invoke(question)
    answer = result_dict.get('result', '답변 키를 찾지 못했습니다.')
    logging.info("답변 생성 완료")

    return answer