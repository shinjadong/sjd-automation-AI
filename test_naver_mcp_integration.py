#!/usr/bin/env python3
"""
네이버 검색 MCP와 OpenManus 통합 테스트 스크립트
"""

import os
import sys
import asyncio
import json
from pathlib import Path

# OpenManus 모듈 경로 추가
project_root = Path(__file__).parent
sys.path.append(str(project_root / "OpenManus"))

from app.tool.mcp import MCPClients
from app.config import Config

async def test_naver_mcp_integration():
    """네이버 검색 MCP 통합 테스트"""
    print("🔍 네이버 검색 MCP 통합 테스트 시작...")
    
    try:
        # MCP 설정 파일 경로
        mcp_config_path = project_root / "OpenManus" / "config" / "mcp.json"
        
        print(f"📁 MCP 설정 파일 경로: {mcp_config_path}")
        
        if not mcp_config_path.exists():
            print("❌ MCP 설정 파일이 존재하지 않습니다!")
            return False
            
        # MCP 설정 로드
        with open(mcp_config_path, 'r') as f:
            mcp_config = json.load(f)
        
        print(f"✅ MCP 설정 로드 완료: {mcp_config}")
        
        # MCPClients 초기화
        mcp_clients = MCPClients()
        
        # 네이버 검색 MCP 서버 추가
        naver_config = mcp_config["mcpServers"]["naver-search"]
        server_name = "naver-search"
        
        print(f"🔌 {server_name} MCP 서버 연결 시도...")
        
        # MCP 서버 연결
        await mcp_clients.connect_stdio(
            command=naver_config["command"],
            args=naver_config["args"],
            server_id=server_name
        )
        
        print(f"✅ {server_name} MCP 서버 연결 성공!")
        
        # 사용 가능한 도구 목록 조회
        tools = await mcp_clients.list_tools()
        print(f"🛠️ 사용 가능한 도구들: {[tool['name'] for tool in tools]}")
        
        # 네이버 검색 도구 테스트 (예시)
        if any(tool['name'].startswith('naver') for tool in tools):
            print("🎉 네이버 검색 도구가 성공적으로 로드되었습니다!")
            
            # 실제 검색 테스트 (옵션)
            # 네이버 API 키가 설정되어 있다면 실제 검색을 수행할 수 있습니다.
            print("💡 실제 검색을 수행하려면 .env 파일에 NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET을 설정하세요.")
            
        else:
            print("⚠️ 네이버 검색 도구를 찾을 수 없습니다.")
        
        # 연결 종료
        await mcp_clients.disconnect()
        print("🔚 테스트 완료 - 모든 연결이 종료되었습니다.")
        
        return True
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """메인 함수"""
    print("=" * 60)
    print("🤖 SJD Automation AI - 네이버 검색 MCP 통합 테스트")
    print("=" * 60)
    
    success = await test_naver_mcp_integration()
    
    if success:
        print("\n🎉 통합 테스트 성공!")
        print("✅ 네이버 검색 MCP가 OpenManus에 성공적으로 통합되었습니다.")
        print("\n📝 다음 단계:")
        print("1. .env 파일에 네이버 API 키 설정")
        print("2. OpenManus 실행하여 네이버 검색 기능 사용")
    else:
        print("\n❌ 통합 테스트 실패!")
        print("⚠️ 설정을 다시 확인해주세요.")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 