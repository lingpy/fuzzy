from lingpy import Alignments
from lingpy.read.qlc import reduce_alignment
from lingpy.sequence.sound_classes import tokens2class
from lingrex.util import prep_wordlist
from lingreg.checks import clean_slash


def run(wordlist):
    wordlist = prep_wordlist(wordlist)
    alms = Alignments(wordlist, ref="cogid", transcription="tokens")

    dct = {}
    for _, msa in alms.msa["cogid"].items():
        msa_reduced = []
        for site in msa["alignment"]:
            reduced = reduce_alignment([site])[0]
            reduced = clean_slash(reduced)
            msa_reduced.append(reduced)
        for i, row in enumerate(msa_reduced):
            dct[msa["ID"][i]] = row

    alms.add_entries("tokens", dct, lambda x: " ".join([y for y in x if y != "-"]), override=True)
    alms.add_entries("alignment", dct, lambda x: " ".join([y for y in x]), override=True)
    alms.add_entries("structure", "tokens", lambda x: tokens2class(x.split(" "), "cv"))

    return alms
