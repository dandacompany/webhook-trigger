#!/bin/bash
# mcp_run.sh

# 오류 발생 시 스크립트 중단
set -e

# 프로젝트 디렉토리로 이동
cd "$(dirname "$0")"

# Python 경로 설정
PYTHON_PATH="/Users/dante/miniconda3/bin/python"

# 필요한 패키지들
REQUIRED_PACKAGES="fastmcp httpx mcp pydantic pydantic-settings python-dotenv typer"

echo "종속성 확인 및 설치 중..."

# 필요한 패키지 모두 확인 및 설치
for package in $REQUIRED_PACKAGES; do
  echo "패키지 확인: $package"
  $PYTHON_PATH -c "import ${package//-/_}" 2>/dev/null || {
    echo "${package} 설치 중..."
    $PYTHON_PATH -m pip install $package
  }
done

echo "모든 종속성이 설치되었습니다."

# 메인 스크립트 실행
echo "메인 스크립트 실행 중..."
$PYTHON_PATH ./main.py 