
#!/bin/bash

echo "INPUT_DATA: ${INPUT_DATA}"
echo "OUTPUT_PREFIX: ${OUTPUT_PREFIX}"
echo "DATASET_BOS_PATH: ${DATASET_BOS_PATH}"
echo "TOKENIZER_PATH: ${TOKENIZER_PATH}"
echo "JSON_KEYS: ${JSON_KEYS}"

# 如果INPUT_DATA文件已存在，则终止启动，打印提示信息
if [ -f "${INPUT_DATA}" ]; then
    echo "The INPUT_DATA file ${INPUT_DATA} already exists, you can use it directly. Or you can delete it and run this script again."
    exit 1
fi

# 下载测试数据集
# 检查INPUT_DATA是否存在，不存在则下载
if [ ! -f "${INPUT_DATA}" ]; then
    # 下载bcecmd程序
    wget https://doc.bce.baidu.com/bce-documentation/BOS/linux-bcecmd-0.4.5.zip
    # 解压
    unzip linux-bcecmd-0.4.5.zip
    cd linux-bcecmd-0.4.5

    echo "Start to download data..."
    ./bcecmd bos cp ${DATASET_BOS_PATH} ${INPUT_DATA} --restart --quiet --yes
fi

echo "Download data done."

MEGATRON_PATH=/workspace/AIAK-Megatron
AIAK_TRAINING_PATH=${AIAK_TRAINING_PATH:-"/workspace/AIAK-Training-LLM"}

PYTHONPATH=$MEGATRON_PATH:$AIAK_TRAINING_PATH:$PYTHONPATH \
    python ${AIAK_TRAINING_PATH}/tools/data_preprocess/preprocess_pretrain_data.py \
        --input ${INPUT_DATA} \
        --output-prefix ${OUTPUT_PREFIX} \
        --tokenizer-type HFTokenizer \
        --hf-tokenizer-path $TOKENIZER_PATH \
        --json-keys $JSON_KEYS \
        --workers 50 \
        --append-eod
echo "Data preprocess done."
