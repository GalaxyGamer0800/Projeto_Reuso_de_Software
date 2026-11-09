"""
Módulo: rental_core.components.notifier
Descrição: Componente reutilizável para emissão de eventos e logs de auditoria do sistema.
Técnica de Reuso: Componente de Software (CBSE)
"""

from datetime import datetime
from typing import List, Dict, Any

class EventNotifierComponent:
    """
    Componente responsável pelo registro e emissão de eventos operacionais
    ocorridos durante o processamento de reservas.
    """

    def __init__(self):
        self._historico_eventos: List[Dict[str, Any]] = []

    def notificar_evento(self, tipo_evento: str, mensagem: str, detalhes: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Registra um novo evento no histórico do sistema com timestamp automático.
        """
        evento = {
            "timestamp": datetime.now().isoformat(),
            "tipo_evento": tipo_evento.upper(),
            "mensagem": mensagem,
            "detalhes": detalhes or {}
        }
        self._historico_eventos.append(evento)
        # Exibe o log formatado no console para acompanhamento
        print(f"[{evento['timestamp']}] [{evento['tipo_evento']}] - {mensagem}")
        return evento

    def obter_historico(self) -> List[Dict[str, Any]]:
        """Retorna a lista completa de eventos registrados no componente."""
        return self._historico_eventos.copy()