#!/bin/bash
# OpenManus AI 에이전트 실행 스크립트

# 스크립트가 위치한 디렉토리로 이동하여 항상 프로젝트 루트에서 실행되도록 보장합니다.
cd "$(dirname "$0")"

echo "==============================================="
echo "🚀 OpenManus AI 에이전트를 시작합니다..."
echo "==============================================="

# 현재 시스템에 설치된 Python을 사용하여 main.py를 실행합니다.
/home/tlswk/.pyenv/versions/3.11.9/bin/python OpenManus/main.py
