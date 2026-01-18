from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middlewares.exception_handlers import catch_exception_middleware

app = FastAPI(title='Medical Assistant API',description='API for Medical assistant Chatbot')


app.add_middleware(
    CORSMiddleware(
        allow_origins=['*'],
        allow_credentials=['*'],
        allow_headers=['*'],
        allow_methods=['*']
    )
)


# middleware exception handlers
app.middleware("http")(catch_exception_middleware)

# routers

# 1. upload a pdf
# 2. asking query


