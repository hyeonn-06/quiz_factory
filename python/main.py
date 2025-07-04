import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from extract_text import extract_text_from_pdf
from create_quiz import create_quiz_with_gemini
from utils import format_quizzes_to_string
from chatbot import question_and_answer

# logging 설정
logging.basicConfig(level=logging.INFO)

# FastAPI 앱 인스턴스 생성
app = FastAPI(
    title="퀴즈 공장 API 서버",
    description="PDF 파일을 받아 텍스트를 추출하고 퀴즈를 생성하는 API입니다.",
    version="1.0.0",
)

vector_store_cache = {}

# ----- 요청 모델 정의 (퀴즈 출제) -----
class QuizRequest(BaseModel):
    input_file_path: str
    difficulty : str
    num_quiz : int

# -----요청 모델 정의 (챗봇) -----
class ChatBotRequest(BaseModel):
  input_file_path: str
  question : str
  member_id : str

# ----- 응답 모델 정의 (퀴즈 출제) -----
class QuizResponse(BaseModel):
    quizzes : str

# ----- 응답 모델 정의 (챗봇) -----
class ChatBotResponse(BaseModel) :
    answer : str

@app.post("/api/quiz", response_model=QuizResponse)
async def api_quiz(request_data: QuizRequest):
    logging.info("--- 퀴즈 출제 시작 ---")
    input_file_path = request_data.input_file_path # pdf 파일 경로
    difficulty = request_data.difficulty # 난이도
    num_quiz = request_data.num_quiz # 출제 퀴즈 수

    # pdf 파일에서 텍스트 추출
    full_text = extract_text_from_pdf(input_file_path)

    # 추출한 텍스트를 통해 퀴즈 데이터 생성 (dict 타입)
    quiz_data = create_quiz_with_gemini(full_text, num_quiz, difficulty)

    # 퀴즈 데이터를 문자열로 변환
    quizzes = format_quizzes_to_string(quiz_data)

    return QuizResponse(quizzes=quizzes)

@app.post("/api/chatbot", response_model=ChatBotResponse)
async def api_chatbot(request_data: ChatBotRequest):
    logging.info("--- 챗봇 시작 ---")
    input_file_path = request_data.input_file_path # pdf 파일 경로
    question = request_data.question # 질문
    member_id = request_data.member_id # 질문한 사용자 ID

    try :
        # 해당 사용자의 기존 캐시가 있다면 삭제 후 vector DB 생성
        if member_id in vector_store_cache:
            logging.info(f"기존 캐시 발견 : {member_id}에 대한 기존 Vector DB 삭제")
            del vector_store_cache[member_id]

        logging.info(f"--- {member_id}를 위한 새로운 Vector DB 생성 시작 ---")

        # pdf 파일에서 텍스트 추출
        full_text = extract_text_from_pdf(input_file_path)

        # RAG 시스템을 통한 질의 응답
        answer = question_and_answer(full_text, question)
        logging.info(f"성공적으로 답변 생성 완료: {answer[:50]}...")
        return ChatBotResponse(answer=answer)

    except Exception as e:
        logging.error(f"⛔ 오류 : 챗봇 과정 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="챗봇 서버 내부 오류 발생")
