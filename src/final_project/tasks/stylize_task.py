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

    mnt = "/mnt/MyAzureFileShare"
    input_video = "orangutan.mp4"
    output_audio = "{}/audio".format(mnt)
    output_images = "{}/images".format(mnt)

    command = [
        "mkdir {}".format(output_audio),
        "mkdir {}".format(output_images),
        "ffmpeg -i {} {}/audio.aac 2>&1 | tee stdout.txt".format(
            input_video, output_audio
        ),
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
    pool_id = luigi.Parameter("AzureBatch-Pool-Id-15")


class StyleImages(AzureBatchTask):
    """ Luigi Task to Stylize Images on Azure Batch
    :param (str): path to the local directory to save the downloaded video to
    :param (str): path to the remote video to be downloaded
    :param (str): output video name to save the downloaded video as

    :return target output
    :rtype: object (:py:class:`pset_4.luigi.target.SuffixPreservingLocalTarget`)
    """

    mnt = "/mnt/MyAzureFileShare"
    styled_image_output = "{}/styled_output".format(mnt)
    image_input_path = "{}/images".format(mnt)

    command = [
        "tar -xvzf artifacts.tar.gz",
        """python3 artifacts/style_transfer.py \
    --model-dir artifacts \
    --cuda 0 \
    --content-dir {} \
    --output-dir {}""".format(
            image_input_path, styled_image_output
        ),
    ]
    batch_account_name = luigi.Parameter(os.getenv("BATCH_ACCOUNT_NAME"))
    batch_account_key = luigi.Parameter(os.getenv("BATCH_ACCOUNT_KEY"))
    batch_account_url = luigi.Parameter(os.getenv("BATCH_ACCOUNT_URL"))
    storage_account_name = luigi.Parameter(os.getenv("STORAGE_ACCOUNT_NAME"))
    storage_account_key = luigi.Parameter(os.getenv("STORAGE_ACCOUNT_KEY"))
    # script_input_path = luigi.Parameter(default="src/final_project/styletransfer/")
    pool_id = luigi.Parameter("AzureBatch-Pool-Id-17")
    data_input_path = luigi.Parameter(default="src/final_project/models/artifacts/")

class PostProcessVideo(AzureBatchTask):
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

    mnt = "/mnt/MyAzureFileShare"
    output_vid_dir = "{}/styled_vid".format(mnt)
    audio = "{}/audio".format(mnt)
    styled_output = "{}/styled_output".format(mnt)
    styled_video = "styled_orangutan"

    command = [
        "mkdir {}".format(output_vid_dir),
        "ffmpeg -framerate 30 -i {}/%05d_video.jpg -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p -y {}/video_without_audio.mp4 2>&1 | tee stdout.txt".format(
            styled_output, output_vid_dir
        ),
        "ffmpeg -i {}/video_without_audio.mp4 -i {}/audio.aac -map 0:0 -map 1:0 -vcodec copy -acodec copy -y {}/{}_processed.mp4 2>&1 | tee stdout.txt".format(
            output_vid_dir, audio, output_vid_dir, styled_video
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
    pool_id = luigi.Parameter("AzureBatch-Pool-Id-15")


if __name__ == "__main__":

    build([PreProcessVideo()], local_scheduler=True)
>>>>>>> 7900c6103fc7e4659ea9c2efe239f6f6b391ed01
