#!/usr/bin/env python3
"""
Manus 에이전트와 네이버 검색 MCP 통합 테스트
"""

import asyncio
import sys
from pathlib import Path

# OpenManus 모듈 경로 추가
project_root = Path(__file__).parent
sys.path.append(str(project_root / "OpenManus"))

from app.agent.manus import Manus
from app.logger import logger

async def test_manus_naver_mcp():
    """Manus 에이전트로 네이버 검색 MCP 테스트"""
    print("🤖 Manus 에이전트 네이버 검색 MCP 테스트 시작...")
    
    try:
        # Manus 에이전트 생성
        print("📦 Manus 에이전트 생성 중...")
        agent = await Manus.create()
        
        print("✅ Manus 에이전트 생성 완료!")
        
        # 사용 가능한 도구 확인
        if hasattr(agent, 'tool_collection') and hasattr(agent.tool_collection, 'tools'):
            tools = agent.tool_collection.tools
            tool_names = [tool.name for tool in tools] if tools else []
            print(f"🛠️ 사용 가능한 도구들: {tool_names}")
            
            # 네이버 관련 도구 확인
            naver_tools = [name for name in tool_names if 'naver' in name.lower()]
            if naver_tools:
                print(f"🎉 네이버 관련 도구 발견: {naver_tools}")
            else:
                print("⚠️ 네이버 관련 도구를 찾을 수 없습니다.")
                
        else:
            print("⚠️ 도구 정보를 확인할 수 없습니다.")
        
        # 간단한 테스트 실행
        print("\n🔍 간단한 테스트 명령 실행...")
        response = await agent.run("사용 가능한 도구들을 나열해줘")
        
        if hasattr(response, 'content'):
            print(f"📝 응답: {response.content}")
        else:
            print(f"📝 응답: {str(response)}")
        
        # 정리
        await agent.cleanup()
        print("🔚 테스트 완료!")
        
        return True
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """메인 함수"""
    print("=" * 60)
    print("🤖 SJD Automation AI - Manus 네이버 검색 MCP 테스트")
    print("=" * 60)
    
    success = await test_manus_naver_mcp()
    
    if success:
        print("\n🎉 테스트 성공!")
        print("✅ Manus 에이전트가 정상적으로 실행되었습니다.")
    else:
        print("\n❌ 테스트 실패!")
        print("⚠️ 설정을 다시 확인해주세요.")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 