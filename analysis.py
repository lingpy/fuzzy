"""
Analysis for the study on fuzzy reconstructions.
"""
from lingrex.fuzzy import FuzzyReconstructor, ntile
from lingpy import Wordlist, basictypes, Alignments
from lingrex.reconstruct import transform_alignment
from functools import partial
from sklearn.svm import SVC
from sys import argv
from tabulate import tabulate
import random
import itertools
import networkx as nx
from tqdm import tqdm as progressbar

random.seed(1234)

# switch if you want to use alignment in the source
align_data = True

align_s = partial(
        transform_alignment, align=align_data, position=False, 
        prosody=True, startend=False, gap="-")

proto_language = "Proto"+argv[1]

clf = lambda : SVC(kernel="linear")
wl = Alignments("data/{0}.tsv".format(argv[1].lower()), ref="cogids",
        transcription="form")
print("[i] loaded wordlist")
fr = FuzzyReconstructor(wl, proto_language, ref="cogids")
print("[i] loaded fuzzy reconstructor")
fr.random_splits(10, retain=0.9)
print("[i] carried out random splits")
fr.fit_samples(clf=clf, onehot=True, func=align_s, aligned=True if not
        align_data else False, pb=True)

output = []

# now, we iterate over individual etymologies and predict them one by one
hits, fails = 0, 0
etd = wl.get_etymdict(ref="cogids")
all_languages = [l for l in wl.cols if l != proto_language]
confusion = nx.Graph()
ntile_dict = {}
for cogid, idxs_ in progressbar(etd.items(), desc="predictions"):
    idxs = []
    for idx in idxs_:
        if idx:
            idxs += [idx[0]]
    languages = [wl[idx, "doculect"] for idx in idxs]
    tokens = []
    for idx in idxs:
        tokens += [basictypes.lists(wl[idx, "tokens" if align_data else "alignment"]).n[
            wl[idx, "cogids"].index(cogid)]]

    if proto_language in languages and len(languages) > 2:
        selected_idxs, selected_languages, selected_tokens = [], [], []
        for idx, language, tks in zip(idxs, languages, tokens):
            if language != proto_language:
                selected_idxs += [idx]
                selected_languages += [language]
                selected_tokens += [tks]
        target_word = " ".join(
                [y for x, y in zip(languages, tokens) if x == proto_language][0]
                )

        words, pred = fr.predict(
                selected_tokens, selected_languages, output="wp")
        sounds = []
        for i, snd in enumerate(pred):
            sound, score = snd.split("¦")[0].split(":")
            if score == "100":
                if sound != "-":
                    sounds += [sound]
            else:
                sounds += ["?"]
                all_sounds = snd.split("¦")
                for sA, sB in itertools.combinations(all_sounds, r=2):
                    sndA, scoreA = sA.split(":")
                    sndB, scoreB = sB.split(":")
                    try:
                        confusion[sndA][sndB]["vals"] += [(cogid, i, scoreA, scoreB)]
                    except:
                        confusion.add_edge(
                                sndA,
                                sndB, vals=[(cogid, i, scoreA, scoreB)])
        if " ".join(sounds) == target_word:
            hits += 1
            ntile_dict[cogid] = (1, target_word)
        else:
            ntile_dict[cogid] = (0, ntile(words))
            fails += 1
            alm = align_s(selected_tokens, selected_languages,
                    all_languages)
            almr = []
            for i in range(len(all_languages)):
                try:
                    oridx = selected_languages.index(all_languages[i])
                    idx = selected_idxs[oridx]
                    concept = wl[idx, "concept"]
                    cogidx = wl[idx, "cogids"].index(cogid)
                except:
                    concept = ""
                    cogidx = ""
                almr += [[
                    all_languages[i],
                    concept,
                    cogidx
                    ]+[row[i] for row in alm]]
            almr += [["Fuzzy", "", "",]+pred]
            almr += [[proto_language, "", ""]+target_word.split(" ")]
            output += [[cogid, wl[idxs[0], "concept"], almr, len(almr[0])]]

# create ntile output
print("[i] writing quintiles to wordlist file")
wl.add_entries("quintiles", "tokens", lambda x: x)
# align data only for burmish and karen
if argv[1] in ["Karen", "Burmish"]:
    wl.align()
for idx, doculect, tokens, cogids in wl.iter_rows("doculect", "tokens", "cogids"):
    if doculect == "Proto" + argv[1]:
        words = []
        for i, cogid in enumerate(cogids):
            if cogid in ntile_dict:
                success, value = ntile_dict[cogid]
                if success:
                    words += ["( "+value+" )"]
                else:
                    words += [value]
            else:
                words += [" ".join(["?" + t for t in tokens.n[i]])]
        wl[idx, "quintiles"] = " + ".join(words)
wl.output('tsv', filename=argv[1].lower()+"-quintiles", prettify=False, ignore="all")
print("[i] quintiles have been written to wordlist file.")

table = []
for nA, nB, data in confusion.edges(data=True):
    table += [[
        nA,
        nB,
        len(data["vals"]),
        " ".join([str(x[0]) for x in data["vals"]])
        ]]
table_s = tabulate(sorted(table, key=lambda x: (x[2], x[0], x[1]), reverse=True), headers=[
    "sound A", "sound B", "occurrences", "cognate sets"], tablefmt="pipe")

tmp = open("template.md")
template = tmp.read()
tmp.close()
with open(argv[1].lower()+".md", "w") as f:
    f.write(template)
    f.write("# Confused Sounds\n\n")
    f.write(table_s+"\n\n")
    f.write("# Individual Alignments with Fuzzy Reconstructions\n\n")
    for row in output:
        f.write("## COGID {0} / «{1}»\n\n".format(row[0], row[1]))
        f.write(tabulate(row[2], tablefmt="pipe", headers=[
            "language", "concept", "pos"]+["S{0}".format(i) for i in range(1, row[3]+1)])+"\n\n")
print(hits, hits/(hits+fails), fails, fails/(hits+fails), hits+fails)
