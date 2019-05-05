import os
import luigi
from luigi import build
from luigi.contrib.azurebatch import AzureBatchTask
from final_project.luigi.target import SuffixPreservingLocalTarget

"""
Prerequisites: 
- Create an Azure Batch Service Account and Azure Storage Account
- Provide the secrets/credentials for Storage Account and Azure Batch Service Account in a .env file 
- Python Packages to install:
    - azure batch package: ``pip install azure-batch>=6.0.0``
    - azure blob storage: ``pip install azure-storage-blob>=1.3.1``
"""

class PrepareAzureBatchCPU(AzureBatchTask):
    """

    Luigi Task to prepare Azure batch pool for Processing video with ffmpeg on video, audio and images.
    
    :param batch_account_name (str): name of pre-created azure batch account
    :param batch_account_key (str): master key for azure batch account
    :param batch_account_url (str): batch account url
    :param storage_account_name (str): name of pre-created storage account
    :param storage_account_key (str): storage account key
    :param pool_id (str): pool id for batch job
    :param create_job_task (Bool): create only azure batch pool with False
    :param pool_node_count (str): number of nodes to create for the batch job; default is 2
    :param pool_vm_size (str): size of vm to use for the batch job
    """

    starter_task_cmds = [
        "apt-get update",
        "apt-get install python3-pip -y",
        "apt-get install -y ffmpeg",
        "ffmpeg -version",
        "python3 -m pip install torch torchvision",
    ]

    batch_account_name = luigi.Parameter(default=os.getenv("BATCH_ACCOUNT_NAME"))
    batch_account_key = luigi.Parameter(default=os.getenv("BATCH_ACCOUNT_KEY"))
    batch_account_url = luigi.Parameter(default=os.getenv("BATCH_ACCOUNT_URL"))
    storage_account_name = luigi.Parameter(default=os.getenv("STORAGE_ACCOUNT_NAME"))
    storage_account_key = luigi.Parameter(default=os.getenv("STORAGE_ACCOUNT_KEY"))
    pool_id = luigi.Parameter("AzureBatch-Pool-Id-12")
    create_job_task = luigi.BoolParameter(False)
    pool_node_count = luigi.IntParameter(default=1)
    starter_task_cmds = luigi.ListParameter(default=starter_task_cmds)
    pool_vm_size = luigi.Parameter(default="STANDARD_D2_V2")
