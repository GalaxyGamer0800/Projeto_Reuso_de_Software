"""
Módulo: rental_agent
Descrição: Engine do Agente Inteligente com Tool Calling nativo (Google Gemini)
           e fallback determinístico local para alta disponibilidade.
"""

import os
import re
from typing import Dict, Any
from google import genai
from google.genai import types
from agent_tools import buscar_imoveis_tool, criar_reserva_tool, processar_pagamento_tool


class RentalAgentEngine:
    def __init__(self, api_key: str = None):
        self.api_key = (
            api_key
            or os.getenv("GEMINI_API_KEY")
            or "AQ.Ab8RN6Kq94yECxyLkzaA9gh8AOwF54zTw90UvNR1KxglJk03rzg"
        )
        self.contexto_sessao: Dict[str, Any] = {}

        self.tools_map = {
            "buscar_imoveis_tool": buscar_imoveis_tool,
            "criar_reserva_tool": criar_reserva_tool,
            "processar_pagamento_tool": processar_pagamento_tool
        }

        self.system_instruction = (
            "Você é o assistente virtual do RentalFramework, um ecossistema de aluguel de imóveis.\n"
            "Utilize as ferramentas fornecidas para atender aos clientes:\n"
            "1. buscar_imoveis_tool(cidade): busca imóveis disponíveis.\n"
            "2. criar_reserva_tool(imovel_id, hospede, tipo_aplicacao, dias, hospedes, valor_diaria): "
            "cria reserva onde tipo_aplicacao deve ser 'urban' ou 'beach'.\n"
            "3. processar_pagamento_tool(booking_id, valor, metodo_pagamento): "
            "liquida pagamento onde metodo_pagamento deve ser 'PIX', 'CREDIT_CARD' ou 'BOLETO'.\n"
            "Mantenha o contexto da conversa (ID do imóvel, valor da diária, ID da reserva e valor final). "
            "Se uma ferramenta retornar erro, informe o usuário sem repetir a chamada em loop."
        )

        self.modelos_candidatos = [
            "gemini-3.8-flash",
            "gemini-3.8-flash-lite",
            "gemini-3.5-flash",
            "gemini-3.0-flash"
        ]
        self.indice_modelo = 0
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None
        self.chat = (
            self._criar_sessao_chat(self.modelos_candidatos[self.indice_modelo])
            if self.client else None
        )

    def _criar_sessao_chat(self, nome_modelo: str):
        return self.client.chats.create(
            model=nome_modelo,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                tools=[buscar_imoveis_tool, criar_reserva_tool, processar_pagamento_tool],
                temperature=0.2
            )
        )

    def processar_mensagem(self, mensagem_usuario: str) -> str:
        """Processa via Gemini Tool Calling; se o servidor retornar 503, usa o parser local."""
        if not self.chat:
            return self._processar_fallback_local(mensagem_usuario)

        while self.indice_modelo < len(self.modelos_candidatos):
            try:
                response = self.chat.send_message(mensagem_usuario)

                tentativas_tool = 0
                while response.function_calls and tentativas_tool < 4:
                    tentativas_tool += 1
                    for function_call in response.function_calls:
                        func_name = function_call.name
                        func_args = function_call.args

                        if func_name in self.tools_map:
                            resultado_tool = self.tools_map[func_name](**func_args)
                            response = self.chat.send_message(
                                types.Part.from_function_response(
                                    name=func_name,
                                    response={"result": resultado_tool}
                                )
                            )
                        else:
                            return f"[Erro Agent Engine] Ferramenta '{func_name}' não encontrada."

                return response.text

            except Exception as e:
                erro_str = str(e)
                if "503" in erro_str or "404" in erro_str:
                    self.indice_modelo += 1
                    if self.indice_modelo < len(self.modelos_candidatos):
                        self.chat = self._criar_sessao_chat(self.modelos_candidatos[self.indice_modelo])
                        continue
                # Se todos os modelos estiverem com 503, aciona seu fluxo original
                return self._processar_fallback_local(mensagem_usuario)

        return self._processar_fallback_local(mensagem_usuario)

    # --- Seu fluxo original preservado como contingência local ---
    def _processar_fallback_local(self, mensagem_usuario: str) -> str:
        texto = mensagem_usuario.lower()

        if "pagar" in texto or "pagamento" in texto or "pix" in texto:
            booking_id = self.contexto_sessao.get("ultima_reserva_id", 1)
            valor = self.contexto_sessao.get("ultimo_valor", 1310.0)
            metodo = "PIX" if "pix" in texto else "CREDIT_CARD"
            resultado = processar_pagamento_tool(booking_id=booking_id, valor=valor, metodo_pagamento=metodo)
            if not resultado.get("sucesso"):
                return f"Erro ao efetuar pagamento: {resultado.get('erro')}"
            p = resultado["pagamento"]
            return (
                f"Pagamento processado com sucesso!\n"
                f"Comprovante: {p['comprovante_id']}\n"
                f"Reserva: #{p['booking_id']} | Método: {p['metodo_pagamento']}\n"
                f"Valor Liquidado: R$ {p['valor']:.2f}"
            )

        elif "reservar" in texto or "alugar" in texto or "reserva" in texto:
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
            r = resultado["reserva"]
            self.contexto_sessao["ultima_reserva_id"] = r["id"]
            self.contexto_sessao["ultimo_valor"] = r["valor_final"]
            return (
                f"Reserva #{r['id']} confirmada com sucesso!\n"
                f"Imóvel: {r['imovel_id']} | Dias: {r['dias']}\n"
                f"Cálculo: {r['detalhe_calculo']}\n"
                f"Valor Total Final: R$ {r['valor_final']:.2f}"
            )

        elif any(p in texto for p in ["buscar", "listar", "imóveis", "imoveis", "procurar"]):
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

        return (
            "Olá! Sou o assistente virtual do RentalFramework. "
            "Como posso ajudar? Você pode me pedir para buscar imóveis em uma cidade, "
            "efetuar uma reserva ou processar o pagamento de uma reserva existente."
        )


# Alias de compatibilidade
RentalAgentEngineGemini = RentalAgentEngine