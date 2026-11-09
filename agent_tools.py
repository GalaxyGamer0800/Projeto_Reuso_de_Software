"""
Módulo: agent_tools
Descrição: Ferramentas (Tools) integradas ao API Gateway para uso do Agente de IA.
Técnica: Tool Calling / Integration Layer
Porta Alvo: 8000 (API Gateway)
"""

import httpx
from typing import Dict, Any, Optional

GATEWAY_URL = "http://localhost:8000/api"


def buscar_imoveis_tool(cidade: Optional[str] = None) -> Dict[str, Any]:
    """
    Ferramenta para consultar imóveis disponíveis no catálogo por cidade.
    """
    url = f"{GATEWAY_URL}/properties"
    params = {"cidade": cidade} if cidade else {}

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url, params=params)
            if response.status_code == 200:
                return {"sucesso": True, "imoveis": response.json()}
            return {"sucesso": False, "erro": f"Erro {response.status_code}: {response.text}"}
    except Exception as e:
        return {"sucesso": False, "erro": f"Falha na comunicação com Gateway: {str(e)}"}


def criar_reserva_tool(
    imovel_id: str,
    hospede: str,
    tipo_aplicacao: str,
    dias: int,
    hospedes: int,
    valor_diaria: float
) -> Dict[str, Any]:
    """
    Ferramenta para efetuar uma reserva de imóvel via Booking Service.
    tipo_aplicacao deve ser 'urban' ou 'beach'.
    """
    url = f"{GATEWAY_URL}/bookings"
    payload = {
        "imovel_id": imovel_id,
        "hospede": hospede,
        "tipo_aplicacao": tipo_aplicacao.lower(),
        "dias": dias,
        "hospedes": hospedes,
        "valor_diaria": valor_diaria
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(url, json=payload)
            if response.status_code in (200, 201):
                return {"sucesso": True, "reserva": response.json()}
            return {"sucesso": False, "erro": response.json().get("detail", response.text)}
    except Exception as e:
        return {"sucesso": False, "erro": f"Falha na comunicação com Gateway: {str(e)}"}


def processar_pagamento_tool(booking_id: int, valor: float, metodo_pagamento: str) -> Dict[str, Any]:
    """
    Ferramenta para efetuar a liquidação financeira de uma reserva via Payment Service.
    metodo_pagamento ex: 'PIX', 'CREDIT_CARD', 'BOLETO'.
    """
    url = f"{GATEWAY_URL}/payments/process"
    payload = {
        "booking_id": booking_id,
        "valor": valor,
        "metodo_pagamento": metodo_pagamento.upper()
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(url, json=payload)
            if response.status_code in (200, 201):
                return {"sucesso": True, "pagamento": response.json()}
            return {"sucesso": False, "erro": response.json().get("detail", response.text)}
    except Exception as e:
        return {"sucesso": False, "erro": f"Falha na comunicação com Gateway: {str(e)}"}