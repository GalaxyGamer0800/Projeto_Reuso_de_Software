"""
Módulo: rental_core.template
Descrição: Classe Abstrata base do Framework (Padrão Template Method).
Técnica de Reuso: Framework de Software com Frozen Spots e Hotspots.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
from rental_core.components.pricing import PricingCalculatorComponent
from rental_core.components.notifier import EventNotifierComponent


class RentalBookingTemplate(ABC):
    """
    Classe Abstrata que define o esqueleto do algoritmo de reserva de imóveis.
    """

    def __init__(self):
        self.pricing_calculator = PricingCalculatorComponent()
        self.notifier = EventNotifierComponent()

    # =========================================================================
    # FROZEN SPOT (Ponto Congelado): Método Concreto Não-Sobrescritível
    # Define o fluxo invariante da reserva de imóveis.
    # =========================================================================
    def processar_reserva(self, dados_reserva: Dict[str, Any]) -> Dict[str, Any]:
        """
        Template Method: Orquestra a execução das etapas de reserva.
        """
        self.notifier.notificar_evento("INICIO_PROCESSAMENTO", "Iniciando processamento da reserva.")

        # 1. Chamada ao Hotspot 1: Validação de regras específicas da aplicação
        valido, mensagem_validacao = self.validar_regras_locacao(dados_reserva)
        if not valido:
            self.notifier.notificar_evento("RESERVA_RECUSADA", mensagem_validacao)
            return {
                "sucesso": False,
                "status": "RECUSADA",
                "motivo": mensagem_validacao
            }

        # 2. Cálculo do valor base bruto
        valor_diaria = dados_reserva.get("valor_diaria", 0.0)
        dias = dados_reserva.get("dias", 1)
        valor_base = self.pricing_calculator.calcular_valor_diarias(valor_diaria, dias)

        # 3. Chamada ao Hotspot 2: Cálculo customizado de taxas e descontos
        valor_final, detalhe_calculo = self.calcular_taxas_e_descontos(valor_base, dias)

        # 4. Finalização do fluxo
        self.notifier.notificar_evento("RESERVA_APROVADA", "Reserva aprovada e calculada com sucesso.")

        return {
            "sucesso": True,
            "status": "CONFIRMADA",
            "imovel_id": dados_reserva.get("imovel_id"),
            "hospede": dados_reserva.get("hospede"),
            "dias": dias,
            "valor_base": valor_base,
            "valor_final": valor_final,
            "detalhe_calculo": detalhe_calculo
        }

    # =========================================================================
    # HOTSPOTS (Pontos de Adaptação): Métodos Abstratos Obrigatórios
    # Devem ser implementados por cada aplicação concreta herdada do framework.
    # =========================================================================

    @abstractmethod
    def validar_regras_locacao(self, dados_reserva: Dict[str, Any]) -> Tuple[bool, str]:
        """
        HOTSPOT 1: Valida se a requisição atende às regras do tipo de imóvel.
        Deve retornar uma tupla (sucesso: bool, mensagem: str).
        """
        pass

    @abstractmethod
    def calcular_taxas_e_descontos(self, valor_base: float, dias: int) -> Tuple[float, str]:
        """
        HOTSPOT 2: Aplica acréscimos, taxas de serviço ou descontos progressivos.
        Deve retornar uma tupla (valor_final: float, descricao: str).
        """
        pass