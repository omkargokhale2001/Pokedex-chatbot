from together import Together
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import cProfile
import time
import pyttsx3

def generate_response(prompt, client):
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def load_vector_db():
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local("faiss_pokemon", embeddings=embedding, allow_dangerous_deserialization=True)

def find_relevant_text(db, prompt, k=5):
    results = db.similarity_search(prompt, k)
    ans = ""
    for i in range(k):
        ans+=f"Part {i+1}:\n" + str(results[i])
    return ans


def chat():
    start = time.time()
    client = Together()
    end = time.time()
    print("Time to get client:", end-start)
    start = time.time()
    vector_db = load_vector_db()
    end = time.time()
    print("Time to load db:", end-start)
    print("Database loaded...")
    history = [None, None]
    engine = pyttsx3.init()
    while True:
        question = input("Enter your question: ")
        if question=="quit":
            print('Thank you!')
            break
        conversation = ""
        start = time.time()
        rag_context = find_relevant_text(vector_db, question + conversation)
        end = time.time()
        print("Time to pull rag context:", end-start)
        # Format conversation as a back-and-forth history
        if history[1]:
            conversation += f"User: {history[1]['question']}\nAssistant: {history[1]['answer']}\n"
        if history[0]:
            conversation += f"User: {history[0]['question']}\nAssistant: {history[0]['answer']}\n"
        conversation += f"User: {question}\n"

        # Final prompt with context included like retrieved notes
        prompt = f"""
        You are a helpful, knowledgeable, and concise Pokédex assistant.
        Answer the user's latest question clearly and accurately based on the ongoing conversation and relevant information.

        Relevant reference material. No matter what happens don't mention that you are referencing any material:
        {rag_context}

        This is the conversation so far, use it in case you can't tell what the user is talking about. Don't mention this either:
        {conversation}

        Assistant:"""
        
        start = time.time()
        response = generate_response(prompt, client)
        end = time.time()
        print("Time to pull rag context:", end-start)
        temp = history[0]
        history[0] = {"question": question, "answer": response}
        history[1] = temp
        print(response)
        engine.say(response)
        engine.runAndWait()


if __name__ == "__main__":
    chat()