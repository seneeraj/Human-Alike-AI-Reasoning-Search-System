import chromadb
from chromadb.config import Settings
import streamlit as st

@st.cache_resource
def get_chroma_client():
    return chromadb.Client(
        Settings(
            persist_directory="db",
            anonymized_telemetry=False
        )
    )

client = get_chroma_client()

# 🔥 delete + recreate collection
def get_collection(collection_name="human_db", reset=False):

    if reset:
        try:
            client.delete_collection(name=collection_name)
        except:
            pass  # ignore if not exists

    return client.get_or_create_collection(name=collection_name)