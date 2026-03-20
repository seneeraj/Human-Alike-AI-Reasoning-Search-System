## README

```markdown
# 🧠 Human-Alike AI Reasoning Search System

An advanced **AI-powered document analysis system** that combines:

👉 Retrieval (Vector Search)  
👉 Reasoning (LLM Intelligence)  
👉 Answer Generation  

Supports **Multi-PDF search, explainable AI, and smart insights**.

---

## 🚀 Key Features

- 📄 Upload multiple PDFs
- 🔍 Semantic search using embeddings
- 🧠 AI-powered reasoning (Mistral API)
- 💬 ChatGPT-style interface
- 📊 Confidence score for answers
- 📌 Highlighted sources from documents
- 🧾 Auto summary after upload
- 🔄 Multi-document querying (no reset needed)
- ⚠️ Smart fallback (works even without OCR)

---

## 🧠 System Architecture

```

PDF Upload
↓
Text Extraction (OCR / pypdf fallback)
↓
Chunking
↓
Embeddings (Sentence Transformers)
↓
Vector DB (ChromaDB)
↓
User Query
↓
Semantic Retrieval
↓
LLM Reasoning (Mistral)
↓
Answer + Sources + Confidence Score

````

---

## 📸 Demo (Example Use Cases)

Try asking:

- What are the key insights?
- Which supplier is risky?
- Summarize the document
- What trends are visible?

---

## ⚙️ Installation (Local Setup)

### 1. Clone Repository

```bash
git clone https://github.com/your-username/human-alike-ai-reasoning-search-system.git
cd human-alike-ai-reasoning-search-system
````

---

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Setup Environment Variables

Create `.env` file:

```env
MISTRAL_API_KEY=your_api_key_here
```

---

### 5. Run Application

```bash
streamlit run streamlit_app.py
```

---

## 🌍 Streamlit Cloud Deployment

* Ensure `streamlit_app.py` is in root
* Use provided `requirements.txt`
* Include `.streamlit/config.toml`
* Do NOT upload `.env`

---

## 📂 Project Structure

```
Human-Alike-AI-Reasoning-Search-System/
│
├── streamlit_app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── modules/
│   ├── ingest.py
│   ├── retrieve.py
│   ├── generate.py
│   ├── embed.py
│   ├── db.py
│   ├── pdf_loader.py
│
├── .streamlit/
│   └── config.toml
│
├── .env.example
```

---

## ⚠️ Limitations

* OCR may not work on Streamlit Cloud
* Very large PDFs (>50 pages) may slow processing
* Accuracy depends on document quality

---

## 🧠 Tech Stack

* **Frontend:** Streamlit
* **Vector Database:** ChromaDB
* **Embeddings:** Sentence Transformers
* **LLM:** Mistral API
* **PDF Processing:** pypdf / OCR

---

## 🔐 Environment Variables

```
MISTRAL_API_KEY=your_api_key_here
```

---

## 📜 License

MIT License

---

## 👨‍💻 Author

**Neeraj Bhatia**
AI & Data Science Enthusiast 🚀

---

## ⭐ Support

If you like this project, please give it a ⭐ on GitHub!

```

