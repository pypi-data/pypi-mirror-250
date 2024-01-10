"""Functions for exporting and writing files."""
import os
from ..setup.prepare_reactions import parse_rxns
import time


def write_sampling(s_results, out_path, model_name, n_samples, type, fname):
    final_path = str(out_path) + str(fname) + "_" + str(os.path.basename(os.path.splitext(model_name)[0])) + "_sampling_" + str(
                n_samples) + "_" + type + ".csv.gz"
    s_results.to_csv(final_path, index=False, compression='gzip')
    print("Wrote to "+final_path)


def write_fva(fva_results, out_path, model_name, n_samples, type, fname):
    final_path = str(out_path) + str(fname) + "_" + str(os.path.basename(os.path.splitext(model_name)[0])) + "_FVA_" + str(
                n_samples) + "_" + type + ".csv.gz"
    fva_results.to_csv(final_path, index=True, compression='gzip')
    print("Wrote to "+final_path)


def extract_results(s, results, model):
    # Extract from results
    col_names_start = time.time()
    if results == "exchanges":
        if model.exchanges is not None:
            results_columns = [rxn.id for rxn in model.exchanges]
        else:
            results_columns = [col for col in s if col.startswith('EX_')]
    elif results == "all":
        results_columns = [rxn.id for rxn in model.reactions]
    else:  # File containing reaction IDs
        results_columns = parse_rxns(results)
    print("Column names extraction time: " + str(time.time() - col_names_start))
    s_results_round_start = time.time()
    s_results = s[results_columns].round(3)
    print("s_results round time: " + str(time.time() - s_results_round_start))
    return s_results


def extract_fva_results(s, results, model):
    # Extract from results
    if results == "exchanges":
        if model.exchanges is not None:
            results_rows = [rxn.id for rxn in model.exchanges]
        else:
            results_rows = [col for col in s if col.startswith('EX_')]
    elif results == "all":
        results_rows = [rxn.id for rxn in model.reactions]
    else:
        results_rows = parse_rxns(results)
    s_results = s.loc[results_rows]
    return s_results


def export_metab_dict(model, max_name_length=30, use_id=False):
    # Create a metabolite exchange reaction ID to name dict for plotting in R
    metab_dict = {}
    # ex_rxn = model.exchanges.EX_A
    for ex_rxn in model.exchanges:
        name = next(iter(ex_rxn.metabolites)).name
        if len(name) < max_name_length:
            if name != "":
                metab_dict[ex_rxn.id] = name
            else:
                metab_dict[ex_rxn.id] = next(iter(ex_rxn.metabolites)).id
        else:
            if use_id:
                if next(iter(ex_rxn.metabolites)).name.endswith("(e)"):
                    metab_dict[ex_rxn.id] = next(iter(ex_rxn.metabolites)).id[:-3]
                else:
                    metab_dict[ex_rxn.id] = next(iter(ex_rxn.metabolites)).id
            else:
                if name != "":
                    metab_dict[ex_rxn.id] = name[:max_name_length]
                else:
                    metab_dict[ex_rxn.id] = next(iter(ex_rxn.metabolites)).id
    return metab_dict


def export_metab_id_dict(model):
    # Create an exchange reaction ID to metabolite ID dict
    metab_id_dict = {}
    # ex_rxn = model.exchanges.EX_A
    for ex_rxn in model.exchanges:
        metab_id_dict[ex_rxn.id] = next(iter(ex_rxn.metabolites)).id
    return metab_id_dict


def export_gene_to_rxn_dict(model, ids_to_ko):
    # Create a gene to rxn ID using GPRs
    gene_to_rxn_dict = {}
    for gene in ids_to_ko:
        # gene is a list of 1 item for compatibility with using multiple reaction names in one row/group
        rxns = [rxn.id for rxn in model.genes.get_by_id(gene[0]).reactions]
        gene_to_rxn_dict[gene[0]] = " ".join(rxns)
    return gene_to_rxn_dict
