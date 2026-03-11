import chromadb
from openai import OpenAI

# Initialize local Vector DB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="research_papers")
client = OpenAI(api_key="your_groq_api_key", base_url="https://api.groq.com/openai/v1")

async def vectorize_paper(paper_id: str, text: str):
    """Chunks and stores paper text for AI retrieval"""
    # Simple chunking logic
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"{paper_id}_{i}"],
            metadatas=[{"paper_id": paper_id}]
        )

async def ask_ai(question: str, workspace_id: str):
    """Retrieves context and generates an answer using Llama 3.3"""
    # 1. Retrieve relevant paper chunks
    results = collection.query(query_texts=[question], n_results=3)
    context = "\n".join(results['documents'][0])
    
    # 2. Generate response with Llama 3.3
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"Use this context to answer: {context}"},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content