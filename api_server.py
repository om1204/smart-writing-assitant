import os
import nltk
import spacy
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main_nlp_flow import SmartPipeline

for resource in ('wordnet', 'omw-1.4'):
    try:
        nltk.data.find('corpora/' + resource)
    except LookupError:
        try:
            nltk.download(resource, quiet=True)
        except Exception:
            pass

MODEL = os.getenv('SPACY_MODEL', 'en_core_web_sm')
try:
    nlp = spacy.load(MODEL)
except Exception as exc:
    raise RuntimeError(f'Unable to load spaCy model {MODEL}. Install en_core_web_sm.') from exc

pipe = SmartPipeline(nlp)
app = FastAPI(title='Smart Reading & Writing Assistant API', version='2.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

class ProcessRequest(BaseModel):
    text: str

@app.get('/api/health')
def health(): return {'status':'ok','model':MODEL}

@app.post('/api/process')
def process(req: ProcessRequest):
    text = req.text.strip()
    if not text: raise HTTPException(400, 'Text cannot be empty.')
    if len(text) > 12000: raise HTTPException(413, 'Text is too long. Maximum 12,000 characters.')
    return pipe.process(text)
