"""
Script de teste direto para validar o Agente Gemini + Tool Calling via API Gateway.
"""
from rental_agent import RentalAgentEngineGemini

def testar_agente():
    print("=" * 60)
    print("INICIANDO TESTE COM GOOGLE GEMINI REAL + TOOL CALLING")
    print("=" * 60)

    # Instancia a engine do Gemini
    agent = RentalAgentEngineGemini()

    # Teste 1: Intenção de Busca
    prompt1 = "Quero buscar imóveis disponíveis em Recife"
    print(f"\n[USUÁRIO]: {prompt1}")
    resposta1 = agent.processar_mensagem(prompt1)
    print(f"[GEMINI]:\n{resposta1}")

    # Teste 2: Intenção de Reserva
    prompt2 = "Gostaria de reservar o imóvel APT-URB-202 por 7 dias"
    print(f"\n[USUÁRIO]: {prompt2}")
    resposta2 = agent.processar_mensagem(prompt2)
    print(f"[GEMINI]:\n{resposta2}")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    testar_agente()