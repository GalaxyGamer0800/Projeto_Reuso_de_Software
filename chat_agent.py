import sys
from rental_agent import RentalAgentEngineGemini

def iniciar_chat():
    print("=" * 65)
    print("   RENTAL FRAMEWORK - CHAT COM GOOGLE GEMINI REAL")
    print("=" * 65)
    print("Digite suas perguntas. Exemplos:")
    print(" - 'Quais imóveis tem em Recife?'")
    print(" - 'Reserve o APT-URB-202 para 5 dias'")
    print(" - 'Pagar a reserva 1 com PIX'")
    print("Digite 'sair' para encerrar.\n")

    agent = RentalAgentEngineGemini()

    while True:
        try:
            user_input = input("\nVocê: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["sair", "exit", "quit"]:
                print("\nEncerrando o chat.")
                break

            resposta = agent.processar_mensagem(user_input)
            print(f"\nAgente Gemini:\n{resposta}")

        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(f"\n[ERRO]: {str(e)}")

if __name__ == "__main__":
    iniciar_chat()