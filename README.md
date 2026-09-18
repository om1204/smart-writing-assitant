# LexiFlow — Smart Reading & Writing Assistant

A project-level implementation of the assignment **Building a Smart Reading & Writing Assistant (NLP Pipeline)**. The application uses a React/Vite premium frontend and a FastAPI Python api_server. It exposes all five syllabus stages as visible, testable UI views.

## Architecture
- `frontend/` — React + Vite UI
- `api_server.py` — FastAPI API server
- `main_nlp_flow.py` — stage 1 → 4 orchestration
- `part1_spellcheck/` — from-scratch Levenshtein + context-aware spell checking
- `part2_parsing/` — spaCy POS/dependencies + hand-written CKY/CFG parser
- `part3_meaning/` — NER, semantic frames, Lesk-style WordNet WSD
- `part4_pragmatics/` — heuristic coreference, discourse connectives, pragmatic inference
- `data/test_samples.txt` — 10 messy test samples

## Run locally
### Backend
```bash
pip install -r requirements.txt
uvicorn api_server:app --reload --port 8000
```
The spaCy model is installed by the requirements URL.

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Open the Vite URL shown in the terminal. The frontend expects the API at `http://localhost:8000` by default. For deployment, set `VITE_API_URL` to the deployed api_server URL.

## Assignment mapping
1. Spell checking: Levenshtein distance is implemented from scratch; explicit typo corrections and context evidence are displayed.
2. Syntactic processing: spaCy POS/dependencies plus a hand-written compact CKY parser.
3. Semantic analysis: NER, semantic role frames and Lesk-style WSD for bank/bat/light.
4. Discourse/pragmatics: nearest-antecedent coreference, connective relation labels and indirect-request inference.
5. Full main_nlp_flow: `process(raw_text)` returns corrected text, syntax, semantic frames, discourse relations and summary data.
