import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "ardael_triage.db"

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()

    finally:
        conn.close()

def init_db() -> None:

    with get_connection() as conn:
        conn.execute(
            """
                CREATE TABLE IF NOT EXISTS publicacoes_processadas(
                    hash_comunicacao TEXT PRIMARY KEY,
                    numero_processo TEXT NOT NULL,
                    data_captura TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """
        )

def ja_processada(hash_comunicacao: str) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT 1 FROM publicacoes_processadas WHERE hash_comunicacao = ?",
            (hash_comunicacao,),
        )
        return cursor.fetchone() is not None
    
def marcar_como_processada(hash_comunicacao: str, numero_processo: str) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO publicacoes_processadas
                (hash_comunicacao, numero_processo)
            VALUES (?, ?)
            """,
            (hash_comunicacao, numero_processo),
        )