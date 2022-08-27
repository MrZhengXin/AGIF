
DIR=$(pwd)
DATA=$(pwd)/data
MODEL=$(pwd)/model
RES=$(pwd)/res
NUM_GPU=$(nvidia-smi --list-gpus | wc -l)
export http_proxy=http://10.20.47.147:3128  https_proxy=http://10.20.47.147:3128 no_proxy=code.byted.org
export CURL_CA_BUNDLE=""

for model_name in mt5-large mt5-xl #  google/mt5-base
do
    for TASK in 'ATIS' 'MixATIS_clean' 'MixATIS_clean_split' 'SNIPS' 'MixSNIPS' 'MixSNIPS_split'
    do
        TASK=${TASK}_t5_intent
        OUTPUT_DIR=${MODEL}/${TASK}/$(basename ${model_name})
        echo ${OUTPUT_DIR}
        CURL_CA_BUNDLE="" python3 -m torch.distributed.launch --nproc_per_node=${NUM_GPU} --master_port=12345  src/run_summarization.py \
            --model_name_or_path ${MODEL}/${model_name} \
            --do_train \
            --do_predict \
            --do_eval \
            --train_file ${DATA}/${TASK}/train.json \
            --validation_file ${DATA}/${TASK}/test.json \
            --test_file ${DATA}/${TASK}/test.json \
            --output_dir ${OUTPUT_DIR} \
            --overwrite_output_dir \
            --num_train_epochs 8 \
            --overwrite_cache \
            --per_device_train_batch_size 8 \
            --per_device_eval_batch_size 8 \
            --evaluation_strategy epoch \
            --predict_with_generate \
            --generation_num_beams 4 \
            --learning_rate 3e-5 \
            --save_strategy epoch \
            --warmup_steps 50 \
            --logging_steps 500 \
            --sharded_ddp simple \
            --load_best_model_at_end
        rm -rf ${OUTPUT_DIR}/checkpoint*


    done
done


