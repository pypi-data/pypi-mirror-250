import typing
import os
import moviepy.editor as mp  # type: ignore
from moviepy.video.tools.subtitles import SubtitlesClip  # type: ignore
from pathlib import Path
import logging

from .stt.whisper_stt import AudioTextSegment
from .audio import AudioPath
from .error import BaseError


class VideoError(BaseError):
    pass


class Video(object):
    known_extensions = ['.mp4']

    # TODO: Handle case: "For Ubuntu 16.04LTS users, after installing MoviePy on the terminal, IMAGEMAGICK will not be detected by moviepy"
    def __init__(self, path: Path):
        self.path = path
        self.extension = self._validate_extension(path)

        if (not os.path.isfile(path)):
            raise VideoError(f"Video file: '{path}' doesn't exist")
        self.clip: mp.VideoFileClip = mp.VideoFileClip(str(self.path))

    def _gen_output_filename(self, path: Path):
        filename = Path(os.path.join(path, self.path.name)
                        ) if path.is_dir() else path
        if not filename.exists():
            return filename
        new_filename = Path(os.path.join(
            filename.parent, f"{filename.stem}_subtitletd{self.extension}"))
        logging.warning('%s file already exists. Saving as %s',
                        filename, new_filename)
        return new_filename

    def apply_subtitles(self, subtitles: typing.List[AudioTextSegment], path: Path):
        # TODO: make it all configurable (in next version?), research if there is any better way of
        # TODO: editing frames with timestamps (preferably compatible with opencv)
        def generator(text: str) -> mp.TextClip:
            return mp.TextClip(
                text, font='Arial', fontsize=24, color='white')
        subtitles_clip = SubtitlesClip(
            [subtitle.serialize() for subtitle in subtitles], generator)
        composed_clip = mp.CompositeVideoClip([
            self.clip, subtitles_clip.set_position(('center', 'bottom'))
        ])
        output_file = self._gen_output_filename(path)
        composed_clip.write_videofile(str(output_file), logger=None)
        return output_file

    def get_audio_path(self) -> AudioPath:
        if self.clip.audio:
            return AudioPath(audio=self.clip.audio)
        raise VideoError(reason="Clip doesn't have audio path")

    def _validate_extension(self, path: Path) -> str:
        extension: str = path.suffix
        if len(extension) == 0:
            raise VideoError(
                "Provided file path is invalid or doesn't contain extension")
        if extension not in self.known_extensions:
            raise VideoError(f"Unsupported file extension: {extension}")
        return extension
