"""
Módulo: services.property_service.main
Descrição: Microsserviço REST para gestão do catálogo de imóveis.
Tecnologia: FastAPI + SQLite (Banco isolado: property.db)
Porta: 8001
"""

import sqlite3
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI(title="Property Service", version="1.0.0")

DB_FILE = "property.db"


def init_db():
    """Inicializa a tabela de imóveis na base de dados isolada."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            cidade TEXT NOT NULL,
            tipo TEXT NOT NULL,
            capacidade INTEGER NOT NULL,
            preco_diaria REAL NOT NULL,
            disponivel INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()


@app.on_event("startup")
def startup_event():
    init_db()


# Schemas Pydantic para validação das requisições
class PropertyCreate(BaseModel):
    id: str
    titulo: str
    cidade: str
    tipo: str
    capacidade: int
    preco_diaria: float


class PropertyResponse(PropertyCreate):
    disponivel: bool


@app.post("/properties", response_model=PropertyResponse, status_code=201)
def cadastrar_imovel(imovel: PropertyCreate):
    """Cadastra um novo imóvel no catálogo."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO properties (id, titulo, cidade, tipo, capacidade, preco_diaria, disponivel)
            VALUES (?, ?, ?, ?, ?, ?, 1)
            """,
            (imovel.id, imovel.titulo, imovel.cidade, imovel.tipo, imovel.capacidade, imovel.preco_diaria)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Imóvel com este ID já cadastrado.")
    conn.close()

    return {**imovel.dict(), "disponivel": True}


@app.get("/properties", response_model=List[PropertyResponse])
def listar_imoveis(cidade: Optional[str] = Query(None)):
    """Lista todos os imóveis cadastrados, com filtro opcional por cidade."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    if cidade:
        cursor.execute("SELECT id, titulo, cidade, tipo, capacidade, preco_diaria, disponivel FROM properties WHERE LOWER(cidade) = LOWER(?)", (cidade,))
    else:
        cursor.execute("SELECT id, titulo, cidade, tipo, capacidade, preco_diaria, disponivel FROM properties")

    rows = cursor.fetchall()
    conn.close()

    imoveis = []
    for row in rows:
        imoveis.append({
            "id": row[0],
            "titulo": row[1],
            "cidade": row[2],
            "tipo": row[3],
            "capacidade": row[4],
            "preco_diaria": row[5],
            "disponivel": bool(row[6])
        })
    return imoveis


@app.get("/properties/{property_id}", response_model=PropertyResponse)
def obter_imovel(property_id: str):
    """Obtém os detalhes de um imóvel específico pelo ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, cidade, tipo, capacidade, preco_diaria, disponivel FROM properties WHERE id = ?", (property_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado.")

    return {
        "id": row[0],
        "titulo": row[1],
        "cidade": row[2],
        "tipo": row[3],
        "capacidade": row[4],
        "preco_diaria": row[5],
        "disponivel": bool(row[6])
    }