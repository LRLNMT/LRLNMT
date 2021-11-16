# Transformers for MT

- Copy `Datasets` folders to `transformers/experiments` folder and rename it to `dataset`
- Run the code `create_dataset.py`
- Run `run.sh lang_name dataset_name size reverse` to run a experiment or rcopy multiple such experiments to run_multi.sh and run that


## Running
- `run.sh` takes four arguments, first language code (en, ta, etc) , dataset name (bible, PrimeMinisterCorpus etc), size (1k, 10k, 100k etc as written here and not 1000 etc), reverse (0, 1). If the value of reverse is 0 then en-xx is run and if it is 1 xx-en is run
