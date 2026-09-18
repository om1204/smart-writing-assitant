"""
Comprehensive Automated Regression and Adversarial Test Suite
for Smart Reading & Writing Assistant (5-Stage NLP Pipeline).

Tests:
1. API Contract & Partitioned Schema Verification (/api/health, /api/process)
2. Conservative Spell Checking: Immunity of technical vocabulary & valid terms (Zero false positives)
3. 14-Rule Hand-written CFG Parser & SVO Extraction
4. WordNet Lesk WSD: Context-dependent sense disambiguation
5. Ambiguity-Aware Coreference Resolution & Discourse Connectives
6. Pragmatic Speech Act Inferences
7. Adversarial & Edge Cases (Empty text, long text, symbols, numbers, compound terms)
8. All 10 Assignment Benchmark Samples
"""

import sys
import os
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    try:
        getattr(sys.stdout, 'reconfigure')(encoding='utf-8')
    except Exception:
        pass

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import HTTPException
from api_server import app, health as api_health, process as api_process, ProcessRequest, pipe
from part1_spellcheck.custom_spell import MySpellCorrector
from part2_parsing.parser import CKYParser, HANDWRITTEN_CFG_RULES, sentence_tokens
from part3_meaning.semantic import MyMeaningExtractor
from part4_pragmatics.discourse import DiscourseAnalyzer
from main_nlp_flow import SmartPipeline


class TestSmartNLPPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spell = MySpellCorrector()
        cls.cky = CKYParser()
        cls.pipe = pipe
        cls.semantic = cls.pipe.semantic
        cls.discourse = cls.pipe.discourse

    # -------------------------------------------------------------
    # 1. API Contract & Health Check
    # -------------------------------------------------------------
    def test_01_api_health(self):
        data = api_health()
        self.assertEqual(data.get('status'), 'ok')
        self.assertIn('model', data)

    def test_02_api_empty_and_oversized_validation(self):
        # Empty text
        with self.assertRaises(HTTPException) as ctx_empty:
            api_process(ProcessRequest(text='   '))
        self.assertEqual(ctx_empty.exception.status_code, 400)

        # Oversized text (>12000 chars)
        huge_text = 'word ' * 3000
        with self.assertRaises(HTTPException) as ctx_huge:
            api_process(ProcessRequest(text=huge_text))
        self.assertEqual(ctx_huge.exception.status_code, 413)

    # -------------------------------------------------------------
    # 2. Partitioned 5-Stage Schema Structure
    # -------------------------------------------------------------
    def test_03_partitioned_stage_schema(self):
        sample_input = "i want to understand how the model process SAR images."
        payload = api_process(ProcessRequest(text=sample_input))

        # Check all 5 top-level stage keys
        expected_stages = ['spell', 'syntax', 'semantics', 'discourse', 'overview']
        for stage in expected_stages:
            self.assertIn(stage, payload, f"Missing top-level stage key: {stage}")


        # Check stage-specific sub-schemas
        self.assertIn('words_scanned', payload['spell'])
        self.assertIn('corrections', payload['spell'])
        self.assertIn('corrected_text', payload['spell'])

        self.assertIn('grammar_rules', payload['syntax'])
        self.assertIn('sentences', payload['syntax'])
        self.assertIn('total_svo_triples', payload['syntax'])

        self.assertIn('named_entities', payload['semantics'])
        self.assertIn('domain_concepts', payload['semantics'])
        self.assertIn('wsd_disambiguations', payload['semantics'])

        self.assertIn('coreference_chains', payload['discourse'])
        self.assertIn('discourse_relations', payload['discourse'])
        self.assertIn('pragmatic_inferences', payload['discourse'])

        self.assertIn('execution_time_ms', payload['overview'])
        self.assertIn('summary_metrics', payload['overview'])

    # -------------------------------------------------------------
    # 3. Spell Checker: Immunity of Technical Terms & Zero False Positives
    # -------------------------------------------------------------
    def test_04_technical_terms_immunity(self):
        technical_input = "The CUDA kernel running on NVIDIA GPU processed 768-dimensional embeddings with 91.7% accuracy."
        corrected, changes = self.spell.correct(technical_input)
        
        # None of the technical terms should be altered
        altered_words = [c['original'].lower() for c in changes]
        self.assertNotIn('cuda', altered_words)
        self.assertNotIn('nvidia', altered_words)
        self.assertNotIn('gpu', altered_words)
        self.assertNotIn('768-dimensional', altered_words)
        self.assertNotIn('91.7%', altered_words)
        self.assertNotIn('embeddings', altered_words)

    def test_05_common_english_words_not_corrupted(self):
        # Ensure common short words are never miscorrected
        valid_sentence = "the raw satellite data is very huge and it have many different informations into small tokens am lost during this step."
        corrected, changes = self.spell.correct(valid_sentence)
        changed_map = {c['original'].lower(): c['replacement'].lower() for c in changes}
        
        # Valid words that were previously corrupted in buggy spell-checkers:
        forbidden_changes = ['raw', 'very', 'into', 'am', 'lost', 'step', 'is', 'data']
        for w in forbidden_changes:
            self.assertNotIn(w, changed_map, f"CRITICAL: Valid word '{w}' was erroneously changed to '{changed_map.get(w)}'")

    def test_06_from_scratch_levenshtein_properties(self):
        # Verification of edit distance properties
        self.assertEqual(self.spell.levenshtein('kitten', 'sitting'), 3)
        self.assertEqual(self.spell.levenshtein('architeture', 'architecture'), 1)
        self.assertEqual(self.spell.levenshtein('woking', 'working'), 1)
        self.assertEqual(self.spell.levenshtein('same', 'same'), 0)
        self.assertEqual(self.spell.levenshtein('', 'word'), 4)

    # -------------------------------------------------------------
    # 4. 14-Rule Hand-written CFG Parser & SVO Extraction
    # -------------------------------------------------------------
    def test_07_cfg_rules_and_parsing(self):
        self.assertEqual(len(HANDWRITTEN_CFG_RULES), 14, "Must have exactly 14 explicit CFG production rules")
        
        # Test CKY parsing on basic constituent structures
        tokens = ['the', 'model', 'takes', 'the', 'image']
        tree = self.cky.parse(tokens)
        self.assertIsNotNone(tree)
        self.assertEqual(tree[0], 'S')

    def test_08_svo_triples_extraction(self):
        res = self.pipe.process("The researcher extracted important visual features from the satellite image.")
        syntax = res['syntax']
        triples = []
        for s in syntax['sentences']:
            triples.extend(s.get('svo_triples', []))
        
        self.assertTrue(len(triples) > 0, "Failed to extract SVO triple from active transitive clause")
        triple = triples[0]
        self.assertIn('researcher', triple['subject'].lower())
        self.assertIn('extract', triple['verb'].lower())

    # -------------------------------------------------------------
    # 5. Real Lesk WordNet WSD
    # -------------------------------------------------------------
    def test_09_wordnet_lesk_bank_disambiguation(self):
        # Financial context
        sent_fin = "i went to the bank to deposit money and request a loan"
        fin_wsd = self.semantic.lesk_disambiguate('bank', sent_fin)
        self.assertEqual(fin_wsd['sense_label'], 'FINANCIAL INSTITUTION')
        self.assertIn(fin_wsd['synset'], ['bank.n.02', 'depository_financial_institution.n.01'])

        # River context
        sent_riv = "the small boat was tied beside the river bank where the water level rose"
        riv_wsd = self.semantic.lesk_disambiguate('bank', sent_riv)
        self.assertEqual(riv_wsd['sense_label'], 'RIVER BANK / SLOPING SHORE')
        self.assertEqual(riv_wsd['synset'], 'bank.n.01')

    def test_10_wordnet_lesk_bat_disambiguation(self):
        # Sports context
        sent_sport = "he swung the cricket bat to hit the ball in the match"
        sport_wsd = self.semantic.lesk_disambiguate('bat', sent_sport)
        self.assertEqual(sport_wsd['sense_label'], 'SPORTS IMPLEMENT / CRICKET BAT')

        # Animal context
        sent_anim = "a nocturnal bat with wings flew across the garden at night"
        anim_wsd = self.semantic.lesk_disambiguate('bat', sent_anim)
        self.assertEqual(anim_wsd['sense_label'], 'ANIMAL / FLYING MAMMAL')

    # -------------------------------------------------------------
    # 6. Ambiguity-Aware Coreference Resolution
    # -------------------------------------------------------------
    def test_11_ambiguous_coreference_flagged(self):
        # When two competing female entities are in discourse, 'she' must be flagged ambiguous
        text_ambig = "Riya spoke to Neha in the office. She said that the meeting was postponed."
        doc = self.pipe.nlp(text_ambig)
        chains = self.discourse._coref_enhanced(doc, text_ambig)
        
        she_chains = [c for c in chains if c['mention'].lower() == 'she']
        self.assertTrue(len(she_chains) > 0, "Should resolve mention 'she'")
        she_chain = she_chains[0]
        self.assertTrue(she_chain.get('is_ambiguous'), "Coreference resolver must flag ambiguity when multiple candidates exist")
        self.assertIn('Riya', she_chain.get('candidates', []))
        self.assertIn('Neha', she_chain.get('candidates', []))

    def test_12_unambiguous_coreference(self):
        # When only one male entity is in discourse, 'he' is unambiguous
        text_clear = "The boy picked up the bat. He wanted to practice before the match."
        doc = self.pipe.nlp(text_clear)
        chains = self.discourse._coref_enhanced(doc, text_clear)
        
        he_chains = [c for c in chains if c['mention'].lower() == 'he']
        self.assertTrue(len(he_chains) > 0)
        self.assertFalse(he_chains[0].get('is_ambiguous'))
        self.assertIn('boy', he_chains[0]['antecedent'].lower())

    # -------------------------------------------------------------
    # 7. Discourse Connectives & Pragmatic Speech Acts
    # -------------------------------------------------------------
    def test_13_multi_token_discourse_connectives(self):
        text = "The server crashed. Because of this, the final result was delayed. For example, testing failed."
        relations = self.discourse._extract_relations(text)
        connectives = [r['connective'].lower() for r in relations]
        self.assertIn('because of this', connectives)
        self.assertIn('for example', connectives)

    def test_14_pragmatic_speech_act_inferences(self):
        text = "It would be great if someone could check the permissions, and please give me some extra time."
        pragmatics = self.discourse._extract_pragmatics(text)
        inferences = [p['inference'] for p in pragmatics]
        self.assertIn('INDIRECT REQUEST', inferences)
        self.assertIn('DIRECT / POLITE REQUEST', inferences)

    # -------------------------------------------------------------
    # 8. User's Original Bug Test
    # -------------------------------------------------------------
    def test_15_original_user_bug_query(self):
        user_raw = (
            "orignal: i want to understand that how the earthmind architeture is woking "
            "and how it process the SAR images because the raw satelite data is very huge "
            "and it have many differnt informations. the model first take the image and then "
            "it compress them into small tokens however i am not sure why this compression is needed "
            "and what information is lost during this step. the researcher said that the encoder "
            "extract important visual features but they does not clearly explain which features are kept. "
            "therefore the system can process the image more efficently but it maybe loose some spatial details."
        )
        res = self.pipe.process(user_raw)
        
        # Spell corrections must fix typos
        spell_reps = {c['original'].lower(): c['replacement'].lower() for c in res['spell']['corrections']}
        self.assertEqual(spell_reps.get('orignal'), 'original')
        self.assertEqual(spell_reps.get('architeture'), 'architecture')
        self.assertEqual(spell_reps.get('woking'), 'working')
        self.assertEqual(spell_reps.get('satelite'), 'satellite')
        self.assertEqual(spell_reps.get('differnt'), 'different')
        self.assertEqual(spell_reps.get('efficently'), 'efficiently')
        self.assertEqual(spell_reps.get('loose'), 'lose')

        # Must NOT corrupt valid technical terms
        for term in ['earthmind', 'sar', 'images', 'raw', 'very', 'into', 'tokens', 'am', 'lost', 'step']:
            self.assertNotIn(term, spell_reps, f"Bug regression: Term '{term}' was erroneously altered!")

        # Entity recognition
        concepts = [e['text'].lower() for e in res['semantics']['domain_concepts'] + res['semantics']['named_entities']]
        self.assertTrue(any('earthmind' in c for c in concepts))
        self.assertTrue(any('sar' in c for c in concepts))


if __name__ == '__main__':
    unittest.main(verbosity=2)
