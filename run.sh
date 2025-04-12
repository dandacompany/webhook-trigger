#!/bin/bash

# 가상환경 활성화
source venv/bin/activate

# 필요한 패키지 설치
pip install -r requirements.txt

# 서버 실행 방법 1: 개발 모드 (웹 인터페이스 제공)
# fastmcp dev main.py

# 서버 실행 방법 2: 직접 실행
python main.py 