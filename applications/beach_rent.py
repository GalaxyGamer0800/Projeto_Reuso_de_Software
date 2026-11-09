"""
Módulo: applications.beach_rent
Descrição: Aplicação 2 - Locação de Casas de Praia e Temporada.
Técnica de Reuso: Reuso de Framework com sobrescrita de Hotspots.
"""

from typing import Dict, Any, Tuple
from rental_core.template import RentalBookingTemplate


class BeachHouseRentBooking(RentalBookingTemplate):
    """
    Aplicação concreta para aluguer de casas de praia e temporada.
    """

    def validar_regras_locacao(self, dados_reserva: Dict[str, Any]) -> Tuple[bool, str]:
        """
        HOTSPOT 1: Validação específica para casas de praia.
        Regra: Mínimo de 3 diárias (estadia mínima) e máximo de 12 hóspedes.
        """
        dias = dados_reserva.get("dias", 0)
        hospedes = dados_reserva.get("hospedes", 1)

        if dias < 3:
            return False, "BeachHouseRent exige estadia mínima de 3 diárias."
        if hospedes > 12:
            return False, "Casas de praia comportam no máximo 12 hóspedes."
        return True, "Validação aprovada para BeachHouseRent."

    def calcular_taxas_e_descontos(self, valor_base: float, dias: int) -> Tuple[float, str]:
        """
        HOTSPOT 2: Regra tarifária de temporada.
        Regra: Taxa de manutenção de R$ 150,00 e 15% de desconto para estadias a partir de 14 dias.
        """
        taxa_manutencao = 150.0
        desconto = self.pricing_calculator.calcular_desconto_progressivo(
            valor_base=valor_base,
            dias=dias,
            dias_minimos=14,
            percentual_desconto=15.0
        )

        valor_com_taxa = self.pricing_calculator.aplicar_taxa_fixa(valor_base, taxa_manutencao)
        valor_final = round(valor_com_taxa - desconto, 2)

        detalhe = f"Base: R$ {valor_base:.2f} | Manutenção: +R$ {taxa_manutencao:.2f} | Desconto (>=14 dias): -R$ {desconto:.2f}"
        return valor_final, detalhe