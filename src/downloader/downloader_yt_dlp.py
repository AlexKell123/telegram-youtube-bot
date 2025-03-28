import yt_dlp

from src.downloader.downloader_abs import DownloaderAbs


class Downloader(DownloaderAbs):

    def download(self, video_id, ext):
        ydl_opts = self._set_ydl_opts(video_id, ext)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_id])

    @staticmethod
    def _set_ydl_opts(video_id, ext):
        ydl_opts = {'.mp4': {'max_filesize': 20000000000,
                             'format': 'best',
                             'outtmpl': video_id + ext,
                             'output': video_id + ext},
                    '.mp3': {'format': 'bestaudio/best',
                             'outtmpl': video_id + ext,
                             'output': video_id + ext}
                    }

        return ydl_opts[ext]
