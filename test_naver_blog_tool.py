#!/usr/bin/env python3
"""
네이버 블로그 툴 테스트 스크립트
"""
import asyncio
import sys
import os

# 현재 디렉토리를 Python path에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'OpenManus'))

from app.tool.naver_blog_tool import NaverBlogTool


async def test_naver_blog_tool():
    """네이버 블로그 툴 테스트"""
    print("🚀 네이버 블로그 자동화 툴 테스트 시작")
    
    # 툴 인스턴스 생성
    blog_tool = NaverBlogTool()
    
    print(f"📋 툴 이름: {blog_tool.name}")
    print(f"📝 툴 설명: {blog_tool.description}")
    print()
    
    # 사용 가능한 액션들 출력
    actions = blog_tool.parameters["properties"]["action"]["enum"]
    print("🔧 사용 가능한 액션들:")
    for i, action in enumerate(actions, 1):
        descriptions = {
            "login": "네이버 계정으로 로그인",
            "post": "블로그 포스트 작성 및 발행",
            "get_categories": "블로그 카테고리 조회",
            "logout": "로그아웃"
        }
        print(f"  {i}. {action} - {descriptions.get(action, '설명 없음')}")
    
    print("\n" + "="*50)
    print("💡 사용법 예시:")
    print()
    
    print("1️⃣ 로그인:")
    print('   await blog_tool.execute(action="login", naver_id="your_id", naver_password="your_password")')
    print()
    
    print("2️⃣ 카테고리 조회:")
    print('   await blog_tool.execute(action="get_categories")')
    print()
    
    print("3️⃣ 블로그 포스팅:")
    print('   await blog_tool.execute(')
    print('       action="post",')
    print('       title="오늘의 AI 뉴스",')
    print('       content="AI 기술의 발전이 우리 생활에 미치는 영향...",')
    print('       category="기술",')
    print('       tags=["AI", "기술", "뉴스"],')
    print('       publish_immediately=True')
    print('   )')
    print()
    
    print("4️⃣ 로그아웃:")
    print('   await blog_tool.execute(action="logout")')
    print()
    
    print("="*50)
    print("🎯 OpenManus에서 사용하는 방법:")
    print()
    print("OpenManus 에이전트에게 다음과 같이 요청하세요:")
    print('• "네이버 블로그에 \'오늘의 뉴스\'라는 제목으로 글을 써줘"')
    print('• "내 네이버 블로그에 AI 관련 포스트를 작성해줘"')
    print('• "네이버 블로그 카테고리를 조회해줘"')
    print()
    
    print("✅ 네이버 블로그 자동화 툴이 성공적으로 OpenManus에 통합되었습니다!")
    print("🔐 실제 사용 시에는 네이버 계정 정보가 필요합니다.")


if __name__ == "__main__":
    asyncio.run(test_naver_blog_tool())