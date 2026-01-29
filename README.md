# 스키장 정보 제공 사이트 "whiteBalance"

### 프로젝트 소개
#### 개요 
- 국내 여러 스키장의 정보를 한 사이트에서 손쉽게 볼 수 있다면 편리하지 않을까 ?
- 스키와 스노우 보드를 즐기는 같은 취미를 가진 사람들의 공간

#### 목적
- 국내 스키장의 정보를 모아 볼 수 있고, 스키/스노우 보드를 즐기는 사람들이 소통할 수 있는 사이트 제작
- 
#### 기대효과
- 여러 스키장의 정보를 한 사이트에서 손쉽게 비교 가능

- 최신 업데이트를 반영한 스키장 정보를 볼 수 있음

- 스키와 스노우 보드라는 같은 취미를 가진 사람들끼리 소통, 정보 공유 가능

- ‘ 같이탈사람 ’ 게시판을 통해 취미를 함께할 사람을 구할 수 있음
  
#### 담당 파트
- 백엔드 개발 담당 : REST API 설계 및 구현 경험, 데이터 처리, 서버 배포
- 서비스 미완성

### 기술스택
- Language : JAVA, Python
- Framework : SpringBoot3, Spring Web, Spring Data JPA, Spring Security, Spring Session, Spring Validation
- Database : MariaDB, JPA, JPQL
- Deployment / DevOps : AWS LightSail (Amazon Linux 2023), AWS Lambda, EventBridge, Docker,  Docker Compose, Nginx
- HTTPS / SSL : Certbot (Let’s Encrypt)
- API Docs : Swagger
- API Test : Postman
- Version Control : Git / GitHub
- CI/CD : GitHub, GitHub Actions

### ERD
<img width="1368" height="1108" alt="whiteabalance erd" src="https://github.com/user-attachments/assets/54397eee-f820-43d1-b0e0-79b6f4f750ff" />

### Project Architecture
<img width="1116" height="761" alt="whitebalance architecture" src="https://github.com/user-attachments/assets/1b4054f2-28fe-4219-9403-04b6ae7cae70" />

### 주요기능
#### 회원가입/로그인
- Spring Security
- JWT 로그인 구현

#### 커뮤니티
- 자유게시판/같이탈사람 게시판

#### 게시글/댓글 CRUD
- 게시글/댓글 조회, 상세조회, 등록, 수정, 삭제

#### 스키장 데이터 크롤링
- Python 크롤링 함수 작성 – 각 스키장 홈페이지에서 데이터 크롤링

- 크롤링 함수 -> Docker Image -> AWS Lambda에 배포
   - 변동 데이터의 정기적 수집과 처리를 위해 Serverless 환경에 배포
   - 자동화 : Lambda 함수에 trigger를 추가하여 매일 자정마다 실행

#### 스키장 데이터 파싱
- 리조트별 각각의 파싱 로직 적용
  - 리조트별 상이한 데이터 포맷을 처리하기 위해 parserMap을 활용한 Strategy Pattern 구조 적용
- 리조트별 상이한 원시 데이터를 도메인 객체 SlopeInfoForm에 맞게 매핑
- 파싱한 데이터 -> Frontend 에 API로 전달
- 클라이언트가 사용할 수 있는 형태로 데이터를 가공하여 전달
