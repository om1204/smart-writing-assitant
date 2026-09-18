import re
from collections import Counter

# Try loading real NLTK corpora vocabulary and frequency
NLTK_VOCAB = set()
NLTK_FREQ = Counter()

try:
    import nltk
    for resource in ('words', 'brown', 'wordnet', 'omw-1.4'):
        try:
            nltk.data.find('corpora/' + resource)
        except LookupError:
            nltk.download(resource, quiet=True)
            
    from nltk.corpus import words as nltk_words, brown, wordnet as wn
    for w in wn.words():
        NLTK_VOCAB.add(w.lower())
    for w in nltk_words.words():
        NLTK_VOCAB.add(w.lower())
    for w in brown.words():
        w_lower = w.lower()
        NLTK_FREQ[w_lower] += 1
        NLTK_VOCAB.add(w_lower)
except Exception:
    pass

# Regular expressions for tokenization and word identification
TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?(?:-[A-Za-z0-9]+)*|\d+(?:\.\d+)?%?|[^\w\s]")
WORD_RE = re.compile(r"^[A-Za-z]+(?:'[A-Za-z]+)?$")

# Technical acronyms, hardware/software terms, units, and models that must NEVER be altered
IMMUNE_TERMS = {
    'sar', 'ai', 'nlp', 'ml', 'cuda', 'nvidia', 'earthmind', 'pytorch',
    'tensorflow', 'spacy', 'fastapi', 'uvicorn', 'nltk', 'wordnet',
    'transformer', 'encoder', 'tokens', 'token', 'dimensions', 'dimensional',
    'gb', 'mb', 'kb', 'hz', 'ghz', 'params', 'parameters', 'weights',
    'v1', 'v2', 'v3', 'bert', 'gpt', 'llm', 'vlm', 'resnet', 'vit',
    'cky', 'cfg', 'svo', 'pos', 'ner', 'wsd', 'main_nlp_flow', 'cache',
    'cached', 'database', 'sensors', 'satellites', 'satellite',
    'rahul', 'arjun', 'riya', 'neha', 'aman'
}

# Authentic phonetic / typographic error mappings for high-precision corrections
AUTHENTIC_TYPOS = {
    'orignal': 'original',
    'ohk': 'ok',
    'architeture': 'architecture',
    'woking': 'working',
    'satelite': 'satellite',
    'differnt': 'different',
    'efficently': 'efficiently',
    'inteligence': 'intelligence',
    'explictly': 'explicitly',
    'recieved': 'received',
    'definately': 'definitely',
    'definatly': 'definitely',
    'didnt': "didn't",
    'dont': "don't",
    'doesnt': "doesn't",
    'cant': "can't",
    'teh': 'the',
    'adress': 'address',
    'becuase': 'because',
    'severl': 'several',
    'enviroment': 'environment',
    'seperate': 'separate',
    'thier': 'their',
    'tomorow': 'tomorrow',
    'recieve': 'receive',
    'wich': 'which',
    'alot': 'a lot',
    'untill': 'until',
    'occured': 'occurred',
    'beleive': 'believe',
    'wierd': 'weird',
    'necessery': 'necessary',
}

# Baseline core English unigram frequencies
DEFAULT_FREQ = Counter({
    'the': 69971, 'of': 36412, 'and': 28852, 'to': 26158, 'a': 23195,
    'in': 21341, 'that': 10594, 'is': 10109, 'was': 9816, 'he': 9548,
    'for': 9489, 'it': 8760, 'with': 7289, 'as': 7251, 'his': 6996,
    'on': 6742, 'be': 6377, 'at': 5372, 'by': 5306, 'i': 5180,
    'this': 5146, 'had': 5133, 'not': 4610, 'are': 4394, 'but': 4381,
    'from': 4370, 'or': 4206, 'have': 3942, 'an': 3740, 'they': 3620,
    'which': 3561, 'one': 3292, 'you': 3286, 'were': 3284, 'her': 3037,
    'all': 3001, 'she': 2860, 'there': 2724, 'would': 2714, 'their': 2669,
    'we': 2652, 'him': 2619, 'been': 2472, 'has': 2437, 'when': 2331,
    'who': 2252, 'more': 2215, 'will': 2245, 'no': 2139, 'if': 2112,
    'out': 2093, 'so': 1984, 'said': 1961, 'what': 1908, 'up': 1890,
    'its': 1858, 'about': 1815, 'into': 1791, 'than': 1790, 'them': 1787,
    'can': 1772, 'only': 1748, 'other': 1702, 'new': 1635, 'some': 1618,
    'could': 1601, 'time': 1598, 'these': 1573, 'two': 1412, 'may': 1402,
    'then': 1380, 'do': 1363, 'first': 1361, 'any': 1344, 'my': 1319,
    'now': 1314, 'such': 1303, 'like': 1292, 'our': 1252, 'over': 1236,
    'man': 1207, 'me': 1181, 'even': 1170, 'most': 1159, 'made': 1125,
    'after': 1070, 'also': 1069, 'did': 1044, 'many': 1030, 'before': 1016,
    'must': 1013, 'through': 971, 'back': 966, 'years': 950, 'where': 937,
    'much': 937, 'your': 923, 'way': 908, 'well': 897, 'down': 895,
    'should': 888, 'because': 883, 'each': 877, 'just': 872, 'those': 850,
    'people': 847, 'how': 841, 'too': 834, 'little': 831, 'state': 807,
    'good': 806, 'very': 796, 'make': 794, 'world': 787, 'still': 782,
    'own': 772, 'see': 772, 'men': 763, 'work': 762, 'long': 752,
    'get': 749, 'here': 748, 'between': 737, 'both': 730, 'life': 715,
    'being': 712, 'under': 707, 'never': 697, 'day': 687, 'same': 686,
    'another': 684, 'know': 683, 'while': 680, 'last': 676, 'might': 672,
    'great': 665, 'old': 661, 'year': 658, 'off': 639, 'come': 630,
    'since': 628, 'against': 627, 'go': 626, 'came': 622, 'right': 613,
    'used': 611, 'take': 611, 'three': 610, 'himself': 603, 'system': 602,
    'give': 598, 'house': 591, 'during': 585, 'without': 583, 'place': 570,
    'again': 577, 'around': 562, 'however': 552, 'home': 547, 'small': 542,
    'number': 472, 'always': 458, 'found': 436, 'water': 442, 'room': 399,
    'money': 265, 'group': 250, 'problem': 240, 'bank': 180, 'river': 95,
    'bat': 45, 'satellite': 80, 'different': 360, 'efficiently': 60,
    'intelligence': 110, 'explicitly': 40, 'working': 280, 'architecture': 90,
    'original': 140, 'lose': 130, 'loose': 75,
})

class MySpellCorrector:
    """From-scratch conservative Levenshtein spell checker with lexical evidence."""
    
    def __init__(self, custom_freq=None):
        self.freq = DEFAULT_FREQ.copy()
        if NLTK_FREQ:
            self.freq.update(NLTK_FREQ)
        if custom_freq:
            self.freq.update({k.lower(): v for k, v in custom_freq.items()})
            
        self.lexicon = set(self.freq.keys()) | NLTK_VOCAB | IMMUNE_TERMS
        self.immune_terms = IMMUNE_TERMS.copy()

    @staticmethod
    def levenshtein(a: str, b: str) -> int:
        """Computes Levenshtein edit distance from scratch using dynamic programming."""
        m, n = len(a), len(b)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if a[i - 1] == b[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,      # deletion
                    dp[i][j - 1] + 1,      # insertion
                    dp[i - 1][j - 1] + cost # substitution
                )
        return dp[m][n]

    def is_valid_word(self, token: str) -> bool:
        """Verifies if a token is an existing, valid English or domain word."""
        w = token.lower()
        if w in self.lexicon or w in self.immune_terms:
            return True
        # Morphological plural/inflection check
        if w.endswith('s') and (w[:-1] in self.lexicon or w[:-2] in self.lexicon):
            return True
        if w.endswith('ed') and (w[:-1] in self.lexicon or w[:-2] in self.lexicon):
            return True
        if w.endswith('ing') and (w[:-3] in self.lexicon or (w[:-3] + 'e') in self.lexicon):
            return True
        if w.endswith('ly') and (w[:-2] in self.lexicon or w[:-1] in self.lexicon):
            return True
        if w.replace("'", "") in self.lexicon:
            return True
        return False

    def is_immune(self, token: str) -> bool:
        """Determines if a token should never be modified (acronyms, code, units, proper nouns)."""
        # Numbers, decimals, percentages, dimensions (e.g. 768-dimensional, 12.4 GB, 91.7%)
        if re.match(r'^\d+(?:\.\d+)?%?$', token):
            return True
        if re.search(r'\d', token):
            return True
        # All uppercase acronyms of length >= 2 (SAR, AI, NLP, CUDA, NVIDIA)
        if token.isupper() and len(token) >= 2:
            return True
        # CamelCase / Mixed Case proper nouns (EarthMind, spaCy, PyTorch)
        if any(c.isupper() for c in token[1:]) and any(c.islower() for c in token):
            return True
        # Hyphenated technical compound terms (e.g. transformer-based, multi-token)
        if '-' in token:
            parts = token.split('-')
            if all(self.is_valid_word(p) or p.lower() in self.immune_terms or re.match(r'^\d+$', p) for p in parts):
                return True
        # Registered domain terms
        if token.lower() in self.immune_terms:
            return True
        return False

    def candidates(self, word: str, max_dist: int = 2):
        """Generates candidate corrections from lexicon ranked by edit distance and frequency."""
        w = word.lower()
        # Explicit authentic typos
        if w in AUTHENTIC_TYPOS:
            return [(0, AUTHENTIC_TYPOS[w], "authentic typo pattern")]
            
        # If the word is already valid, do not propose random distance-based replacements
        if self.is_valid_word(w):
            return []

        scored = []
        len_w = len(w)
        # Scan frequency lexicon for candidates within edit distance threshold
        for dict_word, freq in self.freq.items():
            if abs(len(dict_word) - len_w) <= max_dist:
                dist = self.levenshtein(w, dict_word)
                if 1 <= dist <= max_dist:
                    # Confidence heuristic combining distance penalty and frequency evidence
                    conf = max(0.2, min(0.95, (1.0 - (dist * 0.35)) + min(0.3, freq / 100000.0)))
                    scored.append((dist, -freq, dict_word, conf))
                    
        scored.sort()
        results = []
        for dist, neg_f, cand, conf in scored[:3]:
            reason = f"Levenshtein edit distance d={dist} with corpus frequency evidence ({ -neg_f } occurrences)"
            results.append((dist, cand, reason, conf))
        return results

    def correct(self, text: str):
        """Processes raw text conservatively, preserving technical terms, casing, and punctuation."""
        matches = list(TOKEN_RE.finditer(text))
        out_tokens = []
        corrections = []
        words_scanned = 0

        for idx, match in enumerate(matches):
            tok = match.group(0)
            start_pos, end_pos = match.start(), match.end()

            # Pass non-word punctuation directly
            if not WORD_RE.fullmatch(tok) and not re.search(r'\w', tok):
                out_tokens.append(tok)
                continue

            words_scanned += 1

            # Immunity check: technical terms, acronyms, mixed-case, numbers
            if self.is_immune(tok):
                out_tokens.append(tok)
                continue

            word_l = tok.lower()
            prev_tok = matches[idx - 1].group(0) if idx > 0 else ""
            next_tok = matches[idx + 1].group(0) if idx + 1 < len(matches) else ""

            # Check context-dependent confusion: 'loose' (adjective) vs 'lose' (verb)
            is_confusion = False
            replacement = tok
            cand_info = None

            if word_l == 'loose':
                modal_triggers = {'maybe', 'might', 'will', 'to', 'can', 'could', 'would', 'shall'}
                obj_triggers = {'some', 'details', 'information', 'data', 'features', 'the', 'a'}
                if prev_tok.lower() in modal_triggers or next_tok.lower() in obj_triggers:
                    replacement = 'lose'
                    cand_info = (
                        1, 'lose',
                        "Contextual confusion: 'loose' (adjective) -> 'lose' (verb before direct object/modal)",
                        0.92
                    )
                    is_confusion = True

            if not is_confusion:
                # Authentic typo check
                if word_l in AUTHENTIC_TYPOS:
                    rep_word = AUTHENTIC_TYPOS[word_l]
                    dist = self.levenshtein(word_l, rep_word)
                    cand_info = (dist, rep_word, f"Authentic typo correction: '{tok}' -> '{rep_word}'", 0.98)
                    replacement = rep_word
                elif not self.is_valid_word(word_l):
                    cands = self.candidates(word_l, max_dist=2)
                    if cands:
                        best = cands[0]
                        dist, rep_word, reason, conf = best
                        cand_info = (dist, rep_word, reason, conf)
                        replacement = rep_word

            if replacement.lower() != word_l and cand_info:
                # Preserve original casing
                if tok.isupper():
                    final_rep = replacement.upper()
                elif tok[0].isupper():
                    final_rep = replacement[0].upper() + replacement[1:]
                else:
                    final_rep = replacement

                corrections.append({
                    'original': tok,
                    'replacement': final_rep,
                    'edit_distance': cand_info[0],
                    'confidence': round(cand_info[3], 2),
                    'reason': cand_info[2],
                    'position': {
                        'start': start_pos,
                        'end': end_pos,
                        'token_index': idx
                    }
                })
                out_tokens.append(final_rep)
            else:
                out_tokens.append(tok)

        # Assemble cleaned text preserving punctuation spacing
        no_space_before = {',', '.', '!', '?', ';', ':', ')', '%'}
        no_space_after = {'('}
        corrected = ''
        for t in out_tokens:
            if not corrected:
                corrected = t
            elif t in no_space_before:
                corrected = corrected.rstrip() + t
            elif corrected.endswith(tuple(no_space_after)):
                corrected += t
            else:
                corrected += ' ' + t

        return SpellResult(
            corrected.strip(),
            corrections,
            words_scanned,
            text
        )

    def check(self, text):
        return self.correct(text).to_dict()


class SpellResult(tuple):
    """
    Dual-compatibility result:
    Unpacks as (corrected_text, corrections) for tuple unpacking,
    while also exposing .words_scanned, .raw_text, .corrections_count, and .to_dict().
    """
    def __new__(cls, corrected_text, corrections, words_scanned, raw_text):
        return super().__new__(cls, (corrected_text, corrections))

    def __init__(self, corrected_text, corrections, words_scanned, raw_text):
        self.corrected_text = corrected_text
        self.corrections = corrections
        self.words_scanned = words_scanned
        self.raw_text = raw_text
        self.corrections_count = len(corrections)

    def to_dict(self):
        return {
            'raw_text': self.raw_text,
            'corrected_text': self.corrected_text,
            'corrections': self.corrections,
            'words_scanned': self.words_scanned,
            'corrections_count': self.corrections_count
        }

    def __getitem__(self, item):
        if isinstance(item, str):
            return getattr(self, item)
        return super().__getitem__(item)

