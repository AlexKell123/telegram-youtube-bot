from abc import ABC, abstractmethod


class DownloaderAbs(ABC):

    @abstractmethod
    def download(self, video_id, ext):
        pass
