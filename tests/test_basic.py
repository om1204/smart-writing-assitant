from part1_spellcheck.custom_spell import MySpellCorrector

def test_levenshtein():
    assert MySpellCorrector.levenshtein('kitten','sitting') == 3

def test_common_fix():
    c=MySpellCorrector()
    fixed, changes=c.correct('I definately recieved the file.')
    assert 'definitely' in fixed.lower()
    assert 'received' in fixed.lower()
    assert len(changes)>=2
