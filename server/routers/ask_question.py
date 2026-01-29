from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone
from pydantic import Field
from typing import List, Optional
from logger import logger
import os


router = APIRouter()

@router.post('/ask_question/')
async def ask_question(question:str=Form(...)):
    try:
        logger.info(f"User query:{question}")
        
    
    except Exception as e:
        logger.exception('Error processing question')
        return JSONResponse(status_code=500,content={'error':str(e)})
