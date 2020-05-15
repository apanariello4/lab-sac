#!bin/bash

import sys, re, random

def mimic(s):
    wordsDict = {}
    with open(s, 'rt') as f:
        data = f.read()
        words = re.findall('\w+', data.lower())
        for i, word in enumerate(words):
            if i+1 < len(words):
                if word not in wordsDict.keys():
                   wordsDict[word] = [words[i+1]]
                else:
                    wordsDict[word].append(words[i+1])
    return wordsDict

def phrase(m):
    randomPhrase = [random.choice(list(m.keys())) + ""]
    for i in range(10):
        randomPhrase.append(random.choice(m[randomPhrase[-1]]))
    return ' '.join(randomPhrase)

def main(s):
    print(phrase(mimic(s)))

if __name__ == '__main__':
    main(sys.argv[1])