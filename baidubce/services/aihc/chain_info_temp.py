chain_info_temp = {
    "resourcePoolId": "cce-e0isdmib",
    "jobs": [
        {
            "name": "pretrain-qwen2-72b-ck-v1",
            "jobSpec": {
                    "command": "",
                    "image": "registry.baidubce.com/aihc-aiak/aiak-training-llm:ubuntu22.04-cu12.3-torch2.2.0-py310-bccl1.2.7.2_v2.1.1.5_release",
                    "replicas": 1,
                    "envs": []
            },
            "labels": [
                {
                    "key": "aijob.cce.baidubce.com/ai-user-id",
                    "value": "69bb4999b2044af8bbda25aec2f1e1f2"
                },
                {
                    "key": "aijob.cce.baidubce.com/ai-user-name",
                    "value": "zhangsan"
                }
            ],
            "datasources": [
                {
                    "type": "pfs",
                    "name": "pfs-oYQuh4",
                    "mountPath": "/root/pfs"
                }
            ],
            "queue": "default",
            "priority": "normal",
            "jobFramework": "PyTorchJob"
        },
        {
            "queue": "default",
            "priority": "normal",
            "jobFramework": "PyTorchJob",
            "name": "pretrain-qwen2-72b-dp-v1",
            "jobSpec": {
                    "command": "",
                    "image": "registry.baidubce.com/aihc-aiak/aiak-training-llm:ubuntu22.04-cu12.3-torch2.2.0-py310-bccl1.2.7.2_v2.1.1.5_release",
                    "replicas": 1,
                    "envs": []
            },
            "labels": [
                {
                    "key": "aijob.cce.baidubce.com/ai-user-id",
                    "value": "69bb4999b2044af8bbda25aec2f1e1f2"
                },
                {
                    "key": "aijob.cce.baidubce.com/ai-user-name",
                    "value": "zhangsan"
                }
            ],
            "datasources": [
                {
                    "type": "pfs",
                    "name": "pfs-oYQuh4",
                    "mountPath": "/root/pfs"
                }
            ]
        },
        {
            "queue": "default",
            "priority": "normal",
            "jobFramework": "PyTorchJob",
            "name": "pretrain-qwen2-72b-train-v1",
            "jobSpec": {
                    "command": "bash /workspace/AIAK-Training-LLM/examples/qwen2/pretrain/pretrain_qwen2_72b.sh",
                    "image": "registry.baidubce.com/aihc-aiak/aiak-training-llm:ubuntu22.04-cu12.3-torch2.2.0-py310-bccl1.2.7.2_v2.1.1.5_release",
                    "replicas": 4,
                    "resources": [
                        {
                            "name": "baidu.com/a800_80g_cgpu",
                            "quantity": 8
                        }
                    ],
                "enableRDMA": True,
                "envs": []
            },
            "labels": [
                {
                    "key": "aijob.cce.baidubce.com/ai-user-id",
                    "value": "69bb4999b2044af8bbda25aec2f1e1f2"
                },
                {
                    "key": "aijob.cce.baidubce.com/ai-user-name",
                    "value": "zhangsan"
                }
            ],
            "datasources": [
                {
                    "type": "pfs",
                    "name": "pfs-oYQuh4",
                    "mountPath": "/root/pfs"
                }
            ]
        }
    ]
}
