import os
import textwrap
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

# Set your Hugging Face API token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
import textract

# Define a function to process a single PDF file
def process_single_pdf(pdf_file):
    # Step 1: Convert PDF to text
    doc = textract.process(pdf_file)

    # Step 2: Save to .txt and reopen (helps prevent issues)
    txt_file = pdf_file.replace(".pdf", ".txt")
    with open(txt_file, 'wb') as f:
        f.write(doc)

    with open(txt_file, 'r', encoding='utf-8') as f:
        text = f.read()


    loader = TextLoader(txt_file)
    documents = loader.load()


    text_splitter = CharacterTextSplitter(chunk_size=2500, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)


    embeddings = HuggingFaceEmbeddings()
    from langchain.vectorstores import FAISS

    db = FAISS.from_documents(docs, embeddings)

    return db

pdf_files = ["2021-09-30-NASA-STD-6016C-Approved.pdf", "AIAA_S_080_1998.pdf"]
             #"N_PD_1000_000C_.pdf","nasa-std-5002a.pdf","nasa-std-5018_revalidated (1).pdf","tb-summary-100223.pdf","dataset.pdf"]


vector_stores = []
for pdf_file in pdf_files:
    print(f"Processing {pdf_file}...\n")
    db = process_single_pdf(pdf_file)
    vector_stores.append((pdf_file, db))


query = input("Enter Keyword")
for pdf_file, db in vector_stores:
    docs = db.similarity_search(query)
    print("-"* 50)
    print("-"* 50)
    print(f"Results from {pdf_file}:\n")
    for doc in docs:
        wrapped_text = "\n".join(textwrap.wrap(str(doc.page_content), width=80))
        print(f"\n{wrapped_text}\n")
        print("-" * 50)

