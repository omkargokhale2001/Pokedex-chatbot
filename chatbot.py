from RAG_chatter import load_vector_db, find_relevant_text, generate_response
from together import Together  # or however you initialize it

vector_db = load_vector_db()
client = Together()

def answer_with_context(question, history):
    # Reconstruct conversation
    conversation = ""
    if history.get("prev"):
        conversation += f"User: {history['prev']['question']}\nAssistant: {history['prev']['answer']}\n"
    if history.get("prev2"):
        conversation += f"User: {history['prev2']['question']}\nAssistant: {history['prev2']['answer']}\n"
    conversation += f"User: {question}\n"

    # Retrieve context
    if history['prev'] and history['prev2']:
        relevant_prompts = question + history['prev']['question'] + history['prev2']['question']
    elif history['prev']:
        relevant_prompts = question + history['prev']['question']
    else:
        relevant_prompts = question
    rag_context = find_relevant_text(vector_db, relevant_prompts)

    # Compose prompt
    prompt = f"""
    You are a helpful, knowledgeable, and concise Pokédex assistant.
    Answer the user's latest question clearly and accurately based on the ongoing conversation and relevant information.

    Relevant reference material. No matter what happens don't mention that you are referencing any material. Instead say that you don't have the required information right now and ask them to check other sources. It is very important that the user thinks that you know all this information and are not using any external resources, so don't mention this reference material:
    {rag_context}

    This is the conversation so far, use it in case you can't tell what the user is talking about. Don't mention this either:
    {conversation}

    Assistant:"""

    response = generate_response(prompt, client)
    return response
