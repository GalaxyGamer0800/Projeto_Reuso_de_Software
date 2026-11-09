"""
Módulo: services.booking_service.main
Descrição: Microsserviço REST para gestão e criação de reservas.
Tecnologia: FastAPI + SQLite (Banco isolado: booking.db) + RentalFramework
Porta: 8002
"""

import sqlite3
import sys
import os
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Garante o carregamento dos pacotes da raiz do projeto (rental_core e applications)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from applications.urban_rent import UrbanRentBooking
from applications.beach_rent import BeachHouseRentBooking

app = FastAPI(title="Booking Service", version="1.0.0")

DB_FILE = "booking.db"


def init_db():
    """Inicializa a tabela de reservas na base de dados isolada do serviço."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            imovel_id TEXT NOT NULL,
            hospede TEXT NOT NULL,
            tipo_aplicacao TEXT NOT NULL,
            dias INTEGER NOT NULL,
            valor_final REAL NOT NULL,
            status TEXT NOT NULL,
            detalhe_calculo TEXT
        )
    """)
    conn.commit()
    conn.close()


@app.on_event("startup")
def startup_event():
    init_db()


# Schemas Pydantic
class BookingRequest(BaseModel):
    imovel_id: str
    hospede: str
    tipo_aplicacao: str  # "urban" ou "beach"
    dias: int
    hospedes: int
    valor_diaria: float


class BookingResponse(BaseModel):
    id: int
    imovel_id: str
    hospede: str
    tipo_aplicacao: str
    dias: int
    valor_final: float
    status: str
    detalhe_calculo: str


@app.post("/bookings", response_model=BookingResponse, status_code=201)
def criar_reserva(requisicao: BookingRequest):
    """
    Cria uma reserva reutilizando a lógica do RentalFramework.
    Instancia UrbanRentBooking ou BeachHouseRentBooking conforme o tipo informado.
    """
    tipo = requisicao.tipo_aplicacao.lower()
    
    if tipo == "urban":
        framework_app = UrbanRentBooking()
    elif tipo == "beach":
        framework_app = BeachHouseRentBooking()
    else:
        raise HTTPException(status_code=400, detail="Tipo de aplicação inválido. Use 'urban' ou 'beach'.")

    # Executa o Template Method (Frozen Spot) que aciona os Hotspots
    dados = requisicao.dict()
    resultado = framework_app.processar_reserva(dados)

    if not resultado.get("sucesso"):
        raise HTTPException(status_code=400, detail=resultado.get("motivo"))

    # Persiste a reserva na base isolada do microsserviço
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO bookings (imovel_id, hospede, tipo_aplicacao, dias, valor_final, status, detalhe_calculo)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            requisicao.imovel_id,
            requisicao.hospede,
            requisicao.tipo_aplicacao,
            requisicao.dias,
            resultado["valor_final"],
            resultado["status"],
            resultado["detalhe_calculo"]
        )
    )
    conn.commit()
    booking_id = cursor.lastrowid
    conn.close()

    return {
        "id": booking_id,
        "imovel_id": requisicao.imovel_id,
        "hospede": requisicao.hospede,
        "tipo_aplicacao": requisicao.tipo_aplicacao,
        "dias": requisicao.dias,
        "valor_final": resultado["valor_final"],
        "status": resultado["status"],
        "detalhe_calculo": resultado["detalhe_calculo"]
    }


@app.get("/bookings/{booking_id}", response_model=BookingResponse)
def obter_reserva(booking_id: int):
    """Obtém o status e detalhes de uma reserva cadastrada."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, imovel_id, hospede, tipo_aplicacao, dias, valor_final, status, detalhe_calculo FROM bookings WHERE id = ?",
        (booking_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Reserva não encontrada.")

    return {
        "id": row[0],
        "imovel_id": row[1],
        "hospede": row[2],
        "tipo_aplicacao": row[3],
        "dias": row[4],
        "valor_final": row[5],
        "status": row[6],
        "detalhe_calculo": row[7]
    }