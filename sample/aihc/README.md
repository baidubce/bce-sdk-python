# AIHC SDK Sample Files

This directory contains sample files demonstrating the usage of various AIHC SDK modules.

## Available Sample Files

1. **[aihc_sample.py](aihc_sample.py)** - Main sample file demonstrating basic usage of all AIHC modules
2. **[aihc_job_sample.py](aihc_job_sample.py)** - Sample file for job management operations
3. **[aihc_dataset_sample.py](aihc_dataset_sample.py)** - Sample file for dataset management operations
4. **[aihc_model_sample.py](aihc_model_sample.py)** - Sample file for model management operations
5. **[aihc_service_sample.py](aihc_service_sample.py)** - Sample file for service management operations
6. **[aihc_devinstance_sample.py](aihc_devinstance_sample.py)** - Sample file for development instance management operations
7. **[aihc_resource_pool_sample.py](aihc_resource_pool_sample.py)** - Sample file for resource pool management operations

## Modules Covered

The AIHC SDK provides interfaces for the following modules:

- **Job Management** - Create, query, and manage training jobs
- **Dataset Management** - Manage datasets and their versions
- **Model Management** - Manage models and their versions
- **Service Management** - Manage online services for model deployment
- **Development Instance Management** - Manage development environments
- **Resource Pool Management** - Manage resource pools and queues

## Configuration

Before running any samples, please update the configuration in [aihc_sample_conf.py](aihc_sample_conf.py):

- Set your `AK` (Access Key) and `SK` (Secret Key)
- Verify the `HOST` endpoint is correct for your region

## Running Samples

To run any sample file:

```bash
python aihc_sample.py
# or
python -m sample.aihc.aihc_sample
```

Replace `aihc_sample.py` with the specific sample file you want to run.