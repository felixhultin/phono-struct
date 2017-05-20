from .xsampa import xs2uni
from .definitions import SYLLABLE_BREAK, PHONEMES, DIACRITICS, PROSODIC_MARKERS


def parse(df):
    words = []
    for row_index, row in df.iterrows():
        w, t = row[0], row[11]
        t = xs2uni(t)
        words.append([[w, t], []])
        non_phonemes = []
        phoneme_idx = 0
        for i, c in enumerate(t):
            if i + 1 != len(t) and (t[i + 1] == 'ː' or t[i + 1] == SYLLABLE_BREAK):
                non_phonemes.append(t[i + 1])
            if c in PHONEMES:
                phoneme = (c, phoneme_idx) + \
                    tuple(sorted(np for np in non_phonemes))
                words[row_index][1].append(phoneme)
                non_phonemes = []
                phoneme_idx += 1
            if c in DIACRITICS or c in PROSODIC_MARKERS and c != 'ː':
                if c == 'ˈ' and c in non_phonemes:
                    non_phonemes.remove(c)
                    non_phonemes.append('ˈˈ')
                    continue
                non_phonemes.append(c)
    return words
