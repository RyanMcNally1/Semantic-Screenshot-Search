import streamlit as st
from indexer import scan_folder, save_index
from search import load_index, prepare_embeddings, transform, search_images
from sentence_transformers import SentenceTransformer
from pathlib import Path

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

def main():
    st.set_page_config(
        page_title="Semantic Screenshot Search",
        page_icon="🔎",
        layout="centered"
    )

    ##Custom styling
    st.markdown("""
        <style>
        .stApp {
            background-color: #0F172A;
            color: #F8FAFC;
        }

        .block-container {
            max-width: 950px;
            padding-top: 3rem;
            padding-bottom: 3rem;
        }

        h1 {
            color: #F8FAFC;
            font-weight: 700;
            letter-spacing: -1px;
        }

        h3 {
            color: #93C5FD;
            margin-top: 1rem;
        }

        div.stButton > button {
            background-color: #2563EB;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1.5rem;
            font-weight: 600;
        }

        div.stButton > button:hover {
            background-color: #1D4ED8;
            color: white;
            border: none;
        }

        div[data-testid="stTextInput"] input {
            background-color: #1E293B;
            color: white;
            border-radius: 8px;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 12px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🔎 Semantic Screenshot Search")
    st.write("Find screenshots by describing what you remember seeing or reading, without needing to know the filename.")

    st.divider()

    transformer = load_model()

    ##Indexing folder
    st.subheader("1. Index Your Screenshots")
    st.caption("Enter the path to a folder containing screenshots to make them searchable.")

    filepath = st.text_input(
        "Folder path",
        placeholder="C:\\Users\\YourName\\Pictures\\Screenshots"
    )

    if "embedded_images" not in st.session_state:
        st.session_state.embedded_images = None

    if st.button("Index folder", icon="📁"):
        folder = Path(filepath)

        if not filepath.strip():
            st.warning("Please enter a folder path.")
        elif not folder.exists():
            st.error("Could not find folder path.")
        elif not folder.is_dir():
            st.error("The selected path is not a folder.")
        else:
            with st.spinner("Scanning screenshots..."):
                scanned_folder = scan_folder(filepath)

            if not scanned_folder:
                st.warning("No screenshots containing readable text were found.")
            else:
                save_index(scanned_folder)
                st.session_state.embedded_images = None
                st.success(f"{len(scanned_folder)} screenshots indexed successfully!")

    st.divider()

    ##Search for image
    st.subheader("2. Search Your Screenshots")
    st.caption("Describe the content you're looking for using everyday language.")

    search_query = st.text_input(
        "Search query",
        placeholder="Example: A menu for a restaurant"
    )

    if st.button("Search", icon="🔍"):
        if not search_query.strip():
            st.warning("Please enter a search query.")
        elif not Path("index.json").is_file():
            st.error("No screenshot index found. Please index a folder first.")
        else:
            with st.spinner("Searching screenshots..."):
                if st.session_state.embedded_images is None:
                    images = load_index()
                    st.session_state.embedded_images = prepare_embeddings(transformer, images)

                embedded_images = st.session_state.embedded_images
                search_embedding = transform(transformer, search_query)
                results = search_images(embedded_images, search_embedding)

            st.divider()
            st.subheader("Search Results")
            st.caption(f"Showing the {len(results)} most relevant screenshots.")

            for record in results:
                with st.container(border=True):
                    col1, col2 = st.columns([1, 2], gap="medium")

                    with col1:
                        st.image(record["path"], use_container_width=True)

                    with col2:
                        st.markdown(f"**{record['filename']}**")
                        st.write(f"Similarity Score: {record['score']:.4f}")
                        st.caption(record["path"])

    st.divider()
    st.caption("Semantic Screenshot Search | Powered by Tesseract OCR and Sentence Transformers")


if __name__ == "__main__":
    main()