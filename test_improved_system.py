#!/usr/bin/env python3
"""
개선된 OpenManus 시스템 테스트
"""
import asyncio
import sys
import os

# OpenManus 모듈 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'OpenManus'))

from app.agent.manus import Manus
from app.logger import logger

async def test_improved_system():
    """개선된 시스템 테스트"""
    try:
        # Manus 에이전트 생성
        agent = await Manus.create()
        
        # 간단한 테스트 요청
        test_request = "네이버 계정으로 로그인하고 'AI 기술 동향'에 대한 간단한 블로그 포스트를 작성해줘"
        
        logger.info("🔥 개선된 OpenManus 시스템 테스트 시작")
        logger.info(f"📝 테스트 요청: {test_request}")
        
        # 에이전트 실행
        response = await agent.run(test_request)
        
        logger.info("✅ 테스트 완료")
        logger.info(f"📄 응답: {response}")
        
        # 워크스페이스 정보 출력
        if hasattr(agent, 'workspace_path'):
            logger.info(f"📁 워크스페이스: {agent.workspace_path}")
            logger.info(f"📋 계획서: {agent.plan_path}")
            logger.info(f"📊 상태 파일: {agent.status_path}")
        
        # 정리
        await agent.cleanup()
        
    except Exception as e:
        logger.error(f"테스트 실패: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(test_improved_system())