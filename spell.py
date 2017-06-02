# Spell Checker from http://norvig.com/spell-correct.html
import re
import json
from collections import Counter

def words(text):
    """."""
    return re.findall(r'\w+', text.lower())

# Cities List from http://www.downloadexcelfiles.com/wo_en/download-excel-file-list-cities-towns-india
cities = words(open('cities.txt').read())
states = words(open('states.txt').read())
WORDS = Counter(cities + states)

#https://en.wikipedia.org/wiki/List_of_renamed_Indian_cities_and_states
mapping = json.load(open('mapping_old_new.json', 'r'))
mapping = {old.lower(): mapping[old] for old in mapping}

def prob(word, num=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / num

def correction(word):
    "Most probable spelling correction for word."
    word = word.lower()
    if word not in mapping:
        # Corrected spelling
        word = max(candidates(word), key=prob).lower()
    if word in mapping:
        return mapping[word.lower()].title()
    else:
        return word.title()

def candidates(word):
    "Generate possible spelling corrections for word."
    return known([word]) or known(edits1(word)) or known(edits2(word)) or [word]

def known(list_of_words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in list_of_words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def main():
    """."""
    while True:
        print "Enter City name: "
        print "Corrected Spelling: {}".format(correction(raw_input()))

if __name__ == '__main__':
    main()
