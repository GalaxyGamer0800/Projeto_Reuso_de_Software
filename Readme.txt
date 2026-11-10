🏢 RentalFramework

Um Framework Extensível baseado em Microsserviços, Componentes de Software e Agentes IA para Sistemas de Gerenciamento de Aluguel de Imóveis.

📌 Visão Geral

O RentalFramework é uma infraestrutura de software reutilizável desenvolvida em Python para o domínio de locação de imóveis (residenciais, urbanos e por temporada).

O projeto resolve a variação constante de regras tarifárias e políticas de restrição do mercado imobiliário mantendo a estrutura fundamental do ciclo de vida de uma locação (consulta de disponibilidade, reserva e liquidação financeira) estritamente invariante.

🏗️ Padrões de Projeto e Técnicas de Reúso Aplicadas

Framework Orientado a Objetos (Template Method - GoF):

Frozen Spot (Ponto Congelado): O fluxo invariante da reserva é orquestrado pela classe abstrata base RentalBookingTemplate, garantindo reutilização white-box.

Hotspots (Pontos de Flexibilização): Métodos abstratos obrigatoriamente implementados por aplicações concretas (UrbanRentBooking, BeachHouseRentBooking) para personalizar regras de precificação e restrições.

Arquitetura de Microsserviços (Reúso Black-box):

Desacoplamento dos domínios em serviços REST autônomos em FastAPI, cada um com persistência SQLite isolada (Property Service, Booking Service e Payment Service).

API Gateway (Padrão Facade - GoF):

Ponto único de entrada (Porta 8000) utilizando o cliente httpx como proxy reverso para abstrair a complexidade da rede e rotear chamadas.

Componentes de Software Autônomos (CBSE):

Módulos utilitários independentes (PricingCalculatorComponent e EventNotifierComponent) altamente coesos e sem acoplamento de estado.

Agente de IA Autônomo (Agentic AI & Tool Calling):

Atendimento em linguagem natural (Broker Agent) que interpreta a intenção do usuário e invoca autonomamente as APIs do sistema via Gateway.

📂 Estrutura do Repositório

Projeto_Reuso_de_Software/
├── applications/               # Aplicações Concretas (Hotspots efetivados)
│   ├── __init__.py
│   ├── beach_rent.py           # Aplicação para Aluguel de Temporada/Praia
│   └── urban_rent.py           # Aplicação para Aluguel Urbano por Diária
├── rental_core/                # Núcleo do Framework de Reúso
│   ├── __init__.py
│   ├── components/             # Componentes Utilidades (CBSE)
│   │   ├── __init__.py
│   │   ├── notifier.py         # EventNotifierComponent (Logs e Auditoria)
│   │   └── pricing.py          # PricingCalculatorComponent (Cálculos)
│   └── template.py             # Classe Abstrata (Template Method: Frozen/Hotspots)
├── services/                   # Infraestrutura de Microsserviços REST
│   ├── __init__.py
│   ├── api_gateway/            # API Gateway / Facade (Porta 8000)
│   │   ├── __init__.py
│   │   └── main.py
│   ├── booking_service/        # Microsserviço de Reservas (Porta 8002)
│   │   ├── __init__.py
│   │   └── main.py
│   ├── payment_service/        # Microsserviço de Pagamentos (Porta 8003)
│   │   ├── __init__.py
│   │   └── main.py
│   └── property_service/       # Microsserviço de Imóveis (Porta 8001)
│       ├── __init__.py
│       └── main.py
├── agent_tools.py              # Camada de Integração / Tool Calling da IA
├── chat_agent.py               # Interface Conversacional via Terminal (CLI)
├── rental_agent.py             # Engine de Processamento de Intenções da IA
├── test_agent.py               # Testes End-to-End (E2E) da IA
├── test_framework.py           # Testes Unitários do Framework Core
└── test_microservices.py       # Testes de Integração via API Gateway


🛠️ Pré-requisitos e Instalação

Pré-requisitos

Python 3.10+ (recomendado Python 3.11 ou superior)

Pip (gerenciador de pacotes do Python)

1. Clonar o Repositório

git clone https://github.com/GalaxyGamer0800/Projeto_Reuso_de_Software.git
cd Projeto_Reuso_de_Software


2. Instalar Dependências

Crie um ambiente virtual (opcional, mas recomendado) e instale as bibliotecas necessárias:

# Opção: Criar ambiente virtual
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/macOS:
source venv/bin/activate

# Instalação dos pacotes
pip install fastapi uvicorn httpx pydantic


🚀 Como Executar o Ecossistema

Para colocar o ecossistema distribuído em funcionamento, abra 4 terminais paralelos para os serviços e 1 terminal adicional para testes/demonstração.

Passo 1: Inicializar os Serviços (Terminais 1 a 4)

Terminal 1 — Property Service (Porta 8001):

python -m uvicorn services.property_service.main:app --port 8001 --reload


Terminal 2 — Booking Service (Porta 8002):

python -m uvicorn services.booking_service.main:app --port 8002 --reload


Terminal 3 — Payment Service (Porta 8003):

python -m uvicorn services.payment_service.main:app --port 8003 --reload


Terminal 4 — API Gateway (Porta 8000):

python -m uvicorn services.api_gateway.main:app --port 8000 --reload


Passo 2: Executar Baterias de Testes e Demonstração (Terminal 5)

No quinto terminal, você pode executar os testes automatizados ou iniciar a interface conversacional:

🟢 Teste Unitário do Framework Core (Template Method)

Valida a herança e a execução dos hotspots na memória sem depender da rede:

python test_framework.py


🟢 Teste Integrado de Microsserviços via API Gateway

Valida o fluxo completo de cadastro, consulta, reserva e pagamento via porta 8000:

python test_microservices.py


🟢 Teste End-to-End (E2E) do Agente Inteligente de IA

Homologa a capacidade do agente de interpretar mensagens em linguagem natural e acionar as APIs via Tool Calling:

python test_agent.py


💬 Chat Conversacional Interativo (CLI)

Interaja diretamente em linguagem natural com o assistente do sistema:

python chat_agent.py


Exemplos de comandos para testar no Chat:

"Buscar imóveis em Recife"

"Quero reservar o imóvel APT-URB-202"

"Efetuar pagamento via PIX"

👨‍💻 Guia do Desenvolvedor: Criando uma Nova Aplicação

Uma das principais vantagens do RentalFramework é a rapidez na criação de novas modalidades de aluguel reutilizando toda a lógica de controle.

Para criar uma nova aplicação (exemplo: MountainRentBooking para chalés de montanha):

1. Crie o arquivo da sua aplicação em applications/mountain_rent.py:

from typing import Dict, Any, Tuple
from rental_core.template import RentalBookingTemplate

class MountainRentBooking(RentalBookingTemplate):
    """Aplicação concreta para aluguel de chalés de montanha."""

    def validar_regras_locacao(self, dados_reserva: Dict[str, Any]) -> Tuple[bool, str]:
        # HOTSPOT 1: Restrição específica de montanha
        if dados_reserva.get("dias", 0) < 2:
            return False, "Chalés de montanha exigem no mínimo 2 diárias."
        return True, "Validação aprovada para MountainRent."

    def calcular_taxas_e_descontos(self, valor_base: float, dias: int) -> Tuple[float, str]:
        # HOTSPOT 2: Regra tarifária com taxa de aquecimento/lenha
        taxa_aquecimento = 80.0
        
        # Reutiliza o componente de precificação para aplicar taxa fixa
        valor_final = self.pricing_calculator.aplicar_taxa_fixa(valor_base, taxa_aquecimento)
        
        detalhe = f"Base: R$ {valor_base:.2f} | Aquecimento: +R$ {taxa_aquecimento:.2f}"
        return valor_final, detalhe


2. Instancie e utilize sem duplicar código:

if __name__ == "__main__":
    app = MountainRentBooking()
    resultado = app.processar_reserva({
        "imovel_id": "CHALE-01",
        "hospede": "Mariana",
        "dias": 3,
        "valor_diaria": 250.0
    })
    print(resultado)


