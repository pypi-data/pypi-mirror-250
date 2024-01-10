"""
Functions for preparing reactions in a metabolic model.
"""


def set_exchanges_rxn_bounds(model, exchange_min):
    """

    :param model:
    :param exchange_min:
    :return: model:
    """
    # Set the exchange reaction bounds
    for rxn in model.exchanges:
        rxn.lower_bound = -exchange_min
        rxn.upper_bound = 1000
    return model


def parse_rxns(filename, sep=" ", sepcol="\t"):
    if filename is None:
        return None
    with open(filename, 'r') as file:
        ids = []
        for r in file:
            row = r.strip().split(sepcol)
            if len(row) == 1:
                ids.append(row[0].strip().split(sep)[0])
            elif len(row) >= 2:
                ids.append([row[0].strip().split(sep), row[1]])
    return ids

