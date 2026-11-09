"""
Módulo: applications.urban_rent
Descrição: Aplicação 1 - Locação de Apartamentos Urbanos.
Técnica de Reuso: Reuso de Framework com sobrescrita de Hotspots.
"""

from typing import Dict, Any, Tuple
from rental_core.template import RentalBookingTemplate


class UrbanRentBooking(RentalBookingTemplate):
    """
    Aplicação concreta para aluguer de apartamentos urbanos.
    """

    def validar_regras_locacao(self, dados_reserva: Dict[str, Any]) -> Tuple[bool, str]:
        """
        HOTSPOT 1: Validação específica para ambiente urbano.
        Regra: Mínimo de 1 diária e máximo de 4 hóspedes.
        """
        dias = dados_reserva.get("dias", 0)
        hospedes = dados_reserva.get("hospedes", 1)

        if dias < 1:
            return False, "UrbanRent exige pelo menos 1 diária."
        if hospedes > 4:
            return False, "Apartamentos urbanos comportam no máximo 4 hóspedes."
        return True, "Validação aprovada para UrbanRent."

    def calcular_taxas_e_descontos(self, valor_base: float, dias: int) -> Tuple[float, str]:
        """
        HOTSPOT 2: Regra tarifária urbana.
        Regra: Taxa fixa de limpeza de R$ 50,00 e 10% de desconto para estadias a partir de 7 dias.
        """
        taxa_limpeza = 50.0
        desconto = self.pricing_calculator.calcular_desconto_progressivo(
            valor_base=valor_base,
            dias=dias,
            dias_minimos=7,
            percentual_desconto=10.0
        )

        valor_com_taxa = self.pricing_calculator.aplicar_taxa_fixa(valor_base, taxa_limpeza)
        valor_final = round(valor_com_taxa - desconto, 2)

        detalhe = f"Base: R$ {valor_base:.2f} | Limpeza: +R$ {taxa_limpeza:.2f} | Desconto (>=7 dias): -R$ {desconto:.2f}"
        return valor_final, detalhe