import re
from copy import deepcopy
import collections
import spacy
from nltk.util import ngrams

NLP = spacy.load("en_core_web_md")


def genTrigrams(s):
    s = s.lower()
    # s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
    tokens = [token for token in s.split(" ") if token != ""]
    output = list(ngrams(tokens, 3))
    return output


def common_member(a, b):
    result = collections.Counter(a) & collections.Counter(b)
    return result.keys()


def preprpcess(text):
    doc = NLP(text)
    filtered_tokens = []
    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        filtered_tokens.append(token.lemma_)
    return " ".join(filtered_tokens)


def string_matching(string, string1):
    # print(string1)
    trigrams = []
    trigrams1 = []
    output = []
    output.append(genTrigrams(' '.join(string.split())))
    output.append(genTrigrams(' '.join(string1.split())))

    output[0] = [' '.join(i) for i in output[0]]
    output[1] = [' '.join(i) for i in output[1]]
    trigrams = deepcopy(output[0])
    trigrams1 = deepcopy(output[1])

    # print(trigrams, '\n\n\n')
    # print(trigrams1)
    match = common_member(trigrams, trigrams1)
    m = []
    for i in match:
        m.append(i.split())
    st = 0
    en = st + 1
    # print(m)
    while en < len(m):
        if m[st][-2] == m[en][0] and m[st][-1] == m[en][1]:
            m[en].pop(0)
            m[en].pop(0)
            m[st].extend(m[en])
            m.pop(en)
        else:
            st += 1
            en += 1
    # print(m)
    if len(m) == 0:
        return 'no match'
    while (len(m) > 1):
        if m[0][-1] == m[1][0]:
            m[1].pop(0)
            # m[1].pop(0)
        m[0].extend(m[1])
        m.pop(1)
    # print(m)
    # print(' '.join(m[0]))
    return ' '.join(m[0])
