#!/bin/bash

# Install libraries 

# source <<conda_path_need_to_add>>/etc/profile.d/conda.sh
# conda create -n lrl_nmt_mbart50_ft  python=3.7.11
# conda activate lrl_nmt_mbart50_ft
# echo $CONDA_PREFIX

# pip install -r requirements.txt 

declare -A language_list=( ["Afrikaans"]="af_ZA" ["Assamese"]="bn_IN" ["French"]="fr_XX" ["Hindi"]="hi_IN" ["Irish"]="fr_XX" ["Kannada"]="te_IN" ["Sinhala"]="si_LK" ["Tamil"]="ta_IN"  ["Xhosa"]="xh_ZA" ["Yoruba"]="sw_KE" )

declare -A domian_list=( ["bible"]=1 ["government"]=2 ["jw300"]=3 ["PrimeMinisterCorpus"]=4 ["dgt"]=4 )

function train () {
    
    lang_tag=${language_list[$1]}
    printf "Fine-tuning for language: $1, mbart_notation: ${lang_tag} in domain: $2-$3 \n"
    
    printf "******************** Start training on: $3-$2-domain for en_XX to ${lang_tag} direction ********************\n"
        
    train_set_path="Datasets/$1/train/$2/$3/train.json"
    printf "Train directory: ${train_set_path}\n"
    
    dev_set_path="Datasets/$1/dev/$2/dev.json"
    printf "Dev directory: ${dev_set_path}\n"
    
    test_set_path="Datasets/$1/test/$2/test.json"
    printf "Test directory: ${test_set_path}\n"
    
    model_save_path_en_to_xx="$2_$3_en-${lang_tag}_model"
    
    python run_translation.py \
    --model_name_or_path facebook/mbart-large-50  \
    --do_train \
    --do_eval \
    --train_file ${train_set_path} \
    --validation_file ${dev_set_path} \
    --test_file ${test_set_path} \
    --source_lang en_XX \
    --target_lang ${lang_tag} \
    --output_dir  ${model_save_path_en_to_xx} \
    --per_device_train_batch_size=10 \
    --per_device_eval_batch_size=10 \
    --overwrite_output_dir \
    --predict_with_generate \
    --forced_bos_token ${lang_tag} \
    --save_steps 50000 \
    --num_beams 10 \
    --do_predict \
    --max_source_length 200 \
    --max_target_length 200
            
    printf "******************** Finished training on: $3-$2-domain for en_XX to ${lang_tag} direction ********************\n"
    
    printf "******************** Testing with other domain-speific test sets on: $model_save_path_en_to_xx ********************\n"
    
    for test_file_path in Datasets/$1/test/*/test.json
    do

        printf "Reading directory: ${test_file_path}\n"
        
        IFS='/' read -ra test_path_array <<< "${test_file_path}"
        
        printf "******************** Start TESTING for: ${test_path_array[3]}-domain on: $model_save_path_en_to_xx ********************\n"
        
        dev_set_path="Datasets/$1/dev/${test_path_array[3]}/dev.json"
        printf "Dev directory: ${dev_set_path}\n"
    
        printf "Test directory: ${test_file_path}\n"
        
        model_test_save_path_en_to_xx="$2_$3_en-${lang_tag}_model_test_on_${test_path_array[3]}"
        
        python run_translation.py \
        --model_name_or_path ${model_save_path_en_to_xx}   \
        --do_eval \
        --validation_file ${dev_set_path} \
        --test_file ${test_file_path} \
        --source_lang en_XX \
        --target_lang ${lang_tag} \
        --output_dir  ${model_test_save_path_en_to_xx} \
        --per_device_train_batch_size=10 \
        --per_device_eval_batch_size=10 \
        --overwrite_output_dir \
        --predict_with_generate \
        --forced_bos_token ${lang_tag} \
        --save_steps 50000 \
        --num_beams 10 \
        --do_predict \
        --max_source_length 200 \
        --max_target_length 200
                
        printf "******************** Finished TESTING for: ${test_path_array[3]}-domain on: $model_save_path_en_to_xx ********************\n"
    done
    
    printf "******************** END of $3-$2-domain for en_XX to ${lang_tag} direction ********************\n"

}


# start training

while getopts l:d: flag
do
    case "${flag}" in
        l) language=${OPTARG};;
        d) domain=${OPTARG};;
    esac
done


if [ -z "$language" ] || [ -z "$domain" ] 
then
      echo "Paramter(s) Language/Domain not provided"

elif [ "$domain" == "*" ]
then 
    echo "You should pick a Domain, wildcard (*) is not supported for domain."
          
elif [ "$language" == "*" ]
then

    echo "Language is wildcard (*), hence train all the supported languages for domain: $domain"
    for data_file_path in Datasets/*/train/$domain/*/train.json
    do
        printf "Reading directory: ${data_file_path}\n"
        
        IFS='/' read -ra path_array <<< "${data_file_path}"
        
        train ${path_array[1]} $domain ${path_array[4]}
    done
    
else
    echo "Provided input language pair: $language and domain: $domain"
    
    if [ -z ${language_list[${language}]} ] ||[ -z ${domian_list[${domain}]} ]
    then 
        echo "NOT-supported input language-domain combination for language: $language and domain: $domain"
    else 
        for data_file_path in Datasets/$language/train/$domain/*/train.json
        do
            printf "Reading directory: ${data_file_path}\n"
            
            IFS='/' read -ra path_array <<< "${data_file_path}"
            
            train $language $domain ${path_array[4]}
        done
    
    fi
fi
