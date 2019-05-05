import os
import wget, requests
from pathlib import Path
from luigi import ExternalTask, Parameter, Task, LocalTarget
from luigi.contrib.azureblob import AzureBlobClient, AzureBlobTarget
from luigi.contrib.external_program import ExternalProgramTask
from luigi.format import Nop

from ..luigi.target import SuffixPreservingLocalTarget


class DownloadVideo(ExternalProgramTask):
    LOCAL_VIDEO_ROOT = Path("data", "video").as_posix()
    REMOTE_VIDEO_PATH = "https://happypathspublic.blob.core.windows.net/videos"
    video = "orangutan.mp4"

    def program_args(self):
        return ["wget", Path(self.REMOTE_VIDEO_PATH, self.video).as_posix()]

    def output(self):
        return SuffixPreservingLocalTarget(
            Path(self.LOCAL_VIDEO_ROOT, self.video).as_posix()
        )


class VideoRequest(ExternalTask):
    def output(self):
        return requests.get(
            "https://happypathspublic.blob.core.windows.net/videos/orangutan.mp4"
        ).content


class DownloadVideoWget(Task):
    LOCAL_VIDEO_ROOT = Path("data", "video").as_posix()
    REMOTE_VIDEO_PATH = "https://happypathspublic.blob.core.windows.net/videos"
    video = "orangutan.mp4"

    # def requires(self):
    #     return VideoRequest()

    def run(self):
        # wget.download("https://happypathspublic.blob.core.windows.net/videos/orangutan.mp4", self.output().path)
        # requests.get("https://happypathspublic.blob.core.windows.net/videos/orangutan.mp4")

        # with self.input().open("r") as infile:
        #     tmp_video = infile.read()
        with self.output().open("w") as outfile:
            outfile.write(wget.download("https://happypathspublic.blob.core.windows.net/videos/orangutan.mp4"))

    def output(self):
        return LocalTarget(os.path.join(self.LOCAL_VIDEO_ROOT, self.video))


class ContentVideo(ExternalTask):
    """
    Task to copy the video file from Azure Blob

    :param container (str): name of the azure bl
    :param blob (str): name of video to download from blob storage
    :param storage_account_name (str): name of pre-created storage account
    :param storage_account_key (str): storage account key
    """

    storage_account_name = Parameter(default=os.getenv("STORAGE_ACCOUNT_NAME"))
    storage_account_key = Parameter(default=os.getenv("STORAGE_ACCOUNT_KEY"))
    sas_token = Parameter(default=os.getenv("SAS_TOKEN"))
    container = Parameter(default="video")
    blob = Parameter(default="orangutan.mp4")
    is_emulated = False if storage_account_name else True
    kwargs = dict(protocol="https", is_emulated=is_emulated)
    client = AzureBlobClient(
        storage_account_name, storage_account_key, sas_token, **kwargs
    )
    print("Have Client: ", client)

    def output(self):
        """ 
        Return the AzureBlobTarget of the video for this external task.
        Expects the video to be available on Azure Blob Storage

        :return target output
        :rtype: object (:py:class: `luigi.target.AzureBlobTarget`)
        """
        # is_emulated = False if self.storage_account_name else True
        # kwargs = dict(protocol="https", is_emulated=is_emulated)
        # client = AzureBlobClient(
        #     self.storage_account_name,
        #     self.storage_account_key,
        #     self.sas_token,
        #     **kwargs
        # )
        return AzureBlobTarget(self.container, self.blob, self.client, format=Nop)

    # def output(self):
    #     is_emulated = False if self.storage_account_name else True
    #     kwargs = dict(protocol="https", is_emulated=is_emulated)
    #     client = AzureBlobClient(
    #         self.storage_account_name,
    #         self.storage_account_key,
    #         self.sas_token,
    #         **kwargs
    #     )
    #     return AzureBlobTarget("luigi-test", "movie-cheesy.txt", client, download_when_reading=False)

    def run(self):
        is_emulated = False if self.storage_account_name else True
        self.client.connection.create_container("luigi-test")
        with self.output().open("w") as op:
            op.write("I'm going to make him an offer he can't refuse.\n")
            op.write("Toto, I've got a feeling we're not in Kansas anymore.\n")
            op.write("May the Force be with you.\n")
            op.write("Bond. James Bond.\n")
            op.write("Greed, for lack of a better word, is good.\n")


class CopyAzureBlobVideoLocally(ExternalTask):
    """ Copies the video from Azure Blob to local target while preserving the video file suffix """

    LOCAL_VIDEO_ROOT = os.path.join("data", "video")
    storage_account_name = Parameter(default=os.getenv("STORAGE_ACCOUNT_NAME"))
    storage_account_key = Parameter(default=os.getenv("STORAGE_ACCOUNT_KEY"))
    container = Parameter(default="video")
    video = Parameter(default="orangutan.mp4")

    def requires(self):
        # Depends on ContentVideo External Task to run successfully
        return ContentVideo(
            self.storage_account_name,
            self.storage_account_key,
            self.container,
            self.video,
        )

    def output(self):
        return SuffixPreservingLocalTarget(
            os.path.join(self.LOCAL_VIDEO_ROOT, self.video)
        )

    def run(self):
        with self.input().open("r") as infile:
            tmp_video = infile.read()
        with self.output().open("w") as outfile:
            outfile.write(tmp_video)

