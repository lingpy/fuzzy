from lingpy import *
from sys import argv

wl = Wordlist("data/"+argv[1].lower()+".tsv")
etd = wl.get_etymdict(ref="cogids")
count, words, langs, refs = 0, 0, [], 0
for key, idxs_ in etd.items():
    idxs = []
    for idx in idxs_:
        if idx:
            idxs += idx
    languages = [wl[idx, "doculect"] for idx in idxs]
    if "Proto"+argv[1] in languages and len(set(languages)) > 2:
        count += 1
        words += len(set(languages))
        langs += languages
        refs += len(set(languages))-1
print(count, words, len(set(langs)), refs)
