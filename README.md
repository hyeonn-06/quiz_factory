## 대한민국 청년 정책 AI Agent

- 프로젝트 기간: 2025/5/26 ~ 2025/6/11
- 참여 인원: 김도현, 백윤지, 박병건, 지세하, 최도경

## 담당 모듈

- **김도현 (Spring Boot, React)**
    - 회원 관리 및 권한 처리(JWT)
    - 서버 연결 관리
    - 프론트엔드 로그인 상태 관리
- **백윤지 (Python, Spring Boot, React)**
    - RAG 시스템 및 API 서버 구축
    - 공지사항 게시판 기능 및 아키텍처
    - 정책 목록&검색 기능 및 아키텍처
- **박병건 (Spring Boot)**
    - RDB 설계 및 구축
    - Q&A 게시판 기능
- **지세하 (React)**
    - 프론트엔드 UI/UX 개발
    - UI/UX 공통 컴포넌트 개발
- **최도경 (Python)**
    - 데이터 수집 및 정제 파이프라인

---

# **⚙️** 설치 및 실행 방법

## Backend (Python - SpringBoot)

### 1. 저장소 복제

Sourcetree와 같은 GUI 프로그램을 사용 중이라면 해당 프로그램을 이용하여 저장소를 복제하세요.

```bash
# 1. 원격 저장소를 로컬에 복제합니다.
git https://github.com/hyeonn-06/ezen_project_helper.git
# 2. clone으로 생성된 프로젝트 폴더로 이동합니다.
cd ezen_project_helper
```

### 2. 가상 환경 설정

RAG, LLM 시스템을 구동하기 위해 독립적인 파이썬 가상 환경을 설정합니다.

※ PyCharm으로 실행한다면 해당 과정을 단축 시킬 수 있습니다.

```powershell
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 필요 패키지 설치

아래 requirements.txt 파일을 프로젝트 루트 디렉토리에 생성하고 내용을 붙여넣은 뒤, 다음 명령어로 한 번에 설치합니다.

※ PyCharm을 이용한다면 [ 파일-설정-Python 인터프리터 ] 기능을 통해 설치할 수 있습니다.

```
# requirements.txt

# Web Framework
fastapi
uvicorn[standard]

# RAG & LLM Core (LangChain)
langchain
langchain-community
langchain-google-genai
langchain-huggingface
langchain-text-splitters

# Embedding
sentence-transformers

# VectorDB
chromadb

# NLP & Utilities
konlpy
python-dotenv
pydantic-settings
filelock

# Deep Learning Framework (for HuggingFace Embeddings)
torch

# Web Crawling & RDB
bs4
oracledb
```

```powershell
# 설치 명령어
pip install -r requirements.txt
```

### 4. 환경 변수 설정

프로젝트 루트 디렉토리에 .env 파일을 생성하고 아래와 같이 API 키를 입력합니다.

```python
GOOGLE_API_KEY="여기에_구글_API_키를_입력하세요"
HF_TOKEN="여기에_허깅페이스_토큰을_입력하세요"
```

### 5. Python 서버 실행

```python
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Spring Boot

- IntelliJ 또는 Eclipse와 같은 IDE에서 프로젝트를 열면 Gradle이 자동으로 의존성을 설정합니다.
- 메인 애플리케이션 클래스(HelperApplication.java)를 실행하여 서버를 시작할 수 있습니다.

---

## Backend (Database - Oracle)

프로젝트 실행에 필요한 Oracle 데이터베이스와 사용자 계정, 테이블을 설정하는 절차입니다.
저희는 **SQL Developer**를  사용했으며, 아래 가이드는 터미널(SQL Plus) 기준입니다.

### **1. DB 관리자(sys)로 접속**

터미널에서 sysdba 권한으로 접속하거나, SQL Developer에서 SYSDBA Role로 접속합니다.

```sql
-- 터미널(SQL Plus) 접속 예시
sqlplus / as sysdba
```

### **2. PDB 생성 및 사용자 계정/테이블 생성**

sql/create_helperpdb_oracle.sql 스크립트의 내용을 실행하여 PDB와 사용자 계정을 생성합니다.

- **SQL Developer**: 스크립트 파일을 열고 F5 키를 눌러 스크립트 전체를 실행합니다.
- **SQL*Plus**: 아래 명령어를 실행합니다.

※ @ 명령어는 SQL Plus에서 스크립트 파일을 실행하는 명령어입니다. 스크립트 경로를 정확하게 입력해주세요.

```sql
@sql/create_helperpdb_oracle.sql
```

### **3. 테이블 및 데이터 생성**

생성된 helper 계정으로 재접속한 뒤, sql/helperpdb.sql 스크립트의 내용을 실행하여 테이블과 초기 데이터를 생성합니다.

- **SQL Developer**: helper 계정으로 새 접속을 만들고, 스크립트 파일을 열어 F5 키로 실행합니다.
- **SQL Plus**: 아래 명령어로 재접속 후 스크립트를 실행합니다.

```sql
connect helper/1111@localhost/helperpdb
@sql/helperpdb.sql
```

---

## **Frontend (React)**

프론트엔드 서버를 실행하기 전에, Python API 서버와 Spring Boot 서버가 먼저 실행되어 있어야 정상적으로 동작합니다.

### 1. 프론트엔드 디렉토리로 이동

```powershell
# 프로젝트 루트 디렉토리에서 React 폴더로 이동합니다.
cd front
```

### 2. 필요 패키지 설치

package.json 파일에 명시된 모든 의존성 라이브러리를 설치합니다.

```powershell
npm install
```

### 3. 프론트엔드 개발 서버 실행

```powershell
npm start
```
