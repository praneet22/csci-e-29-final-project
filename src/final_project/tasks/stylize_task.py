import os
import luigi
from luigi import build
from luigi.contrib.azurebatch import AzureBatchTask


class PreProcessVideo(AzureBatchTask):
    """
    
    AzureBatchTask to split the video into frames
    
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

    input_video = "orangutan.mp4"
    output_audio = "audio"
    output_images = "images"

    command = [
        "mkdir {}".format(output_audio),
        "mkdir {}".format(output_images),
        "ffmpeg -i {} {}/audio.aac 2>&1 | tee stdout.txt".format(input_video, output_audio),
        "ffmpeg -i {} {}/%05d_video.jpg -hide_banner 2>&1 | tee stdout.txt".format(
            input_video, output_images
        ),
    ]

    batch_account_name = luigi.Parameter(os.getenv("BATCH_ACCOUNT_NAME"))
    batch_account_key = luigi.Parameter(os.getenv("BATCH_ACCOUNT_KEY"))
    batch_account_url = luigi.Parameter(os.getenv("BATCH_ACCOUNT_URL"))
    storage_account_name = luigi.Parameter(os.getenv("STORAGE_ACCOUNT_NAME"))
    storage_account_key = luigi.Parameter(os.getenv("STORAGE_ACCOUNT_KEY"))
    data_input_path = luigi.Parameter("data/video/")
    command = luigi.ListParameter(command)
    pool_node_count = luigi.IntParameter(1)
    output_path = luigi.Parameter(default=" ")
    pool_id = luigi.Parameter("AzureBatch-Pool-Id-12")
    #job_id = luigi.Parameter("AzureBatch-Job-Id-12")



if __name__ == "__main__":

    build([PreProcessVideo()], local_scheduler=True)

