"""
Módulo: rental_core.components.pricing
Descrição: Componente reutilizável para cálculos financeiros de reservas de imóveis.
Técnica de Reuso: Componente de Software (CBSE)
"""
class PricingCalculatorComponent:
    """
    Componente responsável por centralizar as operações de cálculo de valores de aluguel,
    aplicação de taxas administrativas e concessão de descontos progressivos.
    """

    @staticmethod
    def calcular_valor_diarias(preco_diaria: float, dias: int) -> float:
        """Calcula o valor base bruto multiplicando a diária pelo número de dias."""
        if dias <= 0:
            raise ValueError("A quantidade de dias deve ser maior que zero.")
        return round(preco_diaria * dias, 2)

    @staticmethod
    def calcular_desconto_progressivo(valor_base: float, dias: int, dias_minimos: int, percentual_desconto: float) -> float:
        """
        Aplica um desconto percentual caso o total de dias atinja ou supere o mínimo estipulado.
        Retorna o valor do desconto calculado.
        """
        if dias >= dias_minimos:
            desconto = valor_base * (percentual_desconto / 100.0)
            return round(desconto, 2)
        return 0.0

    @staticmethod
    def aplicar_taxa_fixa(valor_base: float, taxa: float) -> float:
        """Adiciona uma taxa fixa (ex: taxa de limpeza, taxa de serviço) ao subtotal."""
        if taxa < 0:
            raise ValueError("A taxa não pode ter valor negativo.")
        return round(valor_base + taxa, 2)