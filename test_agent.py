"""
Módulo: test_agent
Descrição: Script de teste automatizado End-to-End (E2E) da camada do Agente de IA.
Técnica: E2E Integration Testing / Agent Validation
Porta Alvo: 8000 (API Gateway via agent_tools)
"""

from rental_agent import RentalAgentEngine


def executar_teste_e2e_agente():
    print("=" * 65)
    print("       TESTE END-TO-END (E2E) - AGENTE INTELIGENTE E TOOLS")
    print("=" * 65)

    agent = RentalAgentEngine()

    # Passo 1: Solicitação de busca de imóveis em linguagem natural
    prompt_1 = "Quero buscar imóveis disponíveis em Recife"
    print(f"\n[ENTRADA DO USUÁRIO]: {prompt_1}")
    resposta_1 = agent.processar_mensagem(prompt_1)
    print(f"[RESPOSTA DA IA]:\n{resposta_1}")

    # Passo 2: Solicitação de reserva em linguagem natural
    prompt_2 = "Gostaria de reservar o imóvel APT-URB-202"
    print(f"\n[ENTRADA DO USUÁRIO]: {prompt_2}")
    resposta_2 = agent.processar_mensagem(prompt_2)
    print(f"[RESPOSTA DA IA]:\n{resposta_2}")

    # Passo 3: Solicitação de pagamento via PIX em linguagem natural
    prompt_3 = "Quero efetuar o pagamento da minha reserva usando PIX"
    print(f"\n[ENTRADA DO USUÁRIO]: {prompt_3}")
    resposta_3 = agent.processar_mensagem(prompt_3)
    print(f"[RESPOSTA DA IA]:\n{resposta_3}")

    print("\n" + "=" * 65)
    print("       TESTE E2E DO AGENTE FINALIZADO COM SUCESSO!")
    print("=" * 65)


if __name__ == "__main__":
    executar_teste_e2e_agente()