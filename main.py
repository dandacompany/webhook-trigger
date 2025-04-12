from fastmcp import FastMCP
from typing import Dict, Any, Optional
import httpx
from pydantic import BaseModel

# FastMCP 서버 생성
mcp = FastMCP("Webhook MCP Server")

class WebhookRequest(BaseModel):
    url: str
    headers: Optional[Dict[str, str]] = None
    payload: Optional[Dict[str, Any]] = None

@mcp.tool()
async def send_get_webhook(url: str, auth_token: str = None, custom_headers: Dict[str, str] = None) -> Dict[str, Any]:
    """
    GET 방식으로 웹훅을 전송합니다.
    
    Args:
        url: 호출할 웹훅 URL
        auth_token: 인증에 사용할 토큰 (선택 사항)
        custom_headers: 추가 요청 헤더 (선택 사항)
    
    Returns:
        웹훅 응답 정보 (상태 코드, 응답 내용, 헤더)
    """
    if not url:
        raise ValueError("URL이 필요합니다")
    
    try:
        async with httpx.AsyncClient() as client:
            headers = custom_headers or {}
            if auth_token:
                headers["Authorization"] = auth_token
                
            response = await client.get(url, headers=headers)
            
            # 응답 처리
            content = None
            try:
                content = response.json()
            except:
                content = response.text
            
            return {
                "status_code": response.status_code,
                "response": content,
                "headers": dict(response.headers)
            }
    except Exception as e:
        return {
            "error": f"웹훅 전송 실패: {str(e)}"
        }

@mcp.tool()
async def send_post_webhook(url: str, payload: Dict[str, Any] = None, headers: Dict[str, str] = None, auth_token: str = None) -> Dict[str, Any]:
    """
    POST 방식으로 웹훅을 전송합니다.
    
    Args:
        url: 호출할 웹훅 URL
        payload: 전송할 JSON 페이로드 (선택 사항)
        headers: 요청 헤더 (선택 사항)
        auth_token: 인증에 사용할 토큰 (선택 사항)
    
    Returns:
        웹훅 응답 정보 (상태 코드, 응답 내용, 헤더)
    """
    if not url:
        raise ValueError("URL이 필요합니다")
    
    try:
        headers = headers or {}
        if auth_token:
            headers["Authorization"] = auth_token
            
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                json=payload
            )
            
            # 응답 처리
            content = None
            try:
                content = response.json()
            except:
                content = response.text
            
            return {
                "status_code": response.status_code,
                "response": content,
                "headers": dict(response.headers)
            }
    except Exception as e:
        return {
            "error": f"웹훅 전송 실패: {str(e)}"
        }

@mcp.tool()
async def send_custom_webhook(method: str, url: str, payload: Dict[str, Any] = None, headers: Dict[str, str] = None, auth_token: str = None) -> Dict[str, Any]:
    """
    사용자 지정 HTTP 메서드로 웹훅을 전송합니다.
    
    Args:
        method: HTTP 메서드 (GET, POST, PUT, DELETE 등)
        url: 호출할 웹훅 URL
        payload: 전송할 JSON 페이로드 (선택 사항, POST/PUT에서 주로 사용)
        headers: 요청 헤더 (선택 사항)
        auth_token: 인증에 사용할 토큰 (선택 사항)
    
    Returns:
        웹훅 응답 정보 (상태 코드, 응답 내용, 헤더)
    """
    if not url:
        raise ValueError("URL이 필요합니다")
    
    if not method:
        raise ValueError("HTTP 메서드가 필요합니다")
    
    try:
        headers = headers or {}
        if auth_token:
            headers["Authorization"] = auth_token
            
        async with httpx.AsyncClient() as client:
            method = method.upper()
            
            if method == "GET":
                response = await client.get(url, headers=headers)
            elif method == "POST":
                response = await client.post(url, headers=headers, json=payload)
            elif method == "PUT":
                response = await client.put(url, headers=headers, json=payload)
            elif method == "DELETE":
                response = await client.delete(url, headers=headers)
            elif method == "PATCH":
                response = await client.patch(url, headers=headers, json=payload)
            else:
                return {"error": f"지원되지 않는 HTTP 메서드: {method}"}
            
            # 응답 처리
            content = None
            try:
                content = response.json()
            except:
                content = response.text
            
            return {
                "status_code": response.status_code,
                "response": content,
                "headers": dict(response.headers)
            }
    except Exception as e:
        return {
            "error": f"웹훅 전송 실패: {str(e)}"
        }

if __name__ == "__main__":
    mcp.run() 