
#!/bin/bash

# 检查INPUT_DATA是否存在，不存在则下载
if [ ! -d "${INPUT_DATA}" ]; then
    # 下载bcecmd程序
    wget https://doc.bce.baidu.com/bce-documentation/BOS/linux-bcecmd-0.4.5.zip
    # 解压
    unzip linux-bcecmd-0.4.5.zip
    cd linux-bcecmd-0.4.5

    echo "Start to download data..."
    # 下载测试数据集
    ./bcecmd bos cp ${DATASET_BOS_PATH} ${INPUT_DATA} --restart --quiet --yes
fi

echo "Download data done."

MEGATRON_PATH=/workspace/AIAK-Megatron
AIAK_TRAINING_PATH=${AIAK_TRAINING_PATH:-"/workspace/AIAK-Training-LLM"}

PYTHONPATH=$MEGATRON_PATH:$AIAK_TRAINING_PATH:$PYTHONPATH \
    python ${AIAK_TRAINING_PATH}/tools/data_preprocess/preprocess_sft_data.py \
        --input ${INPUT_DATA} \
        --output ${OUTPUT_PATH} \
        --seq-length 2048 \
        --chat-template ${CHAT_TEMPLATE} \
        --tokenizer-type HFTokenizer \
        --hf-tokenizer-path $TOKENIZER_PATH \
        --workers 50 \
        --split 100,0,0
        # --packing-sft-data \
        # --train-on-prompt \
        # --eod-mask-loss \
        # --sft-dataset-config /workspace/AIAK-Training-LLM/configs/sft_dataset_config.json \
        # --sft-dataset custom_dataset \
echo "Data preprocess done."
