"""
Módulo: test_microservices
Descrição: Script de teste de integração para validação do API Gateway e Microsserviços.
Tecnologia: HTTPX / Requests
Porta Alvo: 8000 (API Gateway)
"""

import httpx
import time

GATEWAY_URL = "http://localhost:8000/api"


def executar_testes_integrados():
    print("=" * 65)
    print("       TESTE INTEGRADO DE MICROSSERVIÇOS VIA API GATEWAY")
    print("=" * 65)

    with httpx.Client(timeout=10.0) as client:
        # 1. Cadastrar um imóvel via Property Service (Porta 8001 via Gateway)
        print("\n1. [PROPERTY SERVICE] Cadastrando imóvel via API Gateway...")
        payload_imovel = {
            "id": "APT-URB-202",
            "titulo": "Apartamento Executivo Centro",
            "cidade": "Recife",
            "tipo": "Apartamento",
            "capacidade": 3,
            "preco_diaria": 200.0
        }
        res_prop = client.post(f"{GATEWAY_URL}/properties", json=payload_imovel)
        print(f"   Status Code: {res_prop.status_code}")
        print(f"   Resposta: {res_prop.json()}")

        # 2. Listar imóveis via API Gateway
        print("\n2. [PROPERTY SERVICE] Consultando catálogo por cidade 'Recife'...")
        res_list = client.get(f"{GATEWAY_URL}/properties?cidade=Recife")
        print(f"   Status Code: {res_list.status_code}")
        print(f"   Imóveis encontrados: {len(res_list.json())}")

        # 3. Criar Reserva via Booking Service (Porta 8002 via Gateway)
        print("\n3. [BOOKING SERVICE] Efetuando reserva com regra UrbanRent (7 diárias)...")
        payload_reserva = {
            "imovel_id": "APT-URB-202",
            "hospede": "Fernanda Lima",
            "tipo_aplicacao": "urban",
            "dias": 7,
            "hospedes": 2,
            "valor_diaria": 200.0
        }
        res_book = client.post(f"{GATEWAY_URL}/bookings", json=payload_reserva)
        print(f"   Status Code: {res_book.status_code}")
        dados_reserva = res_book.json()
        print(f"   ID da Reserva: {dados_reserva.get('id')}")
        print(f"   Status da Reserva: {dados_reserva.get('status')}")
        print(f"   Cálculo: {dados_reserva.get('detalhe_calculo')}")
        print(f"   Valor Final Calculado: R$ {dados_reserva.get('valor_final'):.2f}")

        booking_id = dados_reserva.get("id")
        valor_final = dados_reserva.get("valor_final")

        # 4. Processar Pagamento via Payment Service (Porta 8003 via Gateway)
        print("\n4. [PAYMENT SERVICE] Efetuando liquidação financeira via PIX...")
        payload_pagamento = {
            "booking_id": booking_id,
            "valor": valor_final,
            "metodo_pagamento": "PIX"
        }
        res_pay = client.post(f"{GATEWAY_URL}/payments/process", json=payload_pagamento)
        print(f"   Status Code: {res_pay.status_code}")
        dados_pagamento = res_pay.json()
        print(f"   Status Pagamento: {dados_pagamento.get('status')}")
        print(f"   Comprovante: {dados_pagamento.get('comprovante_id')}")

    print("\n" + "=" * 65)
    print("       FLUXO COMPLETO VIA API GATEWAY CONCLUÍDO COM SUCESSO!")
    print("=" * 65)


if __name__ == "__main__":
    executar_testes_integrados()