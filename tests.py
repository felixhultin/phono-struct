import webbrowser

from pprint import pprint

from markov import MarkovChain
from parse.parse import parse
from parse.nst import NST

if __name__ == '__main__':
    webbrowser.register('chromium', webbrowser.Chromium('chromium'))
    db = NST(nrows=1000000, fn="../data/swe030224NST.pron",
             exclude_accronyms=True, exclude_loanwords=True, exclude_inflected=True)
    words = parse(db.df)
    mc = MarkovChain(words)

    initial_three_consonant_cluster = [
        {'consonant': '+', 'vowel': '-'},
        {'consonant': '+', 'vowel': '-'},
        {'consonant': '+', 'vowel': '-'}        
    ]

    # Initial sequences diagram hypotheses
    
    configuration_a = [
        {'phoneme': ['h', 'ɕ' 'ɧ', 'j', 'l', 'r']},
        {'consonant': '+', 'vowel': '-'}
    ]
    
    configuration_b = [
        {'phoneme': ['m', 'n']},
        {'exclude_phonemes': ['j'], 'consonant':'+', 'vowel': '-'}
    ]
    configuration_c = [
        {'phoneme': ['d', 't']},
        {'exclude_phonemes': ['v', 'r'], 'consonant':'+', 'vowel': '-'}
    ]
    configuration_d = [
        {'phoneme': ['b', 'p']},
        {'exclude_phonemes': ['r', 'l', 'j'], 'consonant': '+', 'vowel': '-'}
    ]    
    configuration_b_x = [
        {'phoneme': ['m', 'n']},
        {'consonant':'+', 'vowel': '-'}
    ]
    configuration_c_x = [
        {'phoneme': ['d', 't']},
        {'consonant':'+', 'vowel': '-'}
    ]
    configuration_d_x = [
        {'phoneme': ['b', 'p']},
        {'consonant': '+', 'vowel': '-'}
    ]
    
    configuration_d_x_pj = [
        {'phoneme': 'p'},
        {'phoneme': 'j'}
    ]
    
    # configurations_words = [mc.words(mc.sequence(*pcs)) for pcs in
    #                         (configuration_a, configuration_b,
    #                          configuration_c, configuration_d)]
    
    # Combination analysis of classes - counter hypotheses
    stops_stops = [ {'stop': '+'}, {'stop': '+'}]
    nasals_nasals = [{'nasal': '+'}, {'nasal': '+'}]
    fricatives_fricatives = [ {'fricative': '+'}, {'fricative': '+'} ]
    liquids_liquids = [ {'liquid': '+'}, {'liquid': '+'} ]
    labials_labials = [ {'labial': '+'}, {'labial': '+'} ]
    dentals_dentals = [ {'dental': '+'}, {'dental': '+'} ]
    palatals_palatals = [ {'palatal': '+'},  {'palatal': '+'} ]
    nasals_liquids = [ {'nasal': '+'}, {'liquid': '+'} ]
    stops_nasals = [ {'stop': '+'}, {'nasal': '+'} ]
    
    # classes_words = [mc.words(mc.sequence(*pcs)) for pcs in
    #                  (stops_stops, nasals_nasals,
    #                  fricatives_fricatives, liquids_liquids,
    #                  labials_labials, dentals_dentals,
    #                   palatals_palatals, nasals_liquids, stops_nasals)]


def unique_diacritics(words):
    unique_diacritics = set()
    from functools import reduce
    from parse.definitions import DIACRITICS
    for w, seq in words:
        for s in seq:
            d = reduce(lambda l,r: l+r,
                       list(s[0]) + [c for c in s[2:] if c in DIACRITICS])
        unique_diacritics.add(d)
    return unique_diacritics
