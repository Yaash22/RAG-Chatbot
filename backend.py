import os
import sqlite3
import openai
import numpy as np
import faiss

# Initialize OpenAI client
openai.api_type = "azure"
openai.api_key = "d2323ce0232940d98649e66d446ddec3"
openai.api_base = "https://newopenairnd.openai.azure.com/"
openai.api_version = "2023-09-15-preview"

TEXT_FILE_PATH = os.path.join(os.getcwd(), 'data', 'context.txt')
DB_PATH = 'chat_history.db'
EMBEDDING_DIMENSION = 1536

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            user_question TEXT,
            bot_answer TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(user_id, user_question, bot_answer):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO chat_history (user_id, user_question, bot_answer) VALUES (?, ?, ?)', (user_id, user_question, bot_answer))
    conn.commit()
    conn.close()

def load_from_db(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT user_question, bot_answer FROM chat_history WHERE user_id = ?', (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def split_text_into_chunks(text, chunk_size=2000, overlap=200):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks

def generate_embeddings(text_chunks):
    embeddings = []
    for chunk in text_chunks:
        try:
            response = openai.Embedding.create(
                input=chunk,
                engine="text-embedding-ada-002"
            )
            embeddings.append(response['data'][0]['embedding'])
        except Exception as e:
            print(f"Error generating embedding for chunk: {chunk}")
            print(f"Error details: {e}")
            raise
    return embeddings

def build_faiss_index(embeddings, dimension):
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    return index

def retrieve_document(query, index, corpus, all_embeddings):
    try:
        query_embedding = generate_embeddings([query])[0]
    except Exception as e:
        print(f"Error generating embedding for query: {query}")
        print(f"Error details: {e}")
        raise
    query_vector = np.array([query_embedding]).astype('float32')
    distances, indices = index.search(query_vector, k=3)  # Retrieve top 3 documents
    return [corpus[i] for i in indices[0]]

def generate_response(query, context):
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    
    try:
        response = openai.ChatCompletion.create(
            engine="chatgp35test",
            messages=[
                {"role": "system", "content": "You are a very helpful AI assistant that answers questions based on the given context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error generating response for query: {query} with context: {context}")
        print(f"Error details: {e}")
        raise

def process_query(prompt):
    # Read the text file and process
    original_text = read_text_file(TEXT_FILE_PATH)
    chunks = split_text_into_chunks(original_text)

    # Generate embeddings for chunks
    embeddings = generate_embeddings(chunks)

    # Build FAISS index
    index = build_faiss_index(embeddings, EMBEDDING_DIMENSION)

    # Retrieve relevant documents
    relevant_chunks = retrieve_document(prompt, index, chunks, embeddings)
    context = "\n".join(relevant_chunks)

    # Generate response
    bot_response = generate_response(prompt, context)
    
    return bot_response