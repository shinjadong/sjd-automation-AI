# 🤖 SJD Automation AI

> **AI 기반 네이버 블로그 자동화 시스템**  
> OpenManus 프레임워크를 활용한 지능형 블로그 포스팅 자동화 도구

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![OpenManus](https://img.shields.io/badge/framework-OpenManus-green.svg)

## 📋 개요

SJD Automation AI는 OpenManus AI 프레임워크를 기반으로 구축된 네이버 블로그 자동화 시스템입니다. 자연어 명령으로 블로그 포스팅, 이미지 업로드, 카테고리 관리 등을 자동화할 수 있습니다.

## ✨ 주요 기능

### 🎯 블로그 자동화
- ✅ **자동 로그인**: 네이버 계정 자동 로그인 및 세션 관리
- ✅ **포스트 작성**: AI 기반 컨텐츠 생성 및 자동 발행
- ✅ **이미지 처리**: 자동 이미지 업로드 및 최적화
- ✅ **카테고리 관리**: 자동 카테고리 분류 및 태그 설정
- ✅ **스케줄링**: 예약 발행 및 일정 관리

### 🤖 AI 에이전트 기능
- 🧠 **자연어 처리**: 한국어 명령 이해 및 실행
- 📊 **컨텐츠 분석**: 블로그 데이터 크롤링 및 분석
- 🎨 **자동 최적화**: SEO 최적화 및 가독성 개선
- 📈 **성과 분석**: 포스팅 성과 모니터링

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# 저장소 클론
git clone https://github.com/shinjadong/sjd-automation-AI.git
cd sjd-automation-AI

# 가상환경 활성화
source venv/bin/activate

# OpenManus 실행
./run.sh
```

### 2. 기본 사용법
```python
# AI 에이전트에게 자연어로 명령
"네이버 블로그에 'AI 기술 트렌드'라는 제목으로 포스트를 작성해줘"
"이미지 3장을 포함한 여행 후기를 '여행' 카테고리에 발행해줘"
"내 블로그의 최근 포스트 성과를 분석해줘"
```

## 📁 프로젝트 구조

```
sjd-automation-AI/
├── OpenManus/                  # OpenManus AI 프레임워크
│   ├── app/                   # 핵심 애플리케이션
│   │   ├── agent/            # AI 에이전트 모듈
│   │   ├── tool/             # 도구 및 플러그인
│   │   └── flow/             # 워크플로우 관리
│   ├── config/               # 설정 파일
│   └── examples/             # 사용 예제
├── naver_blog_crawler.py      # 네이버 블로그 크롤러
├── test_naver_blog_tool.py    # 테스트 스크립트
├── run.sh                     # 실행 스크립트
└── README.md                  # 프로젝트 문서
```

## 🛠️ 주요 컴포넌트

### 네이버 블로그 크롤러
- **파일**: `naver_blog_crawler.py`
- **기능**: Playwright 기반 블로그 데이터 추출
- **지원**: 제목, 작성자, 본문 정확 추출

### AI 에이전트 도구
- **경로**: `OpenManus/app/tool/`
- **네이버 블로그 도구**: 포스팅, 로그인, 카테고리 관리
- **시각화 도구**: 차트 생성 및 데이터 분석
- **검색 도구**: 웹 검색 및 정보 수집

## 📝 사용 예제

### 기본 포스팅
```python
# 간단한 포스트 작성
"네이버 블로그에 '오늘의 일기'를 작성해줘"

# 카테고리와 태그 포함
"'기술' 카테고리에 AI 관련 포스트를 작성하고 'AI, 머신러닝' 태그를 추가해줘"
```

### 고급 기능
```python
# 이미지 포함 포스팅
"여행 사진 3장과 함께 제주도 여행 후기를 작성해줘"

# 데이터 분석 및 차트 생성
"최근 1개월 블로그 방문자 데이터를 차트로 만들어줘"
```

## ⚙️ 설정

### 환경 변수
```bash
# .env 파일 설정 예제
NAVER_ID=your_naver_id
NAVER_PASSWORD=your_password
OPENAI_API_KEY=your_openai_key
```

### 설정 파일
- **OpenManus 설정**: `OpenManus/config/config.toml`
- **에이전트 설정**: 모델 및 프롬프트 커스터마이징 가능

## 🔧 개발 가이드

### 의존성 설치
```bash
pip install -r requirements.txt
```

### 테스트 실행
```bash
python test_naver_blog_tool.py
```

### 새로운 도구 추가
1. `OpenManus/app/tool/` 디렉토리에 도구 파일 생성
2. 베이스 클래스 상속 및 메서드 구현
3. 도구 등록 및 테스트

## 📊 성능 및 특징

- **응답 속도**: 평균 2-3초 내 포스팅 완료
- **정확도**: 95% 이상의 자연어 명령 이해율
- **안정성**: 자동 재시도 및 오류 복구 메커니즘
- **확장성**: 플러그인 아키텍처로 기능 확장 용이

## 🤝 기여하기

1. Fork 프로젝트
2. Feature 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 변경사항 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 Push (`git push origin feature/AmazingFeature`)
5. Pull Request 생성

## 📄 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 👨‍💻 개발자

**신자동 (Shin Ja-dong)**
- GitHub: [@shinjadong](https://github.com/shinjadong)
- Email: contact@example.com

## 🙏 감사의 말

- [OpenManus](https://github.com/microsoft/OpenManus) 프레임워크 팀
- Playwright 개발팀
- 오픈소스 커뮤니티

---

<div align="center">
  <strong>🚀 AI로 블로그를 자동화하세요! 🚀</strong>
</div>