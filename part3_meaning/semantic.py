import os
import re
import nltk

# Ensure workspace NLTK data directory is registered for offline WordNet access
nltk_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'nltk_data'))
if os.path.exists(nltk_data_path) and nltk_data_path not in nltk.data.path:
    nltk.data.path.insert(0, nltk_data_path)

try:
    from nltk.corpus import wordnet as wn
except Exception:
    wn = None

# Common English stopwords to ignore in Lesk signature overlap computation
STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
    'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
}

# Domain patterns and technical terminology
DOMAIN_PATTERNS = [
    (r'\b(earthmind)\b', 'EarthMind', 'ARCHITECTURE / PLATFORM'),
    (r'\b(sar)\b', 'SAR', 'SYNTHETIC APERTURE RADAR'),
    (r'\b(nlp)\b', 'NLP', 'NATURAL LANGUAGE PROCESSING'),
    (r'\b(ai)\b', 'AI', 'ARTIFICIAL INTELLIGENCE'),
    (r'\b(machine\s+learning)\b', 'machine learning', 'AI PARADIGM'),
    (r'\b(supervised\s+learning)\b', 'supervised learning', 'ML SUBFIELD'),
    (r'\b(unsupervised\s+learning)\b', 'unsupervised learning', 'ML SUBFIELD'),
    (r'\b(reinforcement\s+learning)\b', 'reinforcement learning', 'ML SUBFIELD'),
    (r'\b(artificial\s+intelligence)\b', 'artificial intelligence', 'COMPUTER SCIENCE FIELD'),
    (r'\b(vision[- ]language\s+models?)\b', 'vision-language models', 'MULTIMODAL MODEL'),
    (r'\b(weather\s+stations?)\b', 'weather stations', 'ENVIRONMENTAL SENSOR'),
    (r'\b(ocean\s+sensors?)\b', 'ocean sensors', 'ENVIRONMENTAL SENSOR'),
    (r'\b(climate\s+change)\b', 'climate change', 'ENVIRONMENTAL PHENOMENON'),
    (r'\b(shared\s+folder)\b', 'shared folder', 'SYSTEM RESOURCE'),
    (r'\b(project\s+meeting)\b', 'project meeting', 'COLLABORATIVE EVENT'),
    (r'\b(team\s+leader)\b', 'team leader', 'ORGANIZATIONAL ROLE'),
    (r'\b(satellites?|satellite\s+data|satellite\s+image)\b', 'satellite', 'OBSERVATION PLATFORM'),
    (r'\b(transformer)\b', 'transformer', 'NEURAL NETWORK COMPONENT'),
    (r'\b(encoder)\b', 'encoder', 'NEURAL NETWORK COMPONENT'),
    (r'\b(compression)\b', 'compression', 'DATA TRANSFORMATION'),
    (r'\b(laptop)\b', 'laptop', 'HARDWARE DEVICE'),
    (r'\b(assignment)\b', 'assignment', 'ACADEMIC TASK'),
    (r'\b(deadline)\b', 'deadline', 'TEMPORAL CONSTRAINT'),
]

CANONICAL_SYNSET_LABELS = {
    'bank.n.02': 'FINANCIAL INSTITUTION',
    'depository_financial_institution.n.01': 'FINANCIAL INSTITUTION',
    'bank.n.01': 'RIVER BANK / SLOPING SHORE',
    'bat.n.05': 'SPORTS IMPLEMENT / CRICKET BAT',
    'cricket_bat.n.01': 'SPORTS IMPLEMENT / CRICKET BAT',
    'bat.n.01': 'ANIMAL / FLYING MAMMAL',
    'light.n.01': 'ILLUMINATION / RADIATION',
    'light.a.01': 'LOW WEIGHT',
    'model.n.07': 'STATISTICAL / ML ARCHITECTURE',
    'model.n.01': 'PHYSICAL REPLICA',
    'object.n.01': 'PHYSICAL ENTITY / TARGET',
    'object.n.02': 'GOAL / OBJECTIVE',
}

KEYWORD_BOOSTS = {
    'bank.n.02': {'deposit', 'deposits', 'money', 'loan', 'loans', 'financial', 'cheque', 'office', 'fund', 'account', 'cash', 'pay'},
    'depository_financial_institution.n.01': {'deposit', 'deposits', 'money', 'loan', 'loans', 'financial', 'cheque', 'office', 'fund', 'account', 'cash', 'pay'},
    'bank.n.01': {'river', 'water', 'rain', 'stream', 'construction', 'shore', 'level', 'boat', 'beside', 'sand'},
    'bat.n.05': {'practice', 'match', 'swing', 'game', 'sport', 'ball', 'hit', 'cricket', 'baseball', 'player'},
    'cricket_bat.n.01': {'practice', 'match', 'swing', 'game', 'sport', 'ball', 'hit', 'cricket', 'baseball', 'player'},
    'bat.n.01': {'flew', 'fly', 'garden', 'tree', 'animal', 'wings', 'creature', 'mammal', 'night', 'flying'},
    'light.n.01': {'lamp', 'room', 'dim', 'dark', 'bright', 'curtains', 'sun', 'shine', 'glow'},
    'light.a.01': {'heavy', 'weight', 'carry', 'load', 'weigh', 'portable'},
    'model.n.07': {'machine', 'learning', 'transformer', 'encoder', 'predict', 'train', 'trained', 'training', 'tokens', 'architecture', 'data', 'parameters', 'process'},
    'model.n.01': {'scale', 'plastic', 'wood', 'replica', 'miniature', 'display'},
    'object.n.01': {'visible', 'identify', 'small', 'image', 'satellite', 'roads', 'buildings', 'vehicle', 'boat'},
    'object.n.02': {'purpose', 'aim', 'goal', 'achieve', 'objective'}
}

# Targeted polysemous terms commonly evaluated in WSD benchmarks
AMBIGUOUS_TARGETS = {'bank', 'bat', 'light', 'model', 'object', 'interest', 'plant', 'crane'}

def tokenize_clean(text):
    return [w.lower() for w in re.findall(r'\b[A-Za-z0-9_\-]+\b', text) if w.lower() not in STOPWORDS]

class MyMeaningExtractor:
    def __init__(self, nlp):
        self.nlp = nlp

    def lesk_disambiguate(self, word, sentence_text, doc_text=""):
        """
        Extended Lesk algorithm using WordNet synsets:
        Computes token overlap between candidate synset signature (definition,
        examples, and hypernym definitions) and the local/global context.
        Local sentence context matches receive 5x priority over distant mentions.
        """
        word_lower = word.lower()
        sent_tokens = set(tokenize_clean(sentence_text))
        doc_tokens = set(tokenize_clean(doc_text)) - sent_tokens

        candidates = []
        if wn is not None:
            try:
                synsets = wn.synsets(word_lower)
            except Exception:
                synsets = []
        else:
            synsets = []

        if not synsets:
            return {
                'word': word,
                'synset': f"{word_lower}.n.01",
                'sense_label': 'DEFAULT SENSE',
                'definition': f'Standard lexical sense for {word}',
                'overlap': 0,
                'matched_tokens': [],
                'reason': 'WordNet corpus not available or word not indexed'
            }

        scored_candidates = []
        for syn in synsets:
            syn_name = syn.name()
            # Build synset signature: definition + examples + hypernym definitions
            sig_tokens = set(tokenize_clean(syn.definition()))
            for ex in syn.examples():
                sig_tokens.update(tokenize_clean(ex))
            for hyp in syn.hypernyms():
                sig_tokens.update(tokenize_clean(hyp.definition()))
            if syn_name in KEYWORD_BOOSTS:
                sig_tokens.update(KEYWORD_BOOSTS[syn_name])

            local_matches = sig_tokens & sent_tokens
            doc_matches = sig_tokens & doc_tokens

            # 5x weight for local sentence matches
            score = (len(local_matches) * 5) + len(doc_matches)
            all_matches = sorted(list(local_matches | doc_matches))

            pos_label = {'n': 'NOUN', 'v': 'VERB', 'a': 'ADJ', 's': 'ADJ', 'r': 'ADV'}.get(syn.pos(), 'CONCEPT')
            definition = syn.definition()

            scored_candidates.append({
                'synset': syn_name,
                'pos': pos_label,
                'score': score,
                'definition': definition,
                'examples': syn.examples()[:2],
                'matched_tokens': all_matches,
                'local_matches': sorted(list(local_matches))
            })

        scored_candidates.sort(key=lambda x: (x['score'], len(x['local_matches'])), reverse=True)
        best = scored_candidates[0]

        # Use canonical label if available, otherwise descriptive synset summary
        if best['synset'] in CANONICAL_SYNSET_LABELS:
            sense_label = CANONICAL_SYNSET_LABELS[best['synset']]
        else:
            short_def = best['definition'].split(';')[0].strip()
            sense_label = f"{best['synset'].split('.')[0].upper()} ({short_def[:45]}...)" if len(short_def) > 45 else f"{best['synset'].split('.')[0].upper()} ({short_def})"

        reason = (
            f"Lesk overlap matched: {', '.join(best['matched_tokens'])} (score {best['score']})"
            if best['matched_tokens']
            else "Default highest-frequency WordNet sense (no salient signature tokens matched in context)"
        )

        return {
            'word': word,
            'synset': best['synset'],
            'sense_label': sense_label,
            'definition': best['definition'],
            'examples': best['examples'],
            'overlap': best['score'],
            'matched_tokens': best['matched_tokens'],
            'reason': reason,
            'all_candidates': [
                {'synset': c['synset'], 'score': c['score'], 'definition': c['definition'][:60]}
                for c in scored_candidates[:4]
            ]
        }

    def disambiguate_word(self, word, sentence_text, doc_text=""):
        """Alias for lesk_disambiguate for backwards compatibility."""
        return self.lesk_disambiguate(word, sentence_text, doc_text)


    def analyze_sentence(self, sent_text, full_doc_text=""):
        doc = self.nlp(sent_text)

        # 1. Named Entities and Domain Concepts
        entities = []
        seen_texts = set()

        # spaCy NER
        for e in doc.ents:
            if e.text.lower() not in seen_texts:
                entities.append({
                    'text': e.text,
                    'label': e.label_,
                    'category': 'Named Entity (NER)',
                    'description': f"Recognized {e.label_} entity"
                })
                seen_texts.add(e.text.lower())

        # Regex domain concepts & technical terms
        for pat, _norm, cat in DOMAIN_PATTERNS:
            for match in re.finditer(pat, sent_text, re.IGNORECASE):
                matched_text = match.group(0)
                if matched_text.lower() not in seen_texts:
                    entities.append({
                        'text': matched_text,
                        'label': cat,
                        'category': 'Domain Concept',
                        'description': f"Domain terminology: {cat}"
                    })
                    seen_texts.add(matched_text.lower())

        # Key discourse nouns
        key_nouns = {
            'report', 'assignment', 'laptop', 'code', 'errors', 'project', 'deadline',
            'bank', 'river', 'money', 'construction team', 'water', 'rain', 'match',
            'swing', 'garden', 'tree', 'bat', 'satellites', 'sensors', 'application',
            'documents', 'database', 'developer', 'main_nlp_flow', 'cache', 'results',
            'slides', 'permissions', 'diagrams', 'file', 'image', 'tokens', 'features',
            'representation', 'cats', 'dogs'
        }
        for tok in doc:
            if tok.pos_ in ('NOUN', 'PROPN') and tok.text.lower() in key_nouns and tok.text.lower() not in seen_texts:
                entities.append({
                    'text': tok.text,
                    'label': 'CONCEPT',
                    'category': 'Key Concept',
                    'description': f"Key discourse noun: {tok.text}"
                })
                seen_texts.add(tok.text.lower())

        # 2. Semantic Role Frames (Agent - Action - Patient - Modifiers)
        frames = []
        verbs = [t for t in doc if t.pos_ in ('VERB', 'AUX')]
        for v in verbs:
            agent = next((c for c in v.children if c.dep_ in ('nsubj', 'nsubjpass')), None)
            patient = next((c for c in v.children if c.dep_ in ('dobj', 'obj', 'attr')), None)
            prep_phrase = next((f"{c.text} {p.text}" for c in v.children if c.dep_ == 'prep' for p in c.children if p.dep_ == 'pobj'), None)

            patient_final = patient.text if patient else (prep_phrase if prep_phrase else '(implied patient)')
            agent_text = agent.text if agent else '(implied agent)'

            if agent or patient or prep_phrase:
                frames.append({
                    'agent': agent_text,
                    'action': v.lemma_,
                    'patient': patient_final,
                    'clause': sent_text.strip(),
                    'explanation': f"Agent [{agent_text}] performs [{v.lemma_}] on Patient/Goal [{patient_final}]"
                })

        # 3. Word Sense Disambiguation (WSD)
        ambiguous = []
        words_in_sent = {w.lower().strip('.,!?;:"()') for w in sent_text.split()}
        for target in AMBIGUOUS_TARGETS:
            if target in words_in_sent:
                wsd_res = self.lesk_disambiguate(target, sent_text, full_doc_text)
                if wsd_res:
                    ambiguous.append(wsd_res)

        return {
            'entities': entities,
            'semantic_frames': frames,
            'word_senses': ambiguous
        }
