import streamlit as st
import re
import uuid

from modules.ingest import ingest_data
from modules.retrieve import retrieve
from modules.generate import generate_answer, generate_summary
from modules.pdf_loader import extract_text_from_pdf

# ---------------- PAGE CONFIG ----------------
st.markdown("""
<style>
/* 🔥 Reduce sidebar width */
section[data-testid="stSidebar"] {
    width: 250px !important;
}

/* 🔥 Reduce empty margin */
.block-container {
    max-width: 900px;
    padding-top: 2rem;
}

/* 🔥 Center main content */
.main {
    display: flex;
    justify-content: center;
}

/* 🔥 Improve title */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
}

/* 🔥 Subheading */
.subtitle {
    text-align: center;
    font-size: 18px;
    color: gray;
    margin-bottom: 20px;
}

/* 🔥 Section heading fix */
.section-title {
    text-align: center;
    font-size: 26px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<div class='title'>Human-Alike AI Reasoning Search System</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>*** Retrieval + Reasoning + Answer Generation with Multi-PDF & Quick Explanation ***</div>",
    unsafe_allow_html=True
)

st.divider()


# ---------------- SESSION STATE ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pdf_summary" not in st.session_state:
    st.session_state.pdf_summary = ""

if "collections" not in st.session_state:
    st.session_state.collections = []  # 🔥 multiple PDFs

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []


# ---------------- HELPER FUNCTIONS ----------------
def clean_collection_name(name):
    name = name.split(".")[0]
    name = name.replace(" ", "_")
    name = re.sub(r'[^a-zA-Z0-9_-]', '', name)
    return name[:50]


def highlight_keywords(text, query):
    words = query.split()
    for w in words:
        if len(w) > 3:
            text = re.sub(
                f"({w})",
                r"<mark>\1</mark>",
                text,
                flags=re.IGNORECASE
            )
    return text


def compute_confidence(context, query):
    score = 0
    for doc in context:
        for word in query.split():
            if word.lower() in doc.lower():
                score += 1
    return min(score / 10, 1.0)


# ---------------- SIDEBAR ----------------
st.sidebar.header("📄 Upload PDFs")

uploaded_files = st.sidebar.file_uploader(
    "Upload one or more PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

# ---------------- PROCESS MULTIPLE PDFs ----------------
if uploaded_files:
    for uploaded_file in uploaded_files:

        if uploaded_file.name not in st.session_state.uploaded_files:

            with st.spinner(f"Processing {uploaded_file.name}..."):

                text = extract_text_from_pdf(uploaded_file)
                
                # 🔥 SHOW WARNING IF FALLBACK USED
                if "ERROR" in text:
                    st.warning("⚠️ Limited reading mode (OCR not available in cloud)")                

                if text.startswith("ERROR") or text.strip() == "":
                    st.sidebar.error(f"❌ Failed: {uploaded_file.name}")
                    continue

                # Create unique collection
                base_name = clean_collection_name(uploaded_file.name)
                collection_name = f"{base_name}_{str(uuid.uuid4())[:6]}"

                ingest_data(text, collection_name)

                st.session_state.collections.append(collection_name)
                st.session_state.uploaded_files.append(uploaded_file.name)

                # Generate summary (last uploaded shown)
                summary = generate_summary(text)
                st.session_state.pdf_summary = summary

# ---------------- SHOW STATUS ----------------
if st.session_state.uploaded_files:
    st.sidebar.success("✅ Uploaded Files:")
    for f in st.session_state.uploaded_files:
        st.sidebar.write(f"• {f}")

# Reset system
if st.sidebar.button("🔄 Reset System"):
    st.session_state.clear()
    st.rerun()

# ---------------- SUMMARY ----------------
if st.session_state.get("pdf_summary"):
    st.subheader("📄 Latest Document Summary")

    with st.chat_message("assistant"):
        st.markdown(st.session_state.pdf_summary)

# ---------------- CHAT ----------------
st.markdown(
    "<div class='section-title'>💬 Ask Across All PDFs</div>",
    unsafe_allow_html=True
)
user_query = st.chat_input("Ask anything across all uploaded documents...")

if user_query:
    st.session_state.chat_history.append(("user", user_query))

    if not st.session_state.collections:
        final_answer = "⚠️ Please upload at least one PDF."

    else:
        with st.spinner("Thinking... 🤖"):

            all_context = []

            # 🔥 MULTI-PDF SEARCH
            for col in st.session_state.collections:
                context = retrieve(user_query, col)
                all_context.extend(context)

            # limit context
            all_context = all_context[:5]

            answer = generate_answer(user_query, all_context)

            # 🔥 Confidence score
            confidence = compute_confidence(all_context, user_query)

            # 🔥 Highlight sources
            sources_block = "\n\n---\n### 📄 Sources:\n"

            for i, doc in enumerate(all_context):
                highlighted = highlight_keywords(doc, user_query)

                sources_block += f"""
**🔹 Source {i+1}:**
> {highlighted}
"""

            final_answer = f"""
{answer}

---
📊 **Confidence Score:** {round(confidence * 100, 2)}%

{sources_block}
"""

    st.session_state.chat_history.append(("assistant", final_answer))


# ---------------- DISPLAY CHAT ----------------
for role, message in st.session_state.chat_history:
    with st.chat_message(role):

        if role == "assistant" and "📄 Sources" in message:

            parts = message.split("### 📄 Sources")

            # Answer
            st.markdown(parts[0], unsafe_allow_html=True)

            # Sources
            st.markdown("### 📄 Sources")

            sources = parts[1].split("🔹")

            for src in sources[1:]:
                st.info("🔹 " + src.strip())

        else:
            st.markdown(message, unsafe_allow_html=True)


# ---------------- CONTROLS ----------------
st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

with col2:
    st.write("💡 Upload multiple PDFs and ask cross-document questions!")