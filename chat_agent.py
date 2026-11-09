"""
Módulo: chat_agent
Descrição: Interface em linha de comando (CLI) para interação interativa com o Agente de IA.
Técnica: Interactive CLI / Agent Interface
"""

import sys
from rental_agent import RentalAgentEngine


def iniciar_chat():
    print("=" * 65)
    print("       RENTAL FRAMEWORK - ASSISTENTE VIRTUAL DE RESERVAS")
    print("=" * 65)
    print("Digite suas perguntas ou comandos em linguagem natural.")
    print("Exemplos:")
    print(" - 'Buscar imóveis em Recife'")
    print(" - 'Quero reservar o imóvel APT-URB-202'")
    print(" - 'Efetuar pagamento via PIX'")
    print("Digite 'sair' para encerrar a sessão.\n")

    agent = RentalAgentEngine()

    while True:
        try:
            user_input = input("\nVocê: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["sair", "exit", "quit"]:
                print("\nEncerrando sessão do assistente. Até logo!")
                break

            resposta = agent.processar_mensagem(user_input)
            print(f"\nAgente IA:\n{resposta}")

        except KeyboardInterrupt:
            print("\n\nSessão encerrada pelo usuário.")
            sys.exit(0)
        except Exception as e:
            print(f"\n[ERRO] Falha ao processar mensagem: {str(e)}")


if __name__ == "__main__":
    iniciar_chat()