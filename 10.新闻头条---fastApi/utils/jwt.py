import base64
import hashlib
import hmac
import json
import os
import secrets
from datetime import datetime, timedelta

TOKEN_EXPIRE_MINUTES = 60 * 24
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "news-app-secret-key")
JWT_ALGORITHM = "HS256"


class JWTError(Exception):
    pass


class JWTExpiredError(JWTError):
    pass


def _base64url_encode(data: bytes):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _base64url_decode(data: str):
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode((data + padding).encode("utf-8"))


def _sign(signing_input: str):
    digest = hmac.new(
        JWT_SECRET_KEY.encode("utf-8"),
        signing_input.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return _base64url_encode(digest)


##token创建，签发阶段
def create_access_token(user_id: int, username: str):
    expires_at = datetime.now() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    jti = secrets.token_urlsafe(16)
    header = {"typ": "JWT", "alg": JWT_ALGORITHM}
    payload = {
        "sub": str(user_id),
        "username": username,
        "jti": jti,
        "exp": int(expires_at.timestamp()),
    }

    encoded_header = _base64url_encode(
        json.dumps(header, separators=(",", ":")).encode("utf-8")
    )
    encoded_payload = _base64url_encode(
        json.dumps(payload, separators=(",", ":")).encode("utf-8")
    )
    signing_input = f"{encoded_header}.{encoded_payload}"
    return {
        "access_token": f"{signing_input}.{_sign(signing_input)}",
        "jti": jti,
        "expires_at": expires_at,
    }


# 解析token，验证阶段
def decode_access_token(token: str):
    try:
        encoded_header, encoded_payload, signature = token.split(".")
    except ValueError as exc:
        raise JWTError("token格式错误") from exc

    signing_input = f"{encoded_header}.{encoded_payload}"
    expected_signature = _sign(signing_input)
    if not hmac.compare_digest(signature, expected_signature):
        raise JWTError("token签名无效")

    try:
        header = json.loads(_base64url_decode(encoded_header))
        payload = json.loads(_base64url_decode(encoded_payload))
    except (json.JSONDecodeError, ValueError) as exc:
        raise JWTError("token解析失败") from exc

    if header.get("alg") != JWT_ALGORITHM:
        raise JWTError("token算法无效")

    exp = payload.get("exp")
    if not isinstance(exp, int):
        raise JWTError("token缺少过期时间")
    if datetime.now().timestamp() >= exp:
        raise JWTExpiredError("token已过期")

    if not payload.get("sub") or not payload.get("jti"):
        raise JWTError("token内容无效")

    return payload
