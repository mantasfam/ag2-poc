"""Database connection and query helpers with read-only access."""
import os
from typing import List, Dict
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sentence_transformers import SentenceTransformer

load_dotenv()

class DBConnection:
    def __init__(self):
        self.engine = get_db_engine()
        self.model = get_embedding_model()

    def get_relevant_messages(self, query: str, limit: int = 5) -> List[Dict]:
        """Get messages relevant to the query using vector similarity search."""
        try:
            # Get embeddings for query
            query_embedding = self.model.encode(query, normalize_embeddings=True)
            
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("""
                        WITH query_embedding AS (
                            SELECT CAST(:embedding AS vector) as qemb
                        )
                        SELECT 
                            content,
                            author_name as username,
                            timestamp,
                            embedding <=> qemb as distance
                        FROM discord_messages, query_embedding
                        WHERE embedding IS NOT NULL
                        ORDER BY distance
                        LIMIT :limit
                    """),
                    {
                        "embedding": query_embedding.tolist(),
                        "limit": limit
                    }
                )
                
                return [
                    {
                        "message": row.content,
                        "user": row.username,
                        "timestamp": row.timestamp,
                        "relevance": 1 - row.distance  # Convert distance to relevance
                    }
                    for row in result
                ]
                
        except Exception as e:
            print(f"Database error: {str(e)}")
            return []

def get_db_engine() -> Engine:
    """Create a read-only SQLAlchemy engine."""
    connection_string = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    return create_engine(connection_string, pool_pre_ping=True, pool_size=5)

def get_embedding_model():
    """Get the embedding model specified in env."""
    model_name = os.getenv('EMBEDDING_MODEL', 'BAAI/bge-small-en-v1.5')
    device = os.getenv('EMBEDDING_DEVICE', 'cpu')
    return SentenceTransformer(model_name, device=device)

def search_similar_messages(query: str, limit: int = 5) -> List[dict]:
    """First search messages, then enrich with knowledge if available."""
    model = get_embedding_model()
    query_embedding = model.encode(query, normalize_embeddings=True)
    
    engine = get_db_engine()
    with engine.connect() as conn:
        # First find relevant messages
        message_result = conn.execute(
            text("""
                WITH query_embedding AS (
                    SELECT CAST(:embedding AS vector) as qemb
                )
                SELECT 
                    m.id,
                    m.content,
                    m.author_name,
                    m.timestamp,
                    m.embedding <=> qemb as distance
                FROM discord_messages m, query_embedding
                WHERE m.embedding IS NOT NULL
                ORDER BY distance
                LIMIT :limit
            """),
            {
                "embedding": query_embedding.tolist(),
                "limit": limit
            }
        )
        
        messages = []
        for row in message_result:
            # Try to find related knowledge
            knowledge = get_related_knowledge(conn, str(row.id))  # Convert ID to string
            messages.append({
                "content": row.content,
                "author": row.author_name,
                "timestamp": row.timestamp,
                "distance": row.distance,
                "knowledge": knowledge if knowledge else None
            })
                
        return messages

def get_related_knowledge(conn, message_id: str) -> str:
    """Find curated knowledge related to a message."""
    result = conn.execute(
        text("""
            SELECT content
            FROM discord_knowledge
            WHERE CAST(:msg_id AS TEXT) = ANY(CAST(source_message_ids AS TEXT[]))
        """),
        {"msg_id": message_id}
    )
    row = result.first()
    return row.content if row else None

def get_message_context(conn, message_id: int, context_size: int = 2):
    """Get surrounding messages for additional context."""
    result = conn.execute(
        text("""
            SELECT content, author_name, timestamp
            FROM discord_messages 
            WHERE id = :msg_id
            OR id IN (
                -- Get n messages before and after
                SELECT id FROM discord_messages
                WHERE timestamp BETWEEN 
                    (SELECT timestamp - interval '5 minutes' FROM discord_messages WHERE id = :msg_id)
                    AND
                    (SELECT timestamp + interval '5 minutes' FROM discord_messages WHERE id = :msg_id)
                ORDER BY timestamp
                LIMIT :context_size
            )
            ORDER BY timestamp
        """),
        {
            "msg_id": message_id,
            "context_size": context_size * 2
        }
    )
    return list(result) 