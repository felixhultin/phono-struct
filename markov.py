import copy
import json
import webbrowser

from collections import Counter

from parse.definitions import CONSONANTS, VOWELS, FEATURE_TABLE


class MarkovChain:

    START = "__START__"
    END = "__END__"

    def __init__(self, sequences, reverse=False,
                 json_file='web/data/chain.json',
                 front_end='web/index.html'):
        self.tree = self.create_tree(sequences)
        self.tree = self.normalize(self.tree)

    def create_tree(self, sequences):
        tree = {}
        for row, sequence in sequences:
            children = tree
            for idx, s in enumerate(sequence):
                symbol, pos, *features = s
                if symbol not in children:
                    children[symbol] = {'frequency': 1, 'position': pos,
                                        'features': Counter(features),
                                        'accept': (idx == len(sequence) - 1)}
                else:
                    children[symbol]['frequency'] += 1
                    children[symbol]['features'].update(features)
                if idx == len(sequence) - 1:
                    children[symbol]['accept'] = True
                    children[symbol]['word'] = row[0]
                    children[symbol]['transcription'] = sequence
                else:
                    if 'children' not in children[symbol]:                   
                        children[symbol]['children'] = {}
                    children = children[symbol]['children']
        return tree

    def info(self):
        count = 0
        stack = list(self.tree.items())
        while stack:
            k, v = stack.pop()
            count += 1
            if 'children' in v:
                stack.extend(v['children'].items())
        return count, count-1

    def normalize(self, tree):
        freq = sum(v['frequency'] for k, v in tree.items())
        if freq == 0:
            from pdb import set_trace
            set_trace()
        for key in tree:
            tree[key]['probability'] = tree[key]['frequency'] / freq
            if 'children' in tree[key]:
                self.normalize(tree[key]['children'])
        return tree

    def sequence(self, *phonemes):        
        def filter_tree(tree, phonemes):
            if not tree:
                return tree
            n_pos = next(iter(tree.values()))['position']
            pc = phonemes[n_pos] if n_pos < len(phonemes) else None
            if type(pc) == dict:
                p_expr = pc.get('phoneme')
                if (type(p_expr) == str):
                    tree = {p_expr: tree[p_expr]} if p_expr in tree else {}
                if (type(p_expr) == list):
                    tree = {k:v for k,v in tree.items() if k in p_expr}
                include_phonemes = pc.get('include_phonemes')
                include_phonemes = include_phonemes if include_phonemes else set()
                if pc.get('exclude_phonemes'):
                    tree = {k:v for k,v in tree.items()
                            if k not in pc.get('exclude_phonemes')}
                for ft, value in pc.items():
                    if ft == 'phoneme' or ft == 'exclude_phonemes' or \
                       ft == 'include_phonemes':
                        continue
                    if ft not in FEATURE_TABLE.columns:
                        raise ValueError("Feature not in feature table")
                    value = 1 if value == '+' else 0 if value == '-' else value
                    tree = {k:v for k,v in tree.items() if
                            FEATURE_TABLE.ix[k][ft] == value or k in include_phonemes}
            if type(pc) == str and pc != '*':
                tree = {pc: tree[pc]} if pc in tree else {}
            for n in tree:
                if 'children' not in tree[n]:
                    continue
                tree[n]['children'] = filter_tree(tree[n]['children'], phonemes)
                tree[n]['frequency'] = sum(v['frequency']
                                           for k,v in tree[n]['children'].items())
            if n_pos < len(phonemes) - 1 and pc:
                tree = {k:v for k,v in tree.items() if tree[k]['children']}            
            return tree
        return self.normalize(filter_tree(copy.deepcopy(self.tree), phonemes))
    
    def words(self, tree):
        words = []
        stack = list(tree.items())
        while stack:
            k, v = stack.pop()
            if v['accept']:
                words.append(v['word'])
            if 'children' in v:
                stack.extend(v['children'].items())
        return words

    
    def combinations(self, *phonemes):
        sequence = self.sequence(self.tree, phonemes)        

    def to_json(self, tree=None):
        tree = self.tree if tree is None else tree
        root = {'name': self.START,
                'children': self.serialize_to_json(tree)}
        return json.dumps(root, separators=(',', ':'))

    def serialize_to_json(self, tree):
        json_tree = []
        for k, v in tree.items():
            json_obj = {'name': k, 'pos': v['position'],
                        'f': v['frequency'],
                        'probability': v['probability'],
                        'accept': v['accept'],
                        'ft': [{'feature': f, 'f': freq}
                               for f, freq in v['features'].items()],
                        }
            if json_obj['accept']:
                json_obj['word'] = v['word']
            json_tree.append(json_obj)
            children = v.get('children')
            if v.get('children'):
                json_obj['children'] = self.serialize_to_json(children)
        return json_tree

    def visualize(self, tree=None):
        json_tree = self.to_json(self.tree) if tree is None else self.to_json(tree)
        with open("web/data/chain_var.json", "w") as jsonfile:
            jsonfile.write("var json = " + json_tree + ";")
        webbrowser.open('web/index.html')




if __name__ == '__main__':
    import webbrowser
    from pprint import pprint
    
    from parse.parse import parse
    from parse.nst import NST

    initial_three_consonant_cluster = [
        {'phoneme': 's'},
        {'consonant': '+', 'vowel': '-'},
        {'consonant': '+', 'vowel': '-'}
    ]
    
    webbrowser.register('chromium', webbrowser.Chromium('chromium'))
    db = NST(nrows=1000000, fn="../data/swe030224NST.pron",
             exclude_accronyms=True, exclude_loanwords=True, exclude_inflected=True)
    words = parse(db.df)
    mc = MarkovChain(words)
    # mc.visualize(mc.sequence(*initial_consonant_cluster))
    
