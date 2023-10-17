from lingpy import *
from tabulate import tabulate
import statistics

data = ["Karen", "Burmish", "Panoan"]
table = []
for datum in data:
    
    correct_p = []
    certain_p = []
    correct_alm, false_alm = [], []
    certain_alm, uncertain_alm = [], []

    alms = Alignments(
            datum.lower()+"-quintiles.tsv",
            ref="cogids",
            transcription="form")
    for idx, doculect, tokens, quintiles, cogids in alms.iter_rows(
            "doculect", "tokens", "quintiles", "cogids"):
        # iterate over morphemes
        if doculect == "Proto" + datum:
            quintiles = basictypes.lists(quintiles)
            for segment, quintile, cogid in zip(tokens.n, quintiles.n, cogids):
                # alignment size, check if alignment was carried out
                # check for length of taxa
                if cogid in alms.msa["cogids"] and len(set(alms.msa["cogids"][cogid]["taxa"])) > 2:
                    alm_len = len(alms.msa["cogids"][cogid]["alignment"][0])
                    if quintile[0] == "(":
                        correct_p += [1]
                        certain_p += [1]
                        correct_alm += [alm_len]
                        certain_alm += [alm_len]
                    else:
                        correct_p += [0]
                        false_alm += [alm_len]
                        # uncertainty check
                        if sum([len(set(t.split("|"))) for t in quintile]) == len(quintile):
                            certain_p += [1]
                            certain_alm += [alm_len]
                        else:
                            certain_p += [0]
                            uncertain_alm += [alm_len]
    table += [[
        datum, "correct", 
        sum(correct_p), 
        "{0:.2f}".format(sum(correct_p) / len(correct_p)), 
        "{0:.2f}".format(statistics.mean(correct_alm))
        ]]
    table += [[
        datum, "false", 
        correct_p.count(0), 
        "{0:.2f}".format(correct_p.count(0) / len(correct_p)), 
        "{0:.2f}".format(statistics.mean(false_alm))
        ]]
    table += [[datum, "certain", 
        sum(certain_p), 
        "{0:.2f}".format(sum(certain_p) / len(certain_p)), 
        "{0:.2f}".format(statistics.mean(certain_alm))]]
    table += [[datum, "uncertain", certain_p.count(0), 
        "{0:.2f}".format(certain_p.count(0) / len(certain_p)), 
        "{0:.2f}".format(statistics.mean(uncertain_alm))]]


print(tabulate(table, 
    tablefmt="pipe",
    #float_fmt=".2f",
    headers=["Dataset", "Prediction", "Count", "Proportion", "Alignment Size"]))
