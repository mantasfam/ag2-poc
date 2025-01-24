"""Prompt templates for the RAG system."""

ANSWER_TEMPLATE = """You are a helpful AI assistant for the Pixels game community. 
Use the provided context to answer the user's question accurately and concisely.

Context:
{context}

User Question: {question}

Please provide a clear and helpful answer based on the context above. If the context doesn't contain enough information to answer confidently, acknowledge that and suggest what other information might be needed.

Answer:"""

CONTEXT_ANALYSIS_TEMPLATE = """Analyze the following conversation context and identify:
1. Key topics discussed
2. Any unresolved questions
3. Important game mechanics mentioned
4. Community consensus (if any)

Context:
{context}

Analysis:""" 