# pixels-rag

A RAG-powered AI assistant for the Pixels game that provides accurate answers based on Discord knowledge.

## How it Works
1. User types a question in the CLI
2. Question is converted into a vector using BGE embedding model
3. System searches PostgreSQL's discord_knowledge table using vector similarity
4. Found information is formatted into context for GPT
5. Pyautogen sends context+question to GPT-4 and returns the response

## Requirements
- Python 3.9+
- PostgreSQL with pgvector extension
- OpenAI API key

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd pixels-rag
   ```

2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   - Copy `.env.example` to `.env`
   - Set your database credentials
   - Add your OpenAI API key
   - Adjust RAG settings if needed

5. Run:
   ```bash
   python3 -m src.cli
   ```

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `DB_*`: PostgreSQL connection details
- `EMBEDDING_MODEL`: Default 'BAAI/bge-small-en-v1.5'
- `SEARCH_LIMIT`: Number of relevant messages to retrieve (default: 5) 