import pdfplumber
from pathlib import Path
import shutil
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings

source_folder = Path("/Users/punnu/Desktop/chhalaang/app/source_folder")
destination_folder = Path("/Users/punnu/Desktop/chhalaang/app/destination_folder")

for file in source_folder.iterdir():
    if file.suffix.lower() == ".pdf":
        print(f"\n--- Reading: {file.name} ---")
        loader = PyPDFLoader(file)   # since file is already a Path to the PDF



        docs = loader.load()

        # 2. Split text into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        # print(f"Total Chunks: {len(chunks)}")
        # 3. Generate embeddings (OpenAI here, could be Hugging Face too)
        embeddings = OpenAIEmbeddings(
            model='text-embedding-3-large',
            api_key='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'
        )
        # # 4. Create FAISS vector store
        db = FAISS.from_documents(chunks, embeddings)
        print(f"Vector Store created with {len(db.index)} vectors.")

        # # with pdfplumber.open(file) as pdf:
        # #     for page in pdf.pages:
        # #         print(page.extract_text()) 

        # # Move the file to destination folder
        # shutil.move(str(file), destination_folder / file.name)
        # print(f"Moved {file.name} to {destination_folder}")

        # # 5. Query
        # query = "What is this document about?"
        # results = db.similarity_search(query, k=3)

        # for r in results:
        #     print(r.page_content[:200], "...")

