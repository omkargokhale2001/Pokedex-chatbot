# Pokedex Chatbot

This project is a **Pokédex chatbot** powered by the **Llama 3.3 70B Instruct** model via the **Together API**. I've implemented **RAG (Retrieval-Augmented Generation)** using a **FAISS**-based vector database and **HuggingFace embeddings**. The data used for this project was scraped from **Bulbapedia**. While it's not perfect, I created this project as an experiment to apply RAG in a fun, engaging way.

### Getting Started

To run the project, it's recommended to use a **virtual environment** to manage dependencies. I’ve found that **Python 3.10** works best for this code, but feel free to experiment with other versions.

### Setup Instructions:

1. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```

3. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   python app.py
   ```
5. Use your together ai API key or replace the generate_response() function with your own model inference.
   ```bash
   export TOGETHER_API_KEY=<your_api_key>
   ```

### Notes

- The `requirements.txt` file is included to simplify the setup process.
- While the project is still a work in progress, it serves as a fun and practical way to explore RAG and integrate machine learning models into a chatbot.

Feel free to experiment and make improvements!
