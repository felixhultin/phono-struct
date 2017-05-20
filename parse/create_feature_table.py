import csv

PHONEMES = {'a', 'b', 'd', 'e', 'f', 'h', 'i', 'j', 'k',
            'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'y',
            'ø', 'ŋ', 'œ', 'ɑ', 'ɔ', 'ɖ', 'ɛ', 'ɡ', 'ɧ', 'ɪ', 'ɭ',
            'ɳ', 'ʂ', 'ʈ', 'ʉ', 'ʊ', 'ʏ', 'ʦ', 'ʪ'}


FEATURES = {
    'stop': {'p', 't', 'k', 'b', 'd', 'ɡ'},
    'nasal': {'m', 'n'},
    'fricative': {'s', 'f', 'v', 'j'},
    'liquid': {'l', 'r'},
    'labial': {'p', 'b', 'f', 'm', 'v'},
    'dental': {'s', 't', 'd', 'n', 'l', 'r'},
    'palatal': {'k', 'ɡ', 'j'},
    'consonant': {'b', 'd', 'f', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't',
                  'v', 'ŋ', 'ɖ', 'ɡ', 'ɧ', 'ɭ', 'ɳ', 'ʂ', 'ʈ', 'ʦ', 'ʪ'},
    'vowel': {'a', 'e', 'i', 'ɔ', 'o', 'u', 'y', 'ø', 'œ', 'ɑ', 'ɛ', 'ɪ', 'ʉ', 'ʊ', 'ʏ'}
}


def create_feature_table(fn):
    with open(fn, 'w') as csvfile:
        fieldnames = ['phoneme'] + list(FEATURES)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for p in PHONEMES:
            row = {'phoneme': p} 
            for k,v in FEATURES.items():                
                if p in v:
                    row[k] = 1
                else:
                    row[k] = 0
            writer.writerow(row)


if __name__ == '__main__':
    create_feature_table('data/features.csv')
