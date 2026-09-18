import time
import re
from part1_spellcheck.custom_spell import MySpellCorrector
from part2_parsing.parser import CKYParser, sentence_tokens, tree_to_lines, extract_svo, HANDWRITTEN_CFG_RULES
from part3_meaning.semantic import MyMeaningExtractor
from part4_pragmatics.discourse import DiscourseAnalyzer

class SmartPipeline:
    def __init__(self, nlp):
        self.nlp = nlp
        self.spell = MySpellCorrector()
        self.cky = CKYParser()
        self.semantic = MyMeaningExtractor(nlp)
        self.discourse = DiscourseAnalyzer()

    def process(self, raw_text):
        start_time = time.perf_counter()

        # Stage 1: Conservative, domain-safe spell checking
        spell_res = self.spell.correct(raw_text)
        corrected = spell_res.corrected_text
        corrections = spell_res.corrections
        words_scanned = spell_res.words_scanned
        
        doc = self.nlp(corrected)

        # Stage 2 & 3: Sentence-level syntactic parsing and semantic analysis
        syntax_sentences, semantics_sentences = [], []
        all_named_entities, all_domain_concepts, all_wsd = [], [], []
        seen_ent_keys = set()

        for sent in doc.sents:
            toks = sentence_tokens(sent.text)
            sent_doc = sent.as_doc() if hasattr(sent, 'as_doc') else self.nlp(sent.text)
            spacy_tags = [t.pos_ for t in sent_doc]

            svo_triples = extract_svo(sent_doc)
            parsed_tree = self.cky.parse(toks, spacy_tags)

            syntax_sentences.append({
                'sentence': sent.text,
                'pos': [{'token': t.text, 'pos': t.pos_, 'tag': t.tag_} for t in sent],
                'dependencies': [{'token': t.text, 'dep': t.dep_, 'head': t.head.text} for t in sent],
                'svo_triples': svo_triples,
                'cky_tree': tree_to_lines(parsed_tree)
            })

            sem_res = self.semantic.analyze_sentence(sent.text, full_doc_text=corrected)
            semantics_sentences.append(sem_res)

            for ent in sem_res.get('entities', []):
                key = (ent['text'].lower(), ent.get('label'))
                if key not in seen_ent_keys:
                    seen_ent_keys.add(key)
                    if 'Named Entity' in ent.get('category', ''):
                        all_named_entities.append(ent)
                    else:
                        all_domain_concepts.append(ent)

            for wsd in sem_res.get('word_senses', []):
                all_wsd.append({
                    'sentence': sent.text,
                    **wsd
                })

        # Stage 4: Discourse relations, coreference resolution, and pragmatic speech acts
        discourse_res = self.discourse.analyze(corrected, doc)

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        total_svo = sum(len(s.get('svo_triples', [])) for s in syntax_sentences)

        spell_stage = {
            'raw_text': raw_text,
            'corrected_text': corrected,
            'corrections': corrections,
            'words_scanned': words_scanned,
            'words_flagged': len(corrections),
            'accuracy_impact': f"{len(corrections)} spelling correction(s) applied without altering valid domain terms"
        }

        syntax_stage = {
            'sentences': syntax_sentences,
            'grammar_rules': HANDWRITTEN_CFG_RULES,
            'total_sentences': len(syntax_sentences),
            'total_svo_triples': total_svo
        }

        semantics_stage = {
            'sentences': semantics_sentences,
            'named_entities': all_named_entities,
            'domain_concepts': all_domain_concepts,
            'wsd_disambiguations': all_wsd
        }

        discourse_stage = {
            'coreference_chains': discourse_res.get('coreference_chains', []),
            'discourse_relations': discourse_res.get('discourse_relations', []),
            'pragmatic_inferences': discourse_res.get('pragmatic_inferences', [])
        }

        overview_stage = {
            'raw_text': raw_text,
            'corrected_text': corrected,
            'execution_time_ms': elapsed_ms,
            'summary_metrics': {
                'spelling_errors': len(corrections),
                'sentences': len(syntax_sentences),
                'svo_triples': total_svo,
                'entities_and_concepts': len(all_named_entities) + len(all_domain_concepts),
                'wsd_terms': len(all_wsd),
                'coref_chains': len(discourse_res.get('coreference_chains', [])),
                'discourse_relations': len(discourse_res.get('discourse_relations', [])),
                'pragmatic_acts': len(discourse_res.get('pragmatic_inferences', []))
            }
        }

        return {
            'spell': spell_stage,
            'syntax': syntax_stage,
            'semantics': semantics_stage,
            'discourse': discourse_stage,
            'overview': overview_stage,
            # Backward-compatibility aliases
            'raw_text': raw_text,
            'corrected_text': corrected,
            'corrections': corrections
        }

def process(raw_text, nlp):
    return SmartPipeline(nlp).process(raw_text)

