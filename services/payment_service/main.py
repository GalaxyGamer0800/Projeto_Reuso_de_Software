"""
Módulo: services.payment_service.main
Descrição: Microsserviço REST para processamento e gestão de pagamentos.
Tecnologia: FastAPI + SQLite (Banco isolado: payment.db)
Porta: 8003
"""

import sqlite3
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Payment Service", version="1.0.0")

DB_FILE = "payment.db"


def init_db():
    """Inicializa a tabela de pagamentos na base de dados isolada."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER NOT NULL,
            valor REAL NOT NULL,
            metodo_pagamento TEXT NOT NULL,
            status TEXT NOT NULL,
            data_pagamento TEXT NOT NULL,
            comprovante_id TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.on_event("startup")
def startup_event():
    init_db()


# Schemas Pydantic
class PaymentRequest(BaseModel):
    booking_id: int
    valor: float
    metodo_pagamento: str  # Ex: "PIX", "CREDIT_CARD", "BOLETO"


class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    valor: float
    metodo_pagamento: str
    status: str
    data_pagamento: str
    comprovante_id: str


@app.post("/payments/process", response_model=PaymentResponse, status_code=201)
def processar_pagamento(requisicao: PaymentRequest):
    """Simula a aprovação e o processamento financeiro de uma reserva."""
    if requisicao.valor <= 0:
        raise HTTPException(status_code=400, detail="O valor do pagamento deve ser maior que zero.")

    status = "PAGO"
    data_atual = datetime.now().isoformat()
    comprovante = f"PAY-{requisicao.booking_id}-{int(datetime.now().timestamp())}"

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO payments (booking_id, valor, metodo_pagamento, status, data_pagamento, comprovante_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            requisicao.booking_id,
            requisicao.valor,
            requisicao.metodo_pagamento.upper(),
            status,
            data_atual,
            comprovante
        )
    )
    conn.commit()
    payment_id = cursor.lastrowid
    conn.close()

    return {
        "id": payment_id,
        "booking_id": requisicao.booking_id,
        "valor": requisicao.valor,
        "metodo_pagamento": requisicao.metodo_pagamento.upper(),
        "status": status,
        "data_pagamento": data_atual,
        "comprovante_id": comprovante
    }


@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def obter_pagamento(payment_id: int):
    """Consulta o registro e o comprovante de um pagamento pelo ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, booking_id, valor, metodo_pagamento, status, data_pagamento, comprovante_id FROM payments WHERE id = ?",
        (payment_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Registro de pagamento não encontrado.")

    return {
        "id": row[0],
        "booking_id": row[1],
        "valor": row[2],
        "metodo_pagamento": row[3],
        "status": row[4],
        "data_pagamento": row[5],
        "comprovante_id": row[6]
    }