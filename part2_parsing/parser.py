import re

# Explicit hand-written Context-Free Grammar (CFG) consisting of 14 canonical production rules
HANDWRITTEN_CFG_RULES = [
    "S -> NP VP",
    "S -> S CONJ",
    "S -> CONJ S",
    "NP -> DET N",
    "NP -> ADJ N",
    "NP -> N N",
    "NP -> NP PP",
    "NP -> PRON N",
    "VP -> V NP",
    "VP -> V PP",
    "VP -> AUX VP",
    "VP -> V ADV",
    "VP -> V S",
    "PP -> P NP",
]

PARSED_CFG_RULES = [
    ('S', 'NP', 'VP'),
    ('S', 'S', 'CONJ'),
    ('S', 'CONJ', 'S'),
    ('NP', 'DET', 'N'),
    ('NP', 'ADJ', 'N'),
    ('NP', 'N', 'N'),
    ('NP', 'NP', 'PP'),
    ('NP', 'PRON', 'N'),
    ('VP', 'V', 'NP'),
    ('VP', 'V', 'PP'),
    ('VP', 'AUX', 'VP'),
    ('VP', 'V', 'ADV'),
    ('VP', 'V', 'S'),
    ('PP', 'P', 'NP'),
]

class CKYParser:
    """
    A hand-written Cocke-Younger-Kasami (CKY) phrase-structure parser
    operating over a 14-rule hand-written CFG grammar.
    """
    def __init__(self):
        self.rules = PARSED_CFG_RULES
        self.grammar_rules = HANDWRITTEN_CFG_RULES
        
        # Domain & general lexicon mapping words to non-terminal parts of speech
        self.lexicon = {
            # Nouns
            'student':'N','students':'N','teacher':'N','team':'N','report':'N','file':'N',
            'assignment':'N','project':'N','room':'N','bank':'N','loan':'N','light':'N','bat':'N',
            'class':'N','office':'N','arjun':'N','riya':'N','aman':'N','rahul':'N','neha':'N','professor':'N',
            'mistakes':'N','paragraph':'N','model':'N','models':'N','image':'N','images':'N',
            'token':'N','tokens':'N','encoder':'N','transformer':'N','compression':'N','paper':'N',
            'details':'N','architecture':'N','features':'N','data':'N','satellite':'N','satellites':'N',
            'sensor':'N','sensors':'N','system':'N','laptop':'N','code':'N','testing':'N','result':'N',
            'results':'N','errors':'N','error':'N','deadline':'N','time':'N','river':'N','money':'N',
            'water':'N','rain':'N','window':'N','swing':'N','garden':'N','tree':'N','match':'N',
            'temperature':'N','rainfall':'N','level':'N','application':'N','documents':'N','database':'N',
            'logs':'N','main_nlp_flow':'N','intelligence':'N','rule':'N','mapping':'N','presentation':'N',
            'slides':'N','folder':'N','permissions':'N','diagrams':'N','earthmind':'N','sar':'N','nlp':'N','ai':'N',
            'cat':'N','cats':'N','dog':'N','dogs':'N','computer':'N','hour':'N','hours':'N','user':'N','users':'N',
            # Determiners
            'the':'DET','a':'DET','an':'DET','my':'DET','this':'DET','these':'DET','that':'DET','those':'DET',
            'his':'DET','her':'DET','their':'DET','its':'DET','our':'DET','some':'DET','every':'DET','no':'DET',
            # Verbs
            'sent':'V','send':'V','submitted':'V','submit':'V','read':'V','approved':'V','needed':'V',
            'need':'V','finished':'V','review':'V','practice':'V','became':'V','flew':'V','used':'V',
            'was':'V','is':'V','were':'V','are':'V','want':'V','wants':'V','accepted':'V','improve':'V',
            'went':'V','deposit':'V','take':'V','takes':'V','took':'V','compress':'V','compresses':'V',
            'extract':'V','extracts':'V','explain':'V','explains':'V','process':'V','processes':'V',
            'loose':'V','lose':'V','see':'V','sees':'V','saw':'V','stop':'V','stopped':'V','tried':'V',
            'requesting':'V','request':'V','know':'V','completed':'V','called':'V','asked':'V','walking':'V',
            'talking':'V','increased':'V','carrying':'V','laughed':'V','understand':'V','changing':'V',
            'contain':'V','combine':'V','trusted':'V','trained':'V','designed':'V','cached':'V','reused':'V',
            'returned':'V','learn':'V','predict':'V','showed':'V','convert':'V','recover':'V','preserve':'V',
            'scheduled':'V','prepared':'V','entered':'V','share':'V','updating':'V','realized':'V','uploaded':'V',
            'saved':'V','said':'V','told':'V','give':'V','gives':'V','gave':'V','hanging':'V','started':'V',
            # Prepositions
            'to':'P','before':'P','after':'P','in':'P','into':'P','on':'P','with':'P','near':'P','from':'P',
            'by':'P','for':'P','about':'P','beside':'P','across':'P','during':'P','of':'P','at':'P',
            # Pronouns
            'he':'PRON','she':'PRON','it':'PRON','they':'PRON','i':'PRON','you':'PRON','we':'PRON','him':'PRON','them':'PRON','me':'PRON',
            # Auxiliaries & Modals
            'could':'AUX','would':'AUX','should':'AUX','can':'AUX','may':'AUX','might':'AUX','will':'AUX','shall':'AUX','did':'AUX','does':'AUX','do':'AUX','had':'AUX','have':'AUX','has':'AUX',
            # Conjunctions
            'and':'CONJ','but':'CONJ','because':'CONJ','however':'CONJ','therefore':'CONJ','so':'CONJ','although':'CONJ','while':'CONJ','if':'CONJ',
            # Adverbs
            'tomorrow':'ADV','yesterday':'ADV','definitely':'ADV','not':'ADV','too':'ADV','suddenly':'ADV',
            'very':'ADV','more':'ADV','now':'ADV','then':'ADV','also':'ADV','clearly':'ADV','efficently':'ADV',
            'efficiently':'ADV','slow':'ADV','initially':'ADV','actually':'ADV','only':'ADV','just':'ADV','early':'ADV',
            # Adjectives
            'long':'ADJ','new':'ADJ','difficult':'ADJ','dim':'ADJ','huge':'ADJ','differnt':'ADJ','different':'ADJ',
            'small':'ADJ','important':'ADJ','visual':'ADJ','spatial':'ADJ','original':'ADJ','compressed':'ADJ',
            'unexpected':'ADJ','financial':'ADJ','serious':'ADJ','clean':'ADJ','large':'ADJ','high':'ADJ','old':'ADJ',
            'artificial':'ADJ','supervised':'ADJ','unsupervised':'ADJ','biased':'ADJ','complex':'ADJ','powerful':'ADJ',
            'good':'ADJ','final':'ADJ','latest':'ADJ','great':'ADJ','restricted':'ADJ',
        }

    def tag_word(self, word, spacy_pos=None):
        """Map word to CFG terminal symbol using lexicon, spacy pos, or morphological heuristics."""
        w = word.lower()
        if w in self.lexicon:
            return self.lexicon[w]
        
        # Fallback to spaCy POS if available
        if spacy_pos:
            pos_map = {
                'NOUN': 'N', 'PROPN': 'N', 'VERB': 'V', 'AUX': 'AUX',
                'DET': 'DET', 'ADJ': 'ADJ', 'ADV': 'ADV', 'ADP': 'P',
                'PRON': 'PRON', 'CCONJ': 'CONJ', 'SCONJ': 'CONJ'
            }
            if spacy_pos in pos_map:
                return pos_map[spacy_pos]

        # Morphological heuristics
        if w.endswith('ly'): return 'ADV'
        if w.endswith('ing') or w.endswith('ed'): return 'V'
        if w.endswith('s') and w[:-1] in self.lexicon and self.lexicon[w[:-1]] == 'N': return 'N'
        if w.endswith('tion') or w.endswith('ment') or w.endswith('ence') or w.endswith('ance'): return 'N'
        if w.endswith('able') or w.endswith('ive') or w.endswith('al') or w.endswith('ous'): return 'ADJ'
        return 'N' if w.isalpha() else 'X'

    def tag(self, tokens, spacy_tags=None):
        if spacy_tags and len(spacy_tags) == len(tokens):
            return [self.tag_word(tokens[i], spacy_tags[i]) for i in range(len(tokens))]
        return [self.tag_word(t) for t in tokens]

    def parse(self, tokens, spacy_tags=None):
        """CKY bottom-up dynamic programming chart parsing algorithm."""
        n = len(tokens)
        if not n:
            return None
        
        tags = self.tag(tokens, spacy_tags)
        chart = {}
        
        # Base case: Span 1 (Terminals and Unary Phrases)
        for i, tag in enumerate(tags):
            chart[(i, i + 1)] = [(tag, tokens[i])]
            # Unary phrase wrappers
            if tag in ('N', 'PRON'):
                chart[(i, i + 1)].append(('NP', (tag, tokens[i])))
            elif tag == 'V':
                chart[(i, i + 1)].append(('VP', (tag, tokens[i])))

        # Inductive case: Span 2 to n (limited to max 16 for responsive interactive latency)
        max_span = min(n + 1, 16)
        for span in range(2, max_span):
            for i in range(n - span + 1):
                j = i + span
                entries = chart.setdefault((i, j), [])
                existing = {e[0] for e in entries}
                for k in range(i + 1, j):
                    left_candidates = chart.get((i, k), [])
                    right_candidates = chart.get((k, j), [])
                    if not left_candidates or not right_candidates:
                        continue
                    for left in left_candidates:
                        for right in right_candidates:
                            for lhs, a, b in self.rules:
                                if left[0] == a and right[0] == b and lhs not in existing:
                                    entries.append((lhs, (left, right), f"{lhs} -> {a} {b}"))
                                    existing.add(lhs)
        
        # Check if full root S exists
        full = self._find_tree(chart.get((0, min(n, max_span - 1)), []), 'S')
        if full:
            return full
        
        # Robust fallback: construct constituent tree from tokens & tags
        return self._robust_tree(tokens, tags)

    def _find_tree(self, entries, label):
        for e in entries:
            if e[0] == label:
                return (label, e[1])
        return None

    def _robust_tree(self, tokens, tags):
        """Constructs a constituent tree when strict chart misses or span limit exceeded."""
        if not tokens:
            return None
        
        split_idx = max(1, len(tokens) // 2)
        # Find first main verb
        for idx, tag in enumerate(tags):
            if tag in ('V', 'AUX') and idx > 0:
                split_idx = idx
                break
                
        subj_tokens = tokens[:split_idx]
        pred_tokens = tokens[split_idx:]
        
        np_children = [(tags[i], subj_tokens[i]) for i in range(len(subj_tokens))]
        vp_children = [(tags[split_idx + i], pred_tokens[i]) for i in range(len(pred_tokens))]
        
        tree = ('S', (
            ('NP', tuple(np_children) if len(np_children) > 1 else np_children[0]),
            ('VP', tuple(vp_children) if len(vp_children) > 1 else vp_children[0])
        ))
        return tree

def sentence_tokens(text):
    return re.findall(r"[A-Za-z0-9_\-]+(?:'[A-Za-z]+)?", text)

def tree_to_lines(tree, depth=0):
    if tree is None:
        return ['(S NO-PARSE)']
    label = tree[0]
    child = tree[1]
    if isinstance(child, str):
        return ['  ' * depth + f'({label} {child})']
    if isinstance(child, tuple) and len(child) == 2 and isinstance(child[1], str):
        return ['  ' * depth + f'({child[0]} {child[1]})']
    lines = ['  ' * depth + f'({label}']
    if isinstance(child, (list, tuple)):
        for c in child:
            lines.extend(tree_to_lines(c, depth + 1))
    lines.append('  ' * depth + ')')
    return lines

def extract_svo(doc):
    """Extracts Subject-Verb-Object triples and dependency relations from spaCy doc."""
    svo_triples = []
    for token in doc:
        if token.pos_ in ('VERB', 'AUX'):
            subj = next((c.text for c in token.children if c.dep_ in ('nsubj', 'nsubjpass', 'csubj')), None)
            dobj = next((c.text for c in token.children if c.dep_ in ('dobj', 'obj', 'attr')), None)
            prep_obj = next((f"{c.text} {p.text}" for c in token.children if c.dep_ == 'prep' for p in c.children if p.dep_ == 'pobj'), None)
            
            obj = dobj or prep_obj
            if subj or obj:
                svo_triples.append({
                    'subject': subj or '(implied/contextual)',
                    'verb': token.lemma_,
                    'object': obj or '(none)',
                    'clause': token.sent.text.strip(),
                    'relationship': f"{subj or 'implied'} → {token.lemma_} → {obj or 'none'}"
                })
    return svo_triples

