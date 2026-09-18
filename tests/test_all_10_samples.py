"""
Automated Comprehensive Test Suite for Tests 1 - 10
Tests:
1. Did it correct REAL spelling mistakes?
2. Did it avoid changing valid technical words?
3. Did it identify the correct NLP information across syntax, semantics, and discourse?
4. Did it explain WHY each correction and relationship was produced?
"""

import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    try:
        getattr(sys.stdout, 'reconfigure')(encoding='utf-8')
    except Exception:
        pass

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from part1_spellcheck.custom_spell import MySpellCorrector
from part2_parsing.parser import CKYParser
from part3_meaning.semantic import MyMeaningExtractor
from part4_pragmatics.discourse import DiscourseAnalyzer

# Fallback lightweight token mock for spaCy doc if spaCy is not loaded in standalone mode
class MockToken:
    def __init__(self, text, pos='NOUN', dep='ROOT', head=None, tag='NN', i=0):
        self.text = text
        self.lower_ = text.lower()
        self.pos_ = pos
        self.dep_ = dep
        self.head = head or self
        self.tag_ = tag
        self.lemma_ = text.lower()
        self.children = []
        self.ent_type_ = ''
        self.i = i

class MockSentence:
    def __init__(self, text, tokens):
        self.text = text
        self.tokens = tokens
    def __iter__(self):
        return iter(self.tokens)
    def as_doc(self):
        return self

class MockDoc:
    def __init__(self, text):
        self.text = text
        words = text.split()
        self.tokens = [MockToken(w.strip('.,!?;:"()'), i=idx) for idx, w in enumerate(words)]
        self.sents = [MockSentence(text, self.tokens)]
        self.ents = []
    def __iter__(self):
        return iter(self.tokens)

def get_test_samples():
    with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'test_samples.txt'), 'r', encoding='utf-8') as f:
        content = f.read()
    raw_samples = [s.strip() for s in content.split('Sample ') if s.strip()]
    samples = {}
    for s in raw_samples:
        lines = s.split('\n', 1)
        header = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""
        num = int(header.split(':')[0])
        samples[num] = body
    return samples

def run_all_tests():
    spell = MySpellCorrector()
    cky = CKYParser()
    discourse = DiscourseAnalyzer()
    
    # Try to load spaCy model if installed
    try:
        import spacy
        nlp = spacy.load('en_core_web_sm')
        print("Using en_core_web_sm spaCy model.")
    except Exception:
        print("spaCy model not loaded in environment, using rule-based tokenizer for testing.")
        nlp = lambda text: MockDoc(text)
        
    semantic = MyMeaningExtractor(nlp)
    samples = get_test_samples()

    print("\n" + "="*70)
    print("RUNNING TESTS 1 TO 10 ON NLP PIPELINE")
    print("="*70)

    # ---------------------------------------------------------
    # TEST 1: SAR / Earth Observation — Full Pipeline
    # ---------------------------------------------------------
    print("\n🧪 Running Test 1 — SAR / Earth Observation...")
    t1_text = samples[1]
    corrected_1, changes_1 = spell.correct(t1_text)
    
    # 1. Spelling corrections
    orig_to_rep = {c['original'].lower(): c['replacement'].lower() for c in changes_1}
    print(f"  Stage 1 Corrections: {orig_to_rep}")
    assert 'architeture' in orig_to_rep and orig_to_rep['architeture'] == 'architecture', "architeture -> architecture failed"
    assert 'woking' in orig_to_rep and orig_to_rep['woking'] == 'working', "woking -> working failed"
    assert 'satelite' in orig_to_rep and orig_to_rep['satelite'] == 'satellite', "satelite -> satellite failed"
    assert 'differnt' in orig_to_rep and orig_to_rep['differnt'] == 'different', "differnt -> different failed"
    assert 'efficently' in orig_to_rep and orig_to_rep['efficently'] == 'efficiently', "efficently -> efficiently failed"
    assert 'loose' in orig_to_rep and orig_to_rep['loose'] == 'lose', "loose -> lose failed"

    # 2. Must NOT change valid technical words
    for tech in ['EarthMind', 'SAR', 'images', 'transformer', 'encoder', 'tokens']:
        assert tech.lower() not in orig_to_rep, f"Error: Valid technical word '{tech}' was incorrectly altered!"

    # 3. Verify explanations exist
    for c in changes_1:
        assert 'reason' in c and len(c['reason']) > 0, "Missing reason explanation for correction"

    # 4. Semantics & Discourse
    sem_1 = semantic.analyze_sentence(corrected_1, full_doc_text=corrected_1)
    disc_1 = discourse.analyze(corrected_1, nlp(corrected_1))
    
    entities_1 = {e['text'].lower() for e in sem_1['entities']}
    print(f"  Stage 3 Entities: {entities_1}")
    assert any('earthmind' in e for e in entities_1), "Missing EarthMind entity"
    assert any('sar' in e for e in entities_1), "Missing SAR entity"
    assert any('satellite' in e for e in entities_1), "Missing satellite entity"

    connectives_1 = {r['relation'] for r in disc_1['discourse_relations']}
    print(f"  Stage 4 Connectives: {connectives_1}")
    assert 'CAUSE' in connectives_1, "Missing CAUSE relation"
    assert 'CONTRAST' in connectives_1, "Missing CONTRAST relation"
    assert 'RESULT' in connectives_1, "Missing RESULT relation"

    tree_1 = cky.parse(['the', 'model', 'takes', 'the', 'image'])
    assert tree_1 is not None

    print("  ✅ Test 1 Passed!")

    # ---------------------------------------------------------
    # TEST 2: University Email
    # ---------------------------------------------------------
    print("\n🧪 Running Test 2 — University Email...")
    t2_text = samples[2]
    corrected_2, changes_2 = spell.correct(t2_text)
    assert isinstance(changes_2, list)
    disc_2 = discourse.analyze(t2_text, nlp(corrected_2))
    
    pragmatic_inferences = [p['inference'] for p in disc_2['pragmatic_inferences']]
    print(f"  Stage 4 Pragmatic Inferences: {pragmatic_inferences}")
    assert any('REQUEST' in pi for pi in pragmatic_inferences), "Failed to detect request speech act in university email"
    
    rel_2 = {r['relation'] for r in disc_2['discourse_relations']}
    assert 'CAUSE' in rel_2 and 'RESULT' in rel_2 and 'CONTRAST' in rel_2, "Missing expected discourse relations in Test 2"
    print("  ✅ Test 2 Passed!")

    # ---------------------------------------------------------
    # TEST 3: Bank WSD (Main test)
    # ---------------------------------------------------------
    print("\n🧪 Running Test 3 — Bank WSD...")
    t3_text = samples[3]
    corrected_3, changes_3 = spell.correct(t3_text)
    orig_to_rep_3 = {c['original'].lower(): c['replacement'].lower() for c in changes_3}
    
    # Must NOT corrupt 'bank' -> 'back' or 'river' -> 'driver'
    assert 'bank' not in orig_to_rep_3, "CRITICAL ERROR: 'bank' was replaced by spell checker!"
    assert 'river' not in orig_to_rep_3, "CRITICAL ERROR: 'river' was replaced by spell checker!"

    # Disambiguate Bank in Sentence 1 (deposit money) vs Sentence 3 (river / water / construction)
    sents_3 = [s.strip() for s in t3_text.split('.') if s.strip()]
    
    # Financial context test
    bank_fin = semantic.disambiguate_word('bank', sents_3[0], t3_text)
    print(f"  Bank #1 (deposit money) Sense: {bank_fin['sense_label']} — Reason: {bank_fin['reason']}")
    assert bank_fin['sense_label'] == 'FINANCIAL INSTITUTION', f"Expected FINANCIAL INSTITUTION, got {bank_fin['sense_label']}"

    # River bank context test
    bank_riv = semantic.disambiguate_word('bank', sents_3[2], t3_text)
    print(f"  Bank #2 (river / water) Sense: {bank_riv['sense_label']} — Reason: {bank_riv['reason']}")
    assert bank_riv['sense_label'] == 'RIVER BANK / SLOPING SHORE', f"Expected RIVER BANK / SLOPING SHORE, got {bank_riv['sense_label']}"

    disc_3 = discourse.analyze(t3_text, nlp(corrected_3))
    coref_antecedents = {c['mention'].lower(): c['antecedent'].lower() for c in disc_3['coreference_chains']}
    print(f"  Coreference chains: {coref_antecedents}")
    assert 'they' in coref_antecedents, "Expected coreference for 'they'"
    print("  ✅ Test 3 Passed!")

    # ---------------------------------------------------------
    # TEST 4: Coreference Nightmare
    # ---------------------------------------------------------
    print("\n🧪 Running Test 4 — Coreference Nightmare...")
    t4_text = samples[4]
    corrected_4, changes_4 = spell.correct(t4_text)
    # Stage 1: very little or no corrections
    assert len(changes_4) == 0, f"Expected 0 spelling changes on Test 4, got {len(changes_4)}"
    
    disc_4 = discourse.analyze(t4_text, nlp(corrected_4))
    coref_mentions = {c['mention'].lower() for c in disc_4['coreference_chains']}
    print(f"  Coreference Mentions Found: {coref_mentions}")
    assert 'he' in coref_mentions or 'him' in coref_mentions, "Expected male pronoun coreference in Test 4"
    assert 'it' in coref_mentions, "Expected inanimate pronoun 'it' coreference in Test 4"
    print("  ✅ Test 4 Passed!")

    # ---------------------------------------------------------
    # TEST 5: Climate Science
    # ---------------------------------------------------------
    print("\n🧪 Running Test 5 — Climate Science...")
    t5_text = samples[5]
    sem_5 = semantic.analyze_sentence(t5_text, full_doc_text=t5_text)
    disc_5 = discourse.analyze(t5_text, nlp(t5_text))
    
    ent_5 = {e['text'].lower() for e in sem_5['entities']}
    print(f"  Stage 3 Climate Entities: {ent_5}")
    assert any('climate change' in e for e in ent_5), "Missing climate change entity"
    assert any('satellite' in e for e in ent_5), "Missing satellite entity"
    
    coref_5 = {c['mention'].lower(): c['antecedent'].lower() for c in disc_5['coreference_chains']}
    print(f"  Stage 4 Climate Coreference: {coref_5}")
    assert 'this data' in coref_5 or 'these sources' in coref_5, "Missing demonstrative noun phrase resolution in Test 5"
    print("  ✅ Test 5 Passed!")

    # ---------------------------------------------------------
    # TEST 6: Bat WSD (Main test)
    # ---------------------------------------------------------
    print("\n🧪 Running Test 6 — Bat WSD...")
    t6_text = samples[6]
    sents_6 = [s.strip() for s in t6_text.split('.') if s.strip()]
    
    # Sports bat: practice before match
    bat_sports = semantic.disambiguate_word('bat', sents_6[0], t6_text)
    print(f"  Bat #1 (practice / match / swing): {bat_sports['sense_label']} — {bat_sports['reason']}")
    assert bat_sports['sense_label'] == 'SPORTS IMPLEMENT / CRICKET BAT', f"Expected SPORTS IMPLEMENT, got {bat_sports['sense_label']}"

    # Animal bat: flew across the garden
    bat_animal = semantic.disambiguate_word('bat', sents_6[3], t6_text)
    print(f"  Bat #2 (flew across garden): {bat_animal['sense_label']} — {bat_animal['reason']}")
    assert bat_animal['sense_label'] == 'ANIMAL / FLYING MAMMAL', f"Expected ANIMAL / FLYING MAMMAL, got {bat_animal['sense_label']}"

    disc_6 = discourse.analyze(t6_text, nlp(t6_text))
    rel_6 = {r['relation'] for r in disc_6['discourse_relations']}
    assert 'TEMPORAL / CONTRAST' in rel_6 or 'CAUSE' in rel_6, "Missing expected discourse relations in Test 6"
    print("  ✅ Test 6 Passed!")

    # ---------------------------------------------------------
    # TEST 7: Software Engineering
    # ---------------------------------------------------------
    print("\n🧪 Running Test 7 — Software Engineering...")
    t7_text = samples[7]
    disc_7 = discourse.analyze(t7_text, nlp(t7_text))
    sem_7 = semantic.analyze_sentence(t7_text, full_doc_text=t7_text)
    
    ent_7 = {e['text'].lower() for e in sem_7['entities']}
    print(f"  Stage 3 Entities: {ent_7}")
    assert any('nlp' in e for e in ent_7), "Missing NLP entity"
    
    coref_7 = {c['mention'].lower(): c['antecedent'].lower() for c in disc_7['coreference_chains']}
    print(f"  Stage 4 Coreference: {coref_7}")
    assert 'this solution' in coref_7 or 'it' in coref_7, "Missing coreference in Test 7"
    print("  ✅ Test 7 Passed!")

    # ---------------------------------------------------------
    # TEST 8: Machine Learning Assignment
    # ---------------------------------------------------------
    print("\n🧪 Running Test 8 — Machine Learning...")
    t8_text = samples[8]
    corrected_8, changes_8 = spell.correct(t8_text)
    orig_to_rep_8 = {c['original'].lower(): c['replacement'].lower() for c in changes_8}
    print(f"  Stage 1 Corrections: {orig_to_rep_8}")
    assert 'inteligence' in orig_to_rep_8 and orig_to_rep_8['inteligence'] == 'intelligence', "inteligence -> intelligence failed"
    assert 'explictly' in orig_to_rep_8 and orig_to_rep_8['explictly'] == 'explicitly', "explictly -> explicitly failed"

    disc_8 = discourse.analyze(t8_text, nlp(corrected_8))
    rel_8 = {r['relation'] for r in disc_8['discourse_relations']}
    print(f"  Stage 4 Relations: {rel_8}")
    assert 'ELABORATION / EXAMPLE' in rel_8, "Missing ELABORATION / EXAMPLE relation"
    assert 'RESULT / EXPLANATION' in rel_8, "Missing RESULT / EXPLANATION relation"
    print("  ✅ Test 8 Passed!")

    # ---------------------------------------------------------
    # TEST 9: Full Stress Test
    # ---------------------------------------------------------
    print("\n🧪 Running Test 9 — Full Stress Test...")
    t9_text = samples[9]
    corrected_9, changes_9 = spell.correct(t9_text)
    orig_to_rep_9 = {c['original'].lower(): c['replacement'].lower() for c in changes_9}
    print(f"  Stage 1 Corrections: {orig_to_rep_9}")
    assert 'orignal' in orig_to_rep_9 and orig_to_rep_9['orignal'] == 'original', "orignal -> original failed"
    
    # Must NOT corrupt valid technical terms
    for term in ['ai', 'satellite', 'encoder', 'compression', 'architecture', 'representation']:
        assert term not in orig_to_rep_9, f"Technical term '{term}' was erroneously changed!"

    sem_9 = semantic.analyze_sentence(t9_text, full_doc_text=t9_text)
    ent_9 = {e['text'].lower() for e in sem_9['entities']}
    print(f"  Stage 3 Entities: {ent_9}")
    assert any('ai' in e for e in ent_9), "Missing AI entity"
    assert any('vision' in e and 'language' in e for e in ent_9), "Missing vision-language model entity"
    
    disc_9 = discourse.analyze(t9_text, nlp(corrected_9))
    coref_9 = {c['mention'].lower(): c['antecedent'].lower() for c in disc_9['coreference_chains']}
    print(f"  Stage 4 Coreference: {coref_9}")
    assert 'the vehicle' in coref_9 or 'the object' in coref_9, "Missing definite NP resolution in Test 9"
    print("  ✅ Test 9 Passed!")

    # ---------------------------------------------------------
    # TEST 10: Pragmatic Inference
    # ---------------------------------------------------------
    print("\n🧪 Running Test 10 — Pragmatic Inference...")
    t10_text = samples[10]
    corrected_10, changes_10 = spell.correct(t10_text)
    assert len(changes_10) <= 1, f"Expected 0-1 spelling corrections on clean text, got {len(changes_10)}"
    
    disc_10 = discourse.analyze(t10_text, nlp(corrected_10))
    prag_10 = [p['inference'] for p in disc_10['pragmatic_inferences']]
    print(f"  Stage 4 Speech Acts / Inferences: {prag_10}")
    assert any('INDIRECT REQUEST' in p for p in prag_10), "Failed to detect indirect request in Test 10"
    
    coref_10 = {c['mention'].lower(): c['antecedent'].lower() for c in disc_10['coreference_chains']}
    print(f"  Stage 4 Coreference: {coref_10}")
    assert 'his laptop' in coref_10, "Failed to resolve 'his laptop' possessive NP"
    print("  ✅ Test 10 Passed!")

    print("\n" + "="*70)
    print("🎉 ALL 10 TESTS PASSED SUCCESSFULLY!")
    print("="*70)

if __name__ == '__main__':
    run_all_tests()
