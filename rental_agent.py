"""
Módulo: rental_agent
Descrição: Agente Inteligente para orquestração de chamadas de ferramentas e resolução de intenções em linguagem natural.
Técnica: Agent Engine / Intent Parsing / Tool Calling
"""

import re
from typing import Dict, Any
from agent_tools import buscar_imoveis_tool, criar_reserva_tool, processar_pagamento_tool


class RentalAgentEngine:
    """
    Engine central do Agente de IA responsável pelo processamento de linguagem natural
    e execução automatizada de ferramentas integradas ao API Gateway.
    """

    def __init__(self):
        self.contexto_sessao: Dict[str, Any] = {}

    def processar_mensagem(self, mensagem_usuario: str) -> str:
        """
        Analisa a mensagem recebida, identifica a intenção e executa a ferramenta correspondente.
        """
        texto = mensagem_usuario.lower()

        # Intenção 1: Pagamento de reserva
        if "pagar" in texto or "pagamento" in texto or "pix" in texto:
            return self._executar_intencao_pagamento(texto)

        # Intenção 2: Criação de reserva
        elif "reservar" in texto or "alugar" in texto or "reserva" in texto:
            return self._executar_intencao_reserva(texto)

        # Intenção 3: Busca/Consulta de imóveis
        elif "buscar" in texto or "listar" in texto or "imóveis" in texto or "imoveis" in texto or "procurar" in texto:
            return self._executar_intencao_busca(texto)

        # Fallback para saudações ou dúvidas gerais
        else:
            return (
                "Olá! Sou o assistente virtual do RentalFramework. "
                "Como posso ajudar? Você pode me pedir para buscar imóveis em uma cidade, "
                "efetuar uma reserva ou processar o pagamento de uma reserva existente."
            )

    def _executar_intencao_busca(self, texto: str) -> str:
        cidade = None
        palavras = texto.split()
        if "em" in palavras:
            idx = palavras.index("em")
            if idx + 1 < len(palavras):
                cidade = palavras[idx + 1].strip(".,?!")

        resultado = buscar_imoveis_tool(cidade=cidade)
        if not resultado.get("sucesso"):
            return f"Não foi possível consultar os imóveis: {resultado.get('erro')}"

        imoveis = resultado.get("imoveis", [])
        if not imoveis:
            return f"Nenhum imóvel encontrado{f' para a cidade {cidade.title()}' if cidade else ''}."

        resposta = f"Encontrei {len(imoveis)} imóvel(is) disponível(is):\n"
        for imp in imoveis:
            resposta += f"- ID: {imp['id']} | {imp['titulo']} ({imp['cidade']}) - Diária: R$ {imp['preco_diaria']:.2f}\n"
        return resposta

    def _executar_intencao_reserva(self, texto: str) -> str:
        # Extração simples de ID de imóvel se informado no formato APT-XXX ou CASA-XXX
        match_id = re.search(r'(apt-[a-z0-9-]+|casa-[a-z0-9-]+)', texto)
        imovel_id = match_id.group(1).upper() if match_id else "APT-URB-202"

        tipo_app = "beach" if "praia" in texto or "casa" in texto else "urban"
        dias = 7 if tipo_app == "urban" else 14

        resultado = criar_reserva_tool(
            imovel_id=imovel_id,
            hospede="Cliente Agente IA",
            tipo_aplicacao=tipo_app,
            dias=dias,
            hospedes=2,
            valor_diaria=200.0
        )

        if not resultado.get("sucesso"):
            return f"A reserva não pôde ser concluída: {resultado.get('erro')}"

        reserva = resultado["reserva"]
        self.contexto_sessao["ultima_reserva_id"] = reserva["id"]
        self.contexto_sessao["ultimo_valor"] = reserva["valor_final"]

        return (
            f"Reserva #{reserva['id']} confirmada com sucesso!\n"
            f"Imóvel: {reserva['imovel_id']} | Dias: {reserva['dias']}\n"
            f"Cálculo: {reserva['detalhe_calculo']}\n"
            f"Valor Total Final: R$ {reserva['valor_final']:.2f}"
        )

    def _executar_intencao_pagamento(self, texto: str) -> str:
        booking_id = self.contexto_sessao.get("ultima_reserva_id", 1)
        valor = self.contexto_sessao.get("ultimo_valor", 1310.0)
        metodo = "PIX" if "pix" in texto else "CREDIT_CARD"

        resultado = processar_pagamento_tool(
            booking_id=booking_id,
            valor=valor,
            metodo_pagamento=metodo
        )

        if not resultado.get("sucesso"):
            return f"Erro ao efetuar pagamento: {resultado.get('erro')}"

        pagamento = resultado["pagamento"]
        return (
            f"Pagamento processado com sucesso!\n"
            f"Comprovante: {pagamento['comprovante_id']}\n"
            f"Reserva: #{pagamento['booking_id']} | Método: {pagamento['metodo_pagamento']}\n"
            f"Valor Liquidado: R$ {pagamento['valor']:.2f}"
        )