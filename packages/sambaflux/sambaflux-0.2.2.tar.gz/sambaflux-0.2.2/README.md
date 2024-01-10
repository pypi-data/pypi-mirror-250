# SAMBAflux
## Description
SAMpling Biomarker Analysis is a python package for running flux sampling on metabolic networks. Once installed, it can
be imported into new python scripts or used with scripts from the [SAMBA repository.](https://forgemia.inra.fr/metexplore/cbm/samba-project/samba)

## Visuals
[add example plots here]

## Getting started
### Requirements

- Python 3.7
- cobrapy
- A solver (GLPK, CPLEX, GUROBI)
- Access to a computer cluster or powerful computer when sampling larger models


### Installation
Install via pip:  

```bash
pip install sambaflux
```

## Usage
```
  -h, --help            show this help message and exit
  -m MODEL, --model MODEL
                        Metabolic model. Supported file formats: SBML, json, mat.
  -n NSAMPLES, --nsamples NSAMPLES
                        The number of samples
  -p PROCESSORS, --processors PROCESSORS
                        Number of processors
  -t THINNING, --thinning THINNING
                        The thinning factor of the generated sampling chain. A thinning of 10 means samples are returned every 10 steps.
  -o OUTPATH, --outpath OUTPATH
                        Outfile path (without filename)
  -k KO, --ko KO        KO file containing reactions to KO, specify nothing if you want to sample WT
  -s SEPKO, --sepko SEPKO
                        Separator for the KO file
  -r RESULTS, --results RESULTS
                        File containing reactions to output, specify nothing if you want only exchange reactions
  -q, --quiet           Use this flag to silence INFO logging.
  -d, --debug           Use this flag to turn on DEBUG logging.
  --dryrun              Use this flag to run the code without running sampling.
  --log LOG             Log file path + filename. Set to None to output to console.
  -b BIOMASS, --biomass BIOMASS
                        Number between 0 and 1, fraction of biomass to optimize
  --solver {cplex,gurobi,glpk}
                        Solver to use
  --exchangemin EXCHANGEMIN
                        The value used to set the minimum flux through exchange reactions (will be negative). Set to None if you want the default exchange reaction bounds.
  --biomassrxn BIOMASSRXN
                        A .tsv containing a Model column with the name of models and a Biomass column with the name of the corresponding biomass reaction.
  -f, --fva             Use this flag to run FVA as well as sampling.
  --onlyfva             Use this flag to run FVA instead of sampling.
```

See [here](https://forgemia.inra.fr/metexplore/cbm/samba-project/samba/-/blob/main/README.md) for set-up and usage with the project's
scripts.


## Authors
Juliette Cooke

## Acknowledgments


## License
MIT License (see LICENSE file)

## Project status
Currently active on this project. 