CUDA_VISIBLE_DEVICES=0 torchrun --nproc_per_node 1 finetune.py \
    --model_name_or_path /data/yuanql/model/modelscope/AI-ModelScope/chinese-llama-2-1.3b \
    --tokenizer_name /data/yuanql/model/modelscope/AI-ModelScope/chinese-llama-2-1.3b \
    --use_slow_tokenizer \
    --train_file /data/result/selfrag/generator/data/full_output_1005.jsonl \
    --max_seq_length 2048 \
    --preprocessing_num_workers 16 \
    --per_device_train_batch_size 1 \
    --gradient_accumulation_steps 8 \
    --learning_rate 2e-5 \
    --lr_scheduler_type linear \
    --warmup_ratio 0.03 \
    --weight_decay 0. \
    --num_train_epochs 1 \
    --output_dir /data/result/selfrag/generator/0304/self_rag_1.3b/ \
    --with_tracking \
    --report_to tensorboard \
    --logging_steps 1 \
    --use_special_tokens