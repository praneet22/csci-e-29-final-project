import os
from unittest import TestCase
from final_project.tasks.data import DownloadVideo
from tempfile import TemporaryDirectory
from luigi import build
from final_project.cli import main

def test_main():
    main([])

class DataTests(TestCase):

    def test_DownloadVideo_copy(self):
        """Ensure download image"""
        videoFile = "orangutan.mp4"
        REMOTE_VIDEO_PATH = "https://happypathspublic.blob.core.windows.net/videos/orangutan.mp4"
        with TemporaryDirectory() as tmp:
            LOCAL_VIDEO_ROOT = "."
            build([DownloadVideo(LOCAL_VIDEO_ROOT=LOCAL_VIDEO_ROOT,REMOTE_VIDEO_PATH=REMOTE_VIDEO_PATH)], local_scheduler=True)
            self.assertTrue(os.path.exists(videoFile))