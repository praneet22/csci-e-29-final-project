import os
import wget
import shutil
from pathlib import Path
from luigi.format import Nop
from luigi import ExternalTask, Parameter, Task
from final_project.tasks.prepare_batch import PrepareAzureBatchCPU
from final_project.luigi.target import SuffixPreservingLocalTarget


class DownloadVideo(Task):
    """ Luigi Task to Download Video from a public url using python wget module
    :param (str): path to the local directory to save the downloaded video to
    :param (str): path to the remote video to be downloaded
    :param (str): output video name to save the downloaded video as

    :return target output
    :rtype: object (:py:class:`pset_4.luigi.target.SuffixPreservingLocalTarget`)
    """

    LOCAL_VIDEO_ROOT = Parameter(default=Path("data", "video").as_posix())
    REMOTE_VIDEO_PATH = Parameter(
        default="https://happypathspublic.blob.core.windows.net/videos/orangutan.mp4"
    )
    output_video_name = Parameter(default="orangutan.mp4")
    pool_id = Parameter()
    path = os.path.join("data", "luigioutputs")

    def requires(self):
        return PrepareAzureBatchCPU(pool_id=self.pool_id)

    def output(self):
        return SuffixPreservingLocalTarget(
            os.path.join(self.LOCAL_VIDEO_ROOT, self.output_video_name), format=Nop
        )

    def run(self):
        # wget.download uses cwd if no path is given and will not accept self.output().path
        # cleanup resource afterwards using a dependent task
        if not os.path.exists(self.LOCAL_VIDEO_ROOT):
            print("Creating out video Directory: {}".format(self.LOCAL_VIDEO_ROOT))
            try:
                os.makedirs(self.LOCAL_VIDEO_ROOT)
            except FileExistsError:
                # directory already exists
                pass
        # Download file to data/video if not downloaded
        video_file_path = Path(self.LOCAL_VIDEO_ROOT, self.output_video_name).as_posix()
        if not os.path.exists(video_file_path):
            print(
                "{} does not exist. Downloading now....".format(self.output_video_name)
            )
            wget.download(self.REMOTE_VIDEO_PATH, video_file_path)
