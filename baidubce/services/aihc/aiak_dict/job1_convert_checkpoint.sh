#! /bin/bash

echo "LOAD: ${LOAD}"
echo "SAVE: ${SAVE}"
echo "MODEL_BOS_PATH: ${MODEL_BOS_PATH}"
echo "MODEL_NAME: ${MODEL_NAME}"
echo "TP: ${TP}"
echo "PP: ${PP}"

# 如果SAVE文件夹已存在，则终止启动，打印提示信息
if [ -d "${SAVE}" ]; then
    echo "The SAVE folder ${SAVE} already exists, you can use it directly. Or you can delete it and run this script again."
    exit 1
else
    echo "The SAVE folder ${SAVE} does not exist, start to convert checkpoint."
fi

# 检查/mnt/cluster/huggingface.co/meta-llama/Llama-2-70b-hf是否存在，不存在则下载
if [ ! -d "${LOAD}" ]; then
    # 下载bcecmd程序
    wget https://doc.bce.baidu.com/bce-documentation/BOS/linux-bcecmd-0.4.5.zip
    # 解压
    unzip linux-bcecmd-0.4.5.zip
    cd linux-bcecmd-0.4.5
    echo "Start to download checkpoint..."
    ./bcecmd  bos sync ${MODEL_BOS_PATH} ${LOAD}
    echo "Download checkpoint done."
else
    echo "The LOAD folder ${LOAD} already exists,no need to download."
fi

echo "Start to convert checkpoint..."

AIAK_TRAINING_PATH=/workspace/AIAK-Training-LLM
CONVERT_CHECKPOINT_PATH="$AIAK_TRAINING_PATH/tools/convert_checkpoint"
MEGATRON_PATH=${MEGATRON_PATH:-"/workspace/AIAK-Megatron"}

# 当前不支持 optim 部分转换，通过 --no_save_optim 和 --no_load_optim 关闭；
python $CONVERT_CHECKPOINT_PATH/model.py \
    --load_platform=huggingface \
    --save_platform=mcore \
    --common_config_path=$CONVERT_CHECKPOINT_PATH/config/${MODEL_NAME}.json \
    --tensor_model_parallel_size=${TP} \
    --pipeline_model_parallel_size=${PP} \
    --load_ckpt_path=$LOAD \
    --save_ckpt_path=$SAVE \
    --megatron_path=$MEGATRON_PATH \
    --no_save_optim \
    --no_load_optim \
    --safetensors

echo "Convert checkpoint done."
echo "The converted checkpoint is saved in: \n ${SAVE}."
