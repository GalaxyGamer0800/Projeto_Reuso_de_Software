# 🏢 RentalFramework

**Um Framework Extensível baseado em Microsserviços, Componentes de Software e Agentes IA para Sistemas de Gerenciamento de Aluguel de Imóveis.**

---

## 📌 Visão Geral

O **RentalFramework** é uma infraestrutura de software reutilizável desenvolvida em Python para o domínio de locação de imóveis (residenciais, urbanos e por temporada).

O projeto resolve a variação constante de regras tarifárias e políticas de restrição do mercado imobiliário mantendo a estrutura fundamental do ciclo de vida de uma locação (consulta de disponibilidade, reserva e liquidação financeira) estritamente invariante, oferecendo interfaces de interação tanto via Web (**Streamlit**) quanto via Terminal (**CLI**) orquestradas por Inteligência Artificial.

---

## 🏗️ Padrões de Projeto e Técnicas de Reúso Aplicadas

* **Framework Orientado a Objetos (*Template Method* - GoF):**
  * **Frozen Spot (Ponto Congelado):** O fluxo invariante da reserva é orquestrado pela classe abstrata base `RentalBookingTemplate`, garantindo reutilização *white-box*.
  * **Hotspots (Pontos de Flexibilização):** Métodos abstratos obrigatoriamente implementados por aplicações concretas (`UrbanRentBooking`, `BeachHouseRentBooking`) para personalizar regras de precificação e restrições.
* **Arquitetura de Microsserviços (Reúso *Black-box*):**
  * Desacoplamento dos domínios em serviços REST autônomos em FastAPI, cada um com persistência SQLite isolada (*Property Service*, *Booking Service* e *Payment Service*).
* **API Gateway (Padrão *Facade* - GoF):**
  * Ponto único de entrada (Porta `8000`) utilizando o cliente `httpx` (`127.0.0.1`) como proxy reverso para abstrair a complexidade da rede e rotear chamadas.
* **Componentes de Software Autônomos (CBSE):**
  * Módulos utilitários independentes (`PricingCalculatorComponent` e `EventNotifierComponent`) altamente coesos e sem acoplamento de estado.
* **Agente de IA Autônomo (*Agentic AI* & *Tool Calling*):**
  * Assistente virtual integrado ao **Google Gemini (`google-genai`)** com *Tool Calling* nativo, rotação automática de modelos e *fallback* determinístico local para alta disponibilidade, interpretando pedidos em linguagem natural e acionando os microsserviços via API Gateway.

---

## 📂 Estrutura do Repositório

```text
Projeto_Reuso_de_Software/
├── applications/               # Aplicações Concretas (Hotspots efetivados)
│   ├── __init__.py
│   ├── beach_rent.py           # Aplicação para Aluguel de Temporada/Praia
│   └── urban_rent.py           # Aplicação para Aluguel Urbano por Diária
├── rental_core/                # Núcleo do Framework de Reúso
│   ├── __init__.py
│   ├── components/             # Componentes Utilitários (CBSE)
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
├── app.py                      # Interface Web Interativa (Streamlit)
├── chat_agent.py               # Interface Conversacional via Terminal (CLI)
├── rental_agent.py             # Engine do Agente IA (Gemini Tool Calling + Fallback)
├── test_agent.py               # Testes End-to-End (E2E) da IA
├── test_framework.py           # Testes Unitários do Framework Core
└── test_microservices.py       # Testes de Integração via API Gateway
```

---

## 🛠️ Pré-requisitos e Instalação

### Pré-requisitos
* **Python 3.10+** (recomendado Python 3.11 ou superior)
* **Pip** (gerenciador de pacotes do Python)
* Chave de API do Google Gemini (`GEMINI_API_KEY`) — *opcional, pois o agente conta com modo de contingência determinístico local.*

### 1. Clonar o Repositório
```bash
git clone [https://github.com/GalaxyGamer0800/Projeto_Reuso_de_Software.git](https://github.com/GalaxyGamer0800/Projeto_Reuso_de_Software.git)
cd Projeto_Reuso_de_Software
```

### 2. Instalar Dependências
Crie um ambiente virtual (recomendado) e instale todas as bibliotecas necessárias:

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar no Windows:
venv\Scripts\activate
# Ativar no Linux/macOS:
source venv/bin/activate

# Instalação dos pacotes
pip install fastapi uvicorn httpx pydantic google-genai streamlit
```

### 3. Configurar a Chave de API do Gemini (Opcional)
Defina a variável de ambiente no terminal antes de iniciar o agente ou informe-a diretamente na barra lateral da interface Streamlit:

```powershell
# No Windows (PowerShell):
$env:GEMINI_API_KEY="sua_chave_aqui"
```

---

## 🚀 Como Executar o Ecossistema

Para colocar o ecossistema distribuído em funcionamento, abra **4 terminais paralelos** para os serviços de backend e **1 terminal adicional** para a interface ou testes.

### Passo 1: Inicializar os Serviços (Terminais 1 a 4)

* **Terminal 1 — Property Service (Porta 8001):**
  ```bash
  python -m uvicorn services.property_service.main:app --port 8001 --reload
  ```
* **Terminal 2 — Booking Service (Porta 8002):**
  ```bash
  python -m uvicorn services.booking_service.main:app --port 8002 --reload
  ```
* **Terminal 3 — Payment Service (Porta 8003):**
  ```bash
  python -m uvicorn services.payment_service.main:app --port 8003 --reload
  ```
* **Terminal 4 — API Gateway (Porta 8000):**
  ```bash
  python -m uvicorn services.api_gateway.main:app --port 8000 --reload
  ```

### Passo 2: Executar a Interface ou Baterias de Testes (Terminal 5)

#### 🌐 Interface Web Interativa (Streamlit)
Inicia a aplicação gráfica conversacional no navegador (`http://localhost:8501`):
```bash
streamlit run app.py
```

#### 💬 Chat Conversacional Interativo (CLI)
Interaja diretamente em linguagem natural pelo terminal:
```bash
python chat_agent.py
```

**Exemplos de comandos para testar no Chat (Web ou CLI):**
1. `"Buscar imóveis disponíveis em Recife"`
2. `"Quero reservar o APT-URB-202 para Rodrigo Álvaro, 3 hóspedes, 7 dias, perfil urban"`
3. `"Realizar o pagamento dessa reserva via PIX"`

#### 🟢 Scripts Automatizados de Validação
* **Teste Unitário do Framework Core (*Template Method*):**
  ```bash
  python test_framework.py
  ```
* **Teste Integrado de Microsserviços via API Gateway:**
  ```bash
  python test_microservices.py
  ```
* **Teste End-to-End (E2E) do Agente Inteligente de IA:**
  ```bash
  python test_agent.py
  ```

---

## 👨‍💻 Guia do Desenvolvedor: Criando uma Nova Aplicação

Uma das principais vantagens do **RentalFramework** é a rapidez na criação de novas modalidades de aluguel reutilizando toda a lógica de controle (*Frozen Spot*) e os componentes financeiros.

Para criar uma nova aplicação (exemplo: `MountainRentBooking` para chalés de montanha):

### 1. Crie o arquivo da sua aplicação em `applications/mountain_rent.py`:

```python
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
```

### 2. Instancie e utilize sem duplicar código:

```python
if __name__ == "__main__":
    app = MountainRentBooking()
    resultado = app.processar_reserva({
        "imovel_id": "CHALE-01",
        "hospede": "Mariana",
        "dias": 3,
        "valor_diaria": 250.0
    })
    print(resultado)
```
