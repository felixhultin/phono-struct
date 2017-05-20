import pandas as pd

#import csv

UNDEFINED_CHARACTERS = {'¤'}

SYLLABLE_BREAK = '$'
DIPHTONG = '*'

PHONEMES = {'a', 'b', 'd', 'e', 'f', 'h', 'i', 'j', 'k',
            'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'y',
            'ø', 'ŋ', 'œ', 'ɑ', 'ɔ', 'ɖ', 'ɛ', 'ɡ', 'ɧ', 'ɪ', 'ɭ',
            'ɳ', 'ʂ', 'ʈ', 'ʉ', 'ʊ', 'ʏ', 'ʦ', 'ʪ'}

CONSONANTS = {'b', 'd', 'f', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't',
              'v', 'ŋ', 'ɖ', 'ɡ', 'ɧ', 'ɭ', 'ɳ', 'ʂ', 'ʈ', 'ʦ', 'ʪ'}

VOWELS = {'a', 'e', 'i', 'ɔ', 'o', 'u', 'y', 'ø', 'œ', 'ɑ', 'ɛ', 'ɪ', 'ʉ', 'ʊ', 'ʏ'}

DIACRITICS = {'ʰ', 'ʲ', '˞', 'ˡ', '̈', '̤', '̪', '̬', '̰', '̴', '̺', '̻'}
PROSODIC_MARKERS = {'ˈ', 'ˌ', 'ː', 'ˈˈ'}

FEATURE_NAMES = {'aspirated': 'ʰ',
                 'palatalized': 'ʲ',
                 'rhotacization': '˞',
                 'lateral release': 'ˡ',
                 'centralized': '̈',
                 'breathy voice': '̤',
                 'dental': '̪',
                 'voiced': '̬',
                 'creaky voice': '̰',
                 'velarized': '̴',
                 'apical': '̺',
                 'laminal': '̻',
                 'primary stress': 'ˈ',
                 'secondary stress': 'ˌ',
                 'extra stress': 'ˈˈ',
                 'long': 'ː',
                 'end of syllable': '$'}

FEATURE_TABLE = pd.read_csv('parse/data/features.csv').set_index('phoneme')


FEATURE_ABBR = {'syl': 'syllabic',
                'son': 'sonorant',
                'cons': 'consonantal',
                'cont': 'continuant',
                'delrel': 'delayed release',
                'lat': 'lateral',
                'nas': 'nasal',
                'strid': 'strident',
                'voi': 'voice', 
                'sg': 'spread glottis',
                'cg': 'constricted glottis',
                'ant': 'anterior',
                'cor': 'coronal',
                'distr': 'distributed',
                'lab': 'labial',
                'hi': 'high (vowel/consonant, not tone)',
                'lo': 'low (vowel/consonant, not tone)',
                'back': 'back',
                'round': 'round',
                'tense': 'tense'}


