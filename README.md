
# Sequence-to-Sequence Multilingual Pre-Trained Models: A Hope for Low-Resource Language Translation?

## Enviroment Setup

    source <<conda_path_need_to_add>>/etc/profile.d/conda.sh
    conda create -n lrl_nmt_mbart50_ft  python=3.7.11
    conda activate lrl_nmt_mbart50_ft
    echo $CONDA_PREFIX
    
    pip install -r requirements.txt 


## 1. Open-Domain Training/Fine-tuning on cc_aligned

### 1.a. 100k cc_aligned English &#8594; XX

    bash run_opendomain_ft_100k_English_to_xx.sh -l "<<language_name>>" > logs_run_opendomain_ft_100k_English_to_xx

Language (-l) parameter value can be: 
- `Afrikaans`
- `French`
- `Hindi`
- `Kannada`
- `Sinhala`
- `Tamil`
- `Xhosa`
- `Yoruba`
- `Irish`

if you wish to train all (8 languages) suppported language pairs, pass wildcard syombol as -l "*": 

    bash run_opendomain_ft_100k_English_to_xx.sh -l "*" > logs_run_opendomain_ft_100k_English_to_xx



### 1.b. 100k cc_aligned XX &#8594; English


    bash run_opendomain_ft_100k_xx-to-English.sh -l "<<language_name>>" > logs_run_opendomain_ft_100k_xx-to-English

Language (-l) parameter value can be: 
- `Afrikaans`
- `French`
- `Hindi`
- `Kannada`
- `Sinhala`
- `Tamil`
- `Xhosa`
- `Yoruba`
- `Irish`

if you wish to train all (8 languages) suppported language pairs, pass wildcard syombol as -l "*": 

    bash run_opendomain_ft_100k_xx-to-English.sh -l "*" > logs_run_opendomain_ft_100k_xx-to-English




### 1.c. 25k cc_aligned English &#8594; XX

    bash run_opendomain_ft_25k_English_to_xx.sh -l "<<language_name>>" > logs_run_opendomain_ft_25k_English_to_xx

Language (-l) parameter value can be: 
- `Afrikaans`
- `Assamese`
- `French`
- `Hindi`
- `Kannada`
- `Sinhala`
- `Tamil`
- `Xhosa`
- `Yoruba`
- `Irish`

if you wish to train all (9 languages) suppported language pairs, pass wildcard syombol as -l "*": 

    bash run_opendomain_ft_25k_English_to_xx.sh -l "*" > logs_run_opendomain_ft_25k_English_to_xx



### 1.d. 25k cc_aligned XX &#8594; English

    bash run_opendomain_ft_25k_xx-to-English.sh -l "<<language_name>>" > logs_run_opendomain_ft_25k_xx-to-English

Language (-l) parameter value can be: 
- `Afrikaans`
- `Assamese`
- `French`
- `Hindi`
- `Kannada`
- `Sinhala`
- `Tamil`
- `Xhosa`
- `Yoruba`
- `Irish`

if you wish to train all (9 languages) suppported language pairs, pass wildcard syombol as -l "*": 

    bash run_opendomain_ft_25k_xx-to-English.sh -l "*" > logs_run_opendomain_ft_25k_xx-to-English



## 2. Domain specific Training/Fine-tuning. 

### 2.a. English &#8594; XX

    bash domain-specific_ft_English_to_xx.sh -l "<<language_name>>" -d "<<domain>>"   > logs_run_domain-specific-English-to-xx

Possible combination of domain (-d) and language (-l) parameter values can be: 

| Domain (-d)  | languages (-l) |
| ------------- | ------------- |
| bible  | Afrikaans, Assamese, French, Hindi, Irish, Kannada, Sinhala, Tamil, Xhosa, Yoruba  |
| jw300  | Afrikaans, Xhosa, Yoruba  |
| government  | Sinhala, Tamil  |
| PrimeMinisterCorpus  | Assamese, Hindi, Kannada  |
| dgt  | French, Irish   |


if you wish to train all suppported language pairs for each domains: 

    bash domain-specific_ft_English_to_xx.sh -l "*" -d "bible" > logs_bible_en-xx

    bash domain-specific_ft_English_to_xx.sh -l "*" -d "jw300" > logs_jw300_en-xx
    
    bash domain-specific_ft_English_to_xx.sh -l "*" -d "government" > logs_gov_en-xx
    
    bash domain-specific_ft_English_to_xx.sh -l "*" -d "PrimeMinisterCorpus" > logs_pmc_en-xx
    
    bash domain-specific_ft_English_to_xx.sh -l "*" -d "dgt" > logs_dgt_en-xx

Please note wildcard (*) is only supported for (-l) languges not for (-d) domain, you must select a (-d) domain.


### 2.a. XX &#8594; English 

    bash domain-specific_ft_xx_to_English.sh -l "<<language_name>>" -d "<<domain>>"   > logs_run_domain-specific-xx-to-English

Possible combination of domain (-d) and language (-l) parameter values can be: 

| Domain (-d)  | languages (-l) |
| ------------- | ------------- |
| bible  | Afrikaans, Assamese, French, Hindi, Irish, Kannada, Sinhala, Tamil, Xhosa, Yoruba  |
| jw300  | Afrikaans, Xhosa, Yoruba  |
| government  | Sinhala, Tamil  |
| PrimeMinisterCorpus  | Assamese, Hindi, Kannada  |
| dgt  | French, Irish   |


if you wish to train all suppported language pairs for each domains: 

    bash domain-specific_ft_xx_to_English.sh -l "*" -d "bible" > logs_bible_xx-en

    bash domain-specific_ft_xx_to_English.sh -l "*" -d "jw300" > logs_jw300_xx-en
    
    bash domain-specific_ft_xx_to_English.sh -l "*" -d "government" > logs_gov_xx-en
    
    bash domain-specific_ft_xx_to_English.sh -l "*" -d "PrimeMinisterCorpus" > logs_pmc_xx-en
    
    bash domain-specific_ft_xx_to_English.sh -l "*" -d "dgt" > logs_dgt_xx-en

Please note wildcard (*) is only supported for (-l) languges not for (-d) domain, you must select a (-d) domain.



