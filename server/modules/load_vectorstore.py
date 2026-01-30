import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings


load_dotenv()

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
PINECONE_API_KEY=os.getenv('PINECONE_API_KEY')
PINECONE_ENV='us-east-1'
PINECONE_INDEX_NAME='medical-index'

os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR,exist_ok=True)


pc = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud='aws',region=PINECONE_ENV)


existing_index = [i['name'] for i in pc.list_indexes()]

if PINECONE_INDEX_NAME not in existing_index:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=1024,
        spec=spec,
        metric="dotproduct",
    )
    
    while not pc.describe_index(PINECONE_INDEX_NAME).status['ready']:
        time.sleep(1)
        
index  = pc.Index(PINECONE_INDEX_NAME)


def load_vectorstore(uploaded_file):
    embed_model=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001",output_dimensionality=1024)
    file_paths=[]
    
    for file in uploaded_file:
        save_path=Path(UPLOAD_DIR)/file.filename
        with open(save_path,'wb') as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))
        
    for file_path in file_paths:
        loader=PyPDFLoader(file_path)
        document=loader.load()
        print(f"DEBUG: Loaded {len(document)} pages. Content of page 1: '{document[0].page_content[:100]}'")
        
        splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
        chunks = splitter.split_documents(document)
        
        texts = [chunk.page_content for chunk in chunks]
        metadata_with_text = []
        for chunk in chunks:
            meta = chunk.metadata.copy()
            meta["text"] = chunk.page_content 
            metadata_with_text.append(meta)
        ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

        print(f"DEBUG: First chunk text: '{texts}...'")
        print(f"DEBUG: Total chunks to embed: {len(texts)}")
        
        print(f"Embedding chunks")
        embedding=embed_model.embed_documents(texts)
        
        print("Upserting documents")
        with tqdm(total=len(embedding),desc="Upserting to Pinecone") as progress:
            index.upsert(vectors=zip(ids,embedding,metadata_with_text))
            progress.update(len(embedding))
            
        print(f"Upload completed for {file_path}")