"""
Módulo: services.api_gateway.main
Descrição: API Gateway centralizador e roteador do ecossistema de microsserviços.
Tecnologia: FastAPI + HTTPX (Reverse Proxy / Facade)
Porta: 8000
"""

import httpx
from fastapi import FastAPI, HTTPException, Request, Response

app = FastAPI(title="API Gateway", version="1.0.0")

PROPERTY_SERVICE_URL = "http://localhost:8001"
BOOKING_SERVICE_URL = "http://localhost:8002"
PAYMENT_SERVICE_URL = "http://localhost:8003"


async def forward_request(target_url: str, request: Request) -> Response:
    """Redireciona a requisição HTTP recebida no Gateway para o microsserviço de destino."""
    async with httpx.AsyncClient(follow_redirects=True) as client:
        body = await request.body()
        headers = dict(request.headers)
        headers.pop("host", None)

        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                params=request.query_params,
                content=body,
                timeout=10.0
            )
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Serviço indisponível no endereço {target_url}: {str(exc)}"
            )


# Roteamento para Property Service (Porta 8001)
@app.api_route("/api/properties", methods=["GET", "POST", "PUT", "DELETE"])
@app.api_route("/api/properties/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_property(request: Request, path: str = ""):
    clean_path = path.strip("/")
    target_url = f"{PROPERTY_SERVICE_URL}/properties/{clean_path}" if clean_path else f"{PROPERTY_SERVICE_URL}/properties"
    return await forward_request(target_url, request)


# Roteamento para Booking Service (Porta 8002)
@app.api_route("/api/bookings", methods=["GET", "POST", "PUT", "DELETE"])
@app.api_route("/api/bookings/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_booking(request: Request, path: str = ""):
    clean_path = path.strip("/")
    target_url = f"{BOOKING_SERVICE_URL}/bookings/{clean_path}" if clean_path else f"{BOOKING_SERVICE_URL}/bookings"
    return await forward_request(target_url, request)


# Roteamento para Payment Service (Porta 8003)
@app.api_route("/api/payments", methods=["GET", "POST", "PUT", "DELETE"])
@app.api_route("/api/payments/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_payment(request: Request, path: str = ""):
    clean_path = path.strip("/")
    target_url = f"{PAYMENT_SERVICE_URL}/payments/{clean_path}" if clean_path else f"{PAYMENT_SERVICE_URL}/payments"
    return await forward_request(target_url, request)