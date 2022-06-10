export http_proxy=http://10.20.47.147:3128  https_proxy=http://10.20.47.147:3128 no_proxy=code.byted.org

DATA=/mnt/bd/zhengxinvolume/AGIF/data
MODEL=/mnt/bd/zhengxinvolume/AGIF/model
RES=/mnt/bd/zhengxinvolume/AGIF/res

for TASK in MixATIS_clean_seq2seq # MixSNIPS_clean_seq2seq
do
for model_name in  google/t5-v1_1-base google/t5-v1_1-large #  google/t5-v1_1-xl # t5-small # t5-11b #t5-large # t5-small t5-base 
do
    cd /mnt/bd/zhengxinvolume/transformers/examples/pytorch/summarization
    python3 -m torch.distributed.launch --nproc_per_node=4 run_summarization.py \
        --model_name_or_path ${model_name} \
        --do_train \
        --do_eval \
        --do_predict \
        --train_file ${DATA}/${TASK}/train.json \
        --validation_file ${DATA}/${TASK}/dev.json \
        --test_file ${DATA}/${TASK}/test.json \
        --output_dir ${MODEL}/${TASK}_${model_name} \
        --overwrite_output_dir \
        --num_train_epochs 8 \
        --overwrite_cache \
        --per_device_train_batch_size=24 \
        --per_device_eval_batch_size=4 \
        --evaluation_strategy epoch \
        --predict_with_generate \
        --learning_rate 3e-5 \
        --save_strategy no \
        --warmup_steps 50 \
        --logging_steps 500 \
        --sharded_ddp simple \
        --lang 0
    rm -rf ${MODEL}/${TASK}_${model_name}/checkpoint*
    cd /mnt/bd/zhengxinvolume/AGIF
    python3 tools/eval_exact_match.py --ref_file ${DATA}/${TASK}/test.ref  --pred_file ${MODEL}/${TASK}_${model_name}/generated_predictions.txt >> ${RES}/exact_match.txt &

    cd /mnt/bd/zhengxinvolume/e2e-metrics
    ./measure_scores.py -t ${DATA}/${TASK}/test.ref ${MODEL}/${TASK}_${model_name}/generated_predictions.txt >> ${RES}/BLEU.txt &

done
done

