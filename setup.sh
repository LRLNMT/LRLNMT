conda create -n lrl_nmt_mbart50_ft  python=3.7.11

conda activate lrl_nmt_mbart50_ft
echo $CONDA_PREFIX

pip install -r requirements.txt 

# python run_translation.py \
#     --model_name_or_path facebook/mbart-large-50  \
#     --do_train \
#     --do_eval \
#     --train_file data/sien_govUOM_10000_train.json \
#     --validation_file data/wikipedia.dev.si-en_devset.json \
#     --test_file data/wikipedia.test.si-en_testset.json \
#     --source_lang en_XX \
#     --target_lang si_LK \
#     --output_dir mbart50_ft_ensi_govuom_10k \
#     --per_device_train_batch_size=10 \
#     --per_device_eval_batch_size=10 \
#     --overwrite_output_dir \
#     --predict_with_generate \
#     --save_steps 50000 \
#     --num_beams 10 \
#     --do_predict \
#     --max_source_length 200 \
#     --max_target_length 200 
    
    # --max_target_length 1024 / 500 / 200 / default=128 
