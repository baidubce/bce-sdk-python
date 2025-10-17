# AIHC SDK Sample Files

This directory contains sample files demonstrating the usage of various AIHC SDK modules.

## Python Version Requirements

**Important**: AIHC SDK modules require **Python 3.5 or higher**.

- **AIHC Services**: Python 3.5+ (required)
  - Uses type annotations and typing module
  - All AIHC modules (Job, Dataset, Model, Service, DevInstance, ResourcePool)
  
- **Other BCE Services**: Python 2.7+ (compatible)
  - BOS, VPC, BCC, EIP, SCS, RDS, etc. work fine with Python 2.7

**Why Python 3.5+?**
- AIHC modules use modern Python features for better code quality and IDE support
- Type annotations provide better error detection and documentation
- Python 2.7 reached end-of-life on January 1, 2020

**Recommendation**: Use Python 3.7 or higher for the best experience.

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

### Prerequisites

1. **Python Version**: Python 3.5 or higher (Python 3.7+ recommended)
   
   Check your Python version:
   ```bash
   python --version
   # or
   python3 --version
   ```

2. **Install Dependencies**:
   ```bash
   pip install future six pycryptodome
   # or
   pip3 install future six pycryptodome
   ```

3. **Configure Credentials**: Update [aihc_sample_conf.py](aihc_sample_conf.py)

### Run Examples

To run any sample file:

```bash
# Method 1: Direct execution
python3 aihc_sample.py

# Method 2: As module
python3 -m sample.aihc.aihc_sample

# Method 3: Specific module sample
python3 -m sample.aihc.aihc_job_sample
python3 -m sample.aihc.aihc_dataset_sample
python3 -m sample.aihc.aihc_service_sample
```

Replace `aihc_sample.py` with the specific sample file you want to run.

## Python 2 Compatibility Note

If you are using Python 2.7 for other BCE services (BOS, VPC, etc.), they will continue to work normally. AIHC is an independent module and does not affect other services.

To test Python 2 compatibility on ARM64 Mac, use Docker:
```bash
# Run from project root directory
./test_py2_with_docker.sh
```

For detailed Python 2 testing instructions, see [PYTHON2_TEST_GUIDE.md](../../PYTHON2_TEST_GUIDE.md) in the project root.