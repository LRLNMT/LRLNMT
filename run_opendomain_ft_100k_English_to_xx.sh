#!/bin/bash

# This is renamed "run_opendomain_ft_100_English_to_xx.sh" as from "run_opendomain_ft_English_to_xx.sh"


# Install libraries 

# source <<conda_path_need_to_add>>/etc/profile.d/conda.sh
# conda create -n lrl_nmt_mbart50_ft  python=3.7.11
# conda activate lrl_nmt_mbart50_ft
# echo $CONDA_PREFIX

# pip install -r requirements.txt 

declare -A language_list=( ["Afrikaans"]="af_ZA" ["French"]="fr_XX" ["Hindi"]="hi_IN" ["Kannada"]="te_IN" ["Sinhala"]="si_LK" ["Tamil"]="ta_IN"  ["Xhosa"]="xh_ZA" ["Yoruba"]="sw_KE"  ["Irish"]="fr_XX" )

# declare -A language_list=( ["Afrikaans"]="af_ZA" ["Assamese"]="bn_IN" ["French"]="fr_XX" ["Hindi"]="hi_IN" ["Kannada"]="te_IN" ["Sinhala"]="si_LK" ["Tamil"]="ta_IN"  ["Xhosa"]="xh_ZA" ["Yoruba"]="sw_KE" )


function train () {
    
    lang_tag=${language_list[$1]}
    printf "Fine-tuning for language: $1, mbart_notation: ${lang_tag}\n"
    
    train_set_path="Datasets/$1/train/cc_aligned/100k/train.json"
    printf "Train directory: ${train_set_path}\n"
    
    dev_set_path="Datasets/$1/dev/flores/dev.json"
    printf "Dev directory: ${dev_set_path}\n"
    
    test_set_path="Datasets/$1/test/flores/test.json"
    printf "Test directory: ${test_set_path}\n"
    
    model_save_path_en_to_xx="en-${lang_tag}_ccaligned_model"
    
    printf "******************** Start training en_XX to ${lang_tag} direction ********************\n"
    
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
            
    printf "******************** Finished training en_XX to ${lang_tag} direction ********************\n"
    
    printf "******************** Testing on other domain-speific test sets for en_XX to ${lang_tag} direction ********************\n"
    
    for test_file_path in Datasets/$1/test/*/test.json
    do

        printf "Reading directory: ${test_file_path}\n"
        
        IFS='/' read -ra path_array <<< "${test_file_path}"
        
        printf "******************** Start TESTING on: ${path_array[3]} domain for en_XX to ${lang_tag} direction ********************\n"
        
        dev_set_path="Datasets/$1/dev/${path_array[3]}/dev.json"
        printf "Dev directory: ${dev_set_path}\n"
    
        printf "Test directory: ${test_file_path}\n"
        
        model_test_save_path_en_to_xx="test_${path_array[3]}_en-${lang_tag}_ccaligned_model"
        
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
                
        printf "******************** Finished TESTING on: ${path_array[3]} domain for en_XX to ${lang_tag} direction ********************\n"
    done
    
    printf "******************** END of en_XX to ${lang_tag} direction ********************\n"

}


# start training

while getopts l: flag
do
    case "${flag}" in
        l) language=${OPTARG};;
    esac
done


if [ -z "$language" ]
then
      echo "Language is not provided"
      
elif [ "$language" == "*" ]
then
    echo "Language is wildcard (*), hence train all the supported languages"
    for data_file_path in Datasets/*/train/cc_aligned/100k/train.json
    do
        printf "Reading directory: ${data_file_path}\n"
        
        IFS='/' read -ra path_array <<< "${data_file_path}"
        
        train ${path_array[1]}
    
    done
    
else
    echo "Provided input language pair: $language"
    
    if [ -z ${language_list[${language}]} ]
    then 
        echo "NOT-supported input language pair: $language"
    else 
        train $language
    fi
fi
