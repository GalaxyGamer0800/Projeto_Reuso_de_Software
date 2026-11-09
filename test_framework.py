"""
Módulo: test_framework
Descrição: Script de teste para execução e validação do RentalFramework.
Técnica de Reuso: Validação de instâncias concretas estendendo a classe abstrata.
"""

from applications.urban_rent import UrbanRentBooking
from applications.beach_rent import BeachHouseRentBooking


def executar_testes():
    print("=" * 60)
    print("       TESTANDO RENTALFRAMEWORK - TEMPLATE METHOD")
    print("=" * 60)

    # 1. Testando Aplicação 1: UrbanRent (Apartamentos Urbanos)
    print("\n--- [APLICAÇÃO 1: UrbanRent] ---")
    urban_app = UrbanRentBooking()

    reserva_urbana = {
        "imovel_id": "APT-101",
        "hospede": "Carlos Silva",
        "dias": 7,
        "hospedes": 3,
        "valor_diaria": 150.0
    }

    resultado_urbano = urban_app.processar_reserva(reserva_urbana)
    print(f"Status: {resultado_urbano['status']}")
    print(f"Detalhe: {resultado_urbano.get('detalhe_calculo')}")
    print(f"Valor Total Final: R$ {resultado_urbano.get('valor_final', 0):.2f}")

    # 2. Testando Aplicação 2: BeachHouseRent (Casas de Praia)
    print("\n--- [APLICAÇÃO 2: BeachHouseRent] ---")
    beach_app = BeachHouseRentBooking()

    reserva_praia = {
        "imovel_id": "CASA-PRAIA-05",
        "hospede": "Ana Souza",
        "dias": 14,
        "hospedes": 8,
        "valor_diaria": 400.0
    }

    resultado_praia = beach_app.processar_reserva(reserva_praia)
    print(f"Status: {resultado_praia['status']}")
    print(f"Detalhe: {resultado_praia.get('detalhe_calculo')}")
    print(f"Valor Total Final: R$ {resultado_praia.get('valor_final', 0):.2f}")

    print("\n" + "=" * 60)
    print("       TESTES CONCLUÍDOS COM SUCESSO!")
    print("=" * 60)


if __name__ == "__main__":
    executar_testes()