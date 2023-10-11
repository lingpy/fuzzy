import re
from lingpy import Alignments
from lingpy.read.qlc import reduce_alignment
from lingpy.sequence.sound_classes import tokens2class


def clean_slash(x):
    cleaned = []
    for segment in x:
        if "/" in segment:
            after_slash = re.split("/", segment)[1]
            cleaned.append(after_slash)
        else:
            cleaned.append(segment)

    return cleaned


def run(wordlist):

    whitelist = []
    for _, idxs in wordlist.get_etymdict(ref="cogid").items():
        visited, all_indices = set(), []
        for idx in map(lambda x: x[0], filter(lambda x: x, idxs)):
            if wordlist[idx, "doculect"] not in visited:
                visited.add(wordlist[idx, "doculect"])
                all_indices += [idx]
        if len(visited) >= 3:
            whitelist += all_indices
    for idx, tokens in wordlist.iter_rows("tokens"):
        wordlist[idx, "tokens"] = [t for t in tokens if t not in ["_+"]]

    D = {0: wordlist.columns}
    for idx in whitelist:
        D[idx] = wordlist[idx]

    alms = Alignments(D, ref="cogid", transcription="tokens")
    dct = {}

    for cogid, msa in alms.msa["cogid"].items():
        msa_reduced = []
        for site in msa["alignment"]:
            reduced = reduce_alignment([site])[0]
            reduced = clean_slash(reduced)
            msa_reduced.append(reduced)
            if cogid == 242:
                print(site)
                print(reduced)
                print("---")
        for i, row in enumerate(msa_reduced):
            dct[msa["ID"][i]] = row

    alms.add_entries("tokens", dct, lambda x: " ".join([y for y in x if y != "-"]), override=True)
    alms.add_entries("alignment", dct, lambda x: " ".join([y for y in x]), override=True)
    alms.add_entries("structure", "tokens", lambda x: tokens2class(x.split(" "), "cv"))

    for item in alms:
        if alms[item, "cogid"] == 242:
            print(alms[item, "alignment"])
    return alms
