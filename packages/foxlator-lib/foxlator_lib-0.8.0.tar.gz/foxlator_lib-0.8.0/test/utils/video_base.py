from pathlib import Path
import tempfile
from typing import Optional
from moviepy.editor import VideoClip  # type: ignore
from scipy.io.wavfile import write  # type: ignore
import numpy as np
from utils import base
from contextlib import contextmanager


class VideoBase(base.TestBase):
    def generate_frame(self, _: int):
        frame = np.random.randint(   # type: ignore
            0, 256, (640, 480, 3), dtype=np.uint8)
        return frame

    @contextmanager
    def test_video_file(self, path: Optional[Path] = None):
        video_clip = VideoClip(make_frame=self.generate_frame, duration=2)
        if path:
            video_clip.write_videofile(path, codec="libx264", fps=25)
            yield path
        else:
            with tempfile.NamedTemporaryFile(suffix=".mp4") as temp_file:
                temp_path = str(temp_file.name)
                video_clip.write_videofile(temp_path, codec="libx264", fps=25)
                yield Path(temp_path)
