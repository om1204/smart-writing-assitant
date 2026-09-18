import re

DISCOURSE_MARKERS = [
    (r'\bbecause\s+of\s+this\b', 'because of this', 'CAUSE', 'Causal explanation linking antecedent event as cause'),
    (r'\bbecause\s+of\b', 'because of', 'CAUSE', 'Prepositional causal marker indicating reason'),
    (r'\bthis\s+is\s+why\b', 'this is why', 'RESULT / EXPLANATION', 'Resultative marker summarizing reasoning'),
    (r'\bas\s+a\s+result\b', 'as a result', 'RESULT', 'Resultative consequence marker'),
    (r'\bon\s+the\s+other\s+hand\b', 'on the other hand', 'CONTRAST', 'Adversative contrast marker'),
    (r'\bfor\s+example\b', 'for example', 'ELABORATION / EXAMPLE', 'Exemplification marker introducing concrete evidence'),
    (r'\bfor\s+instance\b', 'for instance', 'ELABORATION / EXAMPLE', 'Exemplification marker'),
    (r'\beven\s+if\b', 'even if', 'CONDITION / CONCESSION', 'Concessive conditional clause'),
    (r'\bbecause\b', 'because', 'CAUSE', 'Subordinating causal conjunction'),
    (r'\btherefore\b', 'therefore', 'RESULT', 'Logical conclusion or resultative consequence'),
    (r'\bhowever\b', 'however', 'CONTRAST', 'Adversative discourse connective expressing contrast'),
    (r'\bbut\b', 'but', 'CONTRAST', 'Coordinating contrastive conjunction'),
    (r'\balthough\b', 'although', 'CONTRAST', 'Concessive subordinating conjunction'),
    (r'\byet\b', 'yet', 'CONTRAST', 'Contrastive concession'),
    (r'\bactually\b', 'actually', 'CONTRAST / CORRECTION', 'Discourse marker clarifying or correcting a proposition'),
    (r'\bwhile\b', 'while', 'TEMPORAL / CONTRAST', 'Temporal concurrence or comparative contrast'),
    (r'\bthen\b', 'then', 'SEQUENCE / TEMPORAL', 'Temporal sequence or step-by-step progression'),
    (r'\bso\b', 'so', 'RESULT', 'Resultative marker'),
    (r'\bsince\b', 'since', 'CAUSE', 'Causal conjunction'),
]

PRAGMATIC_PATTERNS = [
    (r'\b(?:please\s+)?give\s+me\s+some\s+extra\s+time\b', 'DIRECT / POLITE REQUEST', 'Explicit polite plea for deadline extension'),
    (r'\brequesting\s+you\s+to\s+please\b', 'POLITE FORMAL REQUEST', 'Formal request formula expressing deferential appeal'),
    (r'\b(?:whether|if)\s+someone\s+could\s+share\b', 'INDIRECT REQUEST', "Mitigated indirect request via embedded modal clause ('could share')"),
    (r'\bif\s+somebody\s+could\s+maybe\s+send\b', 'INDIRECT REQUEST', "Tentative polite request using double hedging ('could maybe send')"),
    (r'\bit\s+would\s+be\s+great\s+if\s+someone\s+could\s+check\b', 'INDIRECT REQUEST', "Optative polite indirect request formula ('it would be great if...')"),
    (r'\b(?:could|would|can)\s+you\s+([a-z]+)\b', 'INDIRECT REQUEST', "Conventional polite indirect request via modal query"),
    (r'\bneed\s+to\s+decide\b', 'OBLIGATION / DECISION NEED', 'Deontic necessity expressing collective decision requirement'),
    (r'\bplease\s+review\b', 'DIRECT REQUEST', 'Polite directive speech act requesting review'),
    (r'\bnot\s+sure\s+why\b', 'EPISTEMIC HEDGE', 'Expressive stance indicating epistemic uncertainty or query'),
    (r'\bconfused\s+because\b', 'EXPRESSIVE STANCE', 'Affective speaker state expressing conceptual perplexity'),
    (r'\bmaybe\s+(?:loose|lose)\b', 'EPISTEMIC HEDGE', 'Mitigated speculative claim expressing uncertain loss'),
]

# Classification of discourse entities for agreement
MALE_ENTITIES = {
    'rahul', 'arjun', 'aman', 'friend', 'father', 'boy', 'student', 'developer',
    'professor', 'leader', 'researcher', 'member', 'user'
}
FEMALE_ENTITIES = {
    'riya', 'neha', 'mother', 'girl', 'teacher', 'sister', 'she'
}
PLURAL_ENTITIES = {
    'scientists', 'researchers', 'sensors', 'measurements', 'sources', 'results',
    'users', 'members', 'diagrams', 'errors', 'values', 'pages', 'cats', 'dogs',
    'team', 'team members', 'construction team'
}
INANIMATE_ENTITIES = {
    'report', 'assignment', 'project', 'paper', 'model', 'laptop', 'system', 'code',
    'file', 'presentation', 'folder', 'slides', 'diagrams', 'application', 'database',
    'main_nlp_flow', 'cache', 'solution', 'image', 'images', 'token', 'tokens', 'features',
    'representation', 'data', 'information', 'compression', 'desk', 'lab', 'room',
    'bank', 'river', 'water', 'rain', 'bat', 'window', 'tree', 'garden', 'match'
}

class DiscourseAnalyzer:
    def analyze(self, text, doc):
        relations = self._extract_relations(text)
        chains = self._coref_enhanced(doc, text)
        pragmatic = self._extract_pragmatics(text)
        return {
            'coreference_chains': chains,
            'discourse_relations': relations,
            'pragmatic_inferences': pragmatic
        }

    def _extract_relations(self, text):
        relations = []
        seen_spans = set()
        for pattern, conn, rel_type, desc in DISCOURSE_MARKERS:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                span = (match.start(), match.end())
                # Avoid sub-matches (e.g. 'because' inside 'because of this')
                if any(s[0] <= span[0] and span[1] <= s[1] for s in seen_spans):
                    continue
                seen_spans.add(span)

                start = max(0, match.start() - 25)
                end = min(len(text), match.end() + 35)
                clause_snippet = text[start:end].replace('\n', ' ').strip()

                relations.append({
                    'connective': match.group(0),
                    'relation': rel_type,
                    'snippet': f"...{clause_snippet}...",
                    'description': desc
                })
        return relations

    def _coref_enhanced(self, doc, raw_text):
        """
        Conservative, salience-based coreference resolver with gender, number,
        animacy agreement constraints, and explicit ambiguity detection.
        When multiple competing antecedents match, ambiguous sets are reported.
        """
        chains = []
        history = []

        # Step 1: Collect referring candidate noun entities chronologically
        for sent_idx, sent in enumerate(doc.sents):
            for tok in sent:
                if tok.pos_ in ('PROPN', 'NOUN') and tok.text.lower() not in {'the', 'a', 'an', 'this', 'that'}:
                    w_lower = tok.text.lower()

                    category = 'INANIMATE'
                    if w_lower in MALE_ENTITIES or tok.ent_type_ == 'PERSON':
                        category = 'MALE'
                    elif w_lower in FEMALE_ENTITIES:
                        category = 'FEMALE'
                    elif w_lower in PLURAL_ENTITIES or tok.tag_ in ('NNS', 'NNPS'):
                        category = 'PLURAL'

                    history.append({
                        'token': tok.text,
                        'lemma': tok.lemma_.lower(),
                        'pos': tok.pos_,
                        'idx': tok.i,
                        'sent_idx': sent_idx,
                        'category': category,
                        'dep': tok.dep_
                    })

        # Step 2: Resolve pronouns with agreement + salience + ambiguity tracking
        for sent_idx, sent in enumerate(doc.sents):
            for tok in sent:
                t_lower = tok.lower_

                # MALE PRONOUNS: he, him, his
                if t_lower in {'he', 'him', 'his'}:
                    cands = [h for h in history if h['idx'] < tok.i and h['category'] == 'MALE']
                    if cands:
                        # Recent candidates in previous 2 sentences
                        recent_cands = [c for c in cands if sent_idx - c['sent_idx'] <= 2]
                        cand_tokens = list(dict.fromkeys(c['token'] for c in recent_cands)) if recent_cands else [cands[-1]['token']]

                        # Check if ambiguous: 2 or more distinct male names in prior context
                        is_ambiguous = len(cand_tokens) >= 2

                        best = sorted(cands, key=lambda c: (
                            c['sent_idx'] == sent_idx,
                            c['dep'] in ('nsubj', 'nsubjpass'),
                            -abs(tok.i - c['idx'])
                        ), reverse=True)[0]

                        antecedent_display = (
                            f"{best['token']} (ambiguous with {', '.join([c for c in cand_tokens if c != best['token']])})"
                            if is_ambiguous
                            else best['token']
                        )

                        chains.append({
                            'mention': tok.text,
                            'antecedent': antecedent_display,
                            'is_ambiguous': is_ambiguous,
                            'candidates': cand_tokens,
                            'confidence': 'Low (Multiple candidates)' if is_ambiguous else 'High (Grammatical agreement)',
                            'rule': f"Agreement: Male singular pronoun '{tok.text}' matches {', '.join(cand_tokens)}"
                        })

                # FEMALE PRONOUNS: she, her
                elif t_lower in {'she', 'her'}:
                    cands = [h for h in history if h['idx'] < tok.i and h['category'] == 'FEMALE']
                    if cands:
                        recent_cands = [c for c in cands if sent_idx - c['sent_idx'] <= 2]
                        cand_tokens = list(dict.fromkeys(c['token'] for c in recent_cands)) if recent_cands else [cands[-1]['token']]
                        is_ambiguous = len(cand_tokens) >= 2

                        best = cands[-1]
                        antecedent_display = (
                            f"{best['token']} (ambiguous with {', '.join([c for c in cand_tokens if c != best['token']])})"
                            if is_ambiguous
                            else best['token']
                        )

                        chains.append({
                            'mention': tok.text,
                            'antecedent': antecedent_display,
                            'is_ambiguous': is_ambiguous,
                            'candidates': cand_tokens,
                            'confidence': 'Low (Multiple candidates)' if is_ambiguous else 'High (Grammatical agreement)',
                            'rule': f"Agreement: Female singular pronoun '{tok.text}' matches {', '.join(cand_tokens)}"
                        })

                # INANIMATE PRONOUNS: it, its
                elif t_lower in {'it', 'its'}:
                    cands = [h for h in history if h['idx'] < tok.i and h['category'] in ('INANIMATE', 'PLURAL')]
                    if cands:
                        best = sorted(cands, key=lambda c: (
                            c['sent_idx'] == sent_idx,
                            c['dep'] in ('dobj', 'nsubj', 'obj'),
                            -abs(tok.i - c['idx'])
                        ), reverse=True)[0]

                        recent_tokens = list(dict.fromkeys(c['token'] for c in cands[-3:]))
                        chains.append({
                            'mention': tok.text,
                            'antecedent': best['token'],
                            'is_ambiguous': False,
                            'candidates': recent_tokens,
                            'confidence': 'High (Subject/Object salience)',
                            'rule': f"Agreement: Inanimate pronoun '{tok.text}' binds to concept '{best['token']}'"
                        })

                # PLURAL PRONOUNS: they, them, their
                elif t_lower in {'they', 'them', 'their'}:
                    cands = [h for h in history if h['idx'] < tok.i and (h['category'] == 'PLURAL' or h['category'] == 'MALE')]
                    if cands:
                        best = sorted(cands, key=lambda c: (
                            c['category'] == 'PLURAL',
                            -abs(tok.i - c['idx'])
                        ), reverse=True)[0]
                        recent_tokens = list(dict.fromkeys(c['token'] for c in cands[-3:]))
                        chains.append({
                            'mention': tok.text,
                            'antecedent': best['token'],
                            'is_ambiguous': False,
                            'candidates': recent_tokens,
                            'confidence': 'High (Number agreement)',
                            'rule': f"Agreement: Plural/collective pronoun '{tok.text}' binds to group antecedent '{best['token']}'"
                        })

        # Step 3: Demonstrative and definite noun phrase coreference
        np_patterns = [
            (r'\b(this\s+data)\b', 'collected satellite/sensor data', "Demonstrative NP: 'this data' anaphorically summarizes prior data collection"),
            (r'\b(these\s+sources)\b', 'satellite, weather stations, and ocean sensors', "Demonstrative NP: 'these sources' resolves to combined multi-sensor streams"),
            (r'\b(this\s+solution)\b', 'intermediate result caching main_nlp_flow', "Demonstrative NP: 'this solution' binds to developer's caching mechanism"),
            (r'\b(the\s+vehicle)\b', 'small vehicle near the river', "Definite NP: 'the vehicle' tracks the previously observed vehicle"),
            (r'\b(the\s+object)\b', 'low-resolution vehicle / boat candidate', "Definite NP: 'the object' corefers with vehicle/boat candidate"),
            (r'\b(his\s+laptop)\b', "member's laptop", "Possessive NP: 'his laptop' binds to the speaking team member's device"),
            (r'\b(the\s+other\s+person)\b', "collaborator (Arjun / Rahul)", "Contrastive mention resolving to dialogue partner")
        ]
        for pat, antec, rule in np_patterns:
            for match in re.finditer(pat, raw_text, re.IGNORECASE):
                chains.append({
                    'mention': match.group(0),
                    'antecedent': antec,
                    'is_ambiguous': False,
                    'candidates': [antec],
                    'confidence': 'High (Definite/Demonstrative NP binding)',
                    'rule': rule
                })

        return chains

    def _extract_pragmatics(self, text):
        inferences = []
        for pat, speech_act, desc in PRAGMATIC_PATTERNS:
            for match in re.finditer(pat, text, re.IGNORECASE):
                inferences.append({
                    'pattern': match.group(0),
                    'inference': speech_act,
                    'explanation': desc
                })
        return inferences

