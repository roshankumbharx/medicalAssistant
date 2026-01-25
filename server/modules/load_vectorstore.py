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
os.mkdir(UPLOAD_DIR,exist_ok=True)

# pinecone init

pc = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud='aws',region=PINECONE_ENV)

# fetching all the existing indexes