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
    
    :param azure_files_path (str): file blob path to mount on azure batch
    :param batch_mnt_path (str): location on azure batch nodes to mount file blob
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

    azure_files_path = luigi.Parameter(
        default="//prsolblobstorage.file.core.windows.net/azurebatchdata"
    )
    batch_mnt_path = luigi.Parameter(default="/mnt/MyAzureFileShare/")
    batch_account_name = luigi.Parameter(default=os.getenv("BATCH_ACCOUNT_NAME"))
    batch_account_key = luigi.Parameter(default=os.getenv("BATCH_ACCOUNT_KEY"))
    batch_account_url = luigi.Parameter(default=os.getenv("BATCH_ACCOUNT_URL"))
    storage_account_name = luigi.Parameter(default=os.getenv("STORAGE_ACCOUNT_NAME"))
    storage_account_key = luigi.Parameter(default=os.getenv("STORAGE_ACCOUNT_KEY"))
    pool_node_count = luigi.IntParameter(default=1)
    pool_id = luigi.Parameter("AzureBatch-Pool-Id-18")
    pool_vm_size = luigi.Parameter(default="STANDARD_D2_V2")

    # build up list of commands to run during node setup
    starter_task_cmds = [
        "apt-get update",
        "apt-get install cifs-utils",
        "mkdir -p {}".format(batch_mnt_path),
        "mount -t cifs {} {} -o vers=3.0,username={},password={},dir_mode=0777,file_mode=0777,serverino".format(
            azure_files_path,
            batch_mnt_path,
            os.getenv("STORAGE_ACCOUNT_NAME"),
            os.getenv("STORAGE_ACCOUNT_KEY"),
        ),
        "apt-get install python3-pip -y",
        "apt-get install -y ffmpeg",
        "ffmpeg -version",
        "python3 -m pip install torch torchvision Pillow",
    ]
    starter_task_cmds = luigi.ListParameter(default=starter_task_cmds)


class PrepareAzureBatchGPU(AzureBatchTask):
    """
    Luigi Task to prepare Azure batch pool for applying style transfer on images from video
    
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
        "apt-get install cuda",
        "nvcc --version",
        "python3 -m pip install torch torchvision Pillow",
    ]

    batch_account_name = luigi.Parameter(default=os.getenv("BATCH_ACCOUNT_NAME"))
    batch_account_key = luigi.Parameter(default=os.getenv("BATCH_ACCOUNT_KEY"))
    batch_account_url = luigi.Parameter(default=os.getenv("BATCH_ACCOUNT_URL"))
    storage_account_name = luigi.Parameter(default=os.getenv("STORAGE_ACCOUNT_NAME"))
    storage_account_key = luigi.Parameter(default=os.getenv("STORAGE_ACCOUNT_KEY"))
    pool_node_count = luigi.IntParameter(default=1)
    starter_task_cmds = luigi.ListParameter(default=starter_task_cmds)
    pool_id = luigi.Parameter(default="AzureBatch-Pool-GPU")
    pool_vm_size = luigi.Parameter(default="Standard_NC6")
    node_agent_sku_id = luigi.Parameter(default="batch.node.ubuntu 16.04")
