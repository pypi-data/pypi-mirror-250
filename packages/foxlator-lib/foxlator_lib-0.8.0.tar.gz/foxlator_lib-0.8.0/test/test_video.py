
import tempfile
from ddt import ddt, data  # type: ignore
from unittest.mock import MagicMock, patch
from src.foxlator_lib.video import AudioTextSegment, Video
from utils.video_base import VideoBase
from src import foxlator_lib as fll
from pathlib import Path
import os


@ddt
class VideoTests(VideoBase):
    invalid_paths = [Path('path-without-extension'),
                     Path('path.mp3'), Path('path.jpg'), Path('relative/path/file.obj')]

    @patch('os.path.isfile')
    def test_when_creating_video_from_not_existing_path_should_throw_error(self, mock_isfile: MagicMock):
        path = Path('some-path.mp4')
        mock_isfile.return_value = False
        self.assertRaises(fll.video.VideoError, lambda: fll.video.Video(path))
        mock_isfile.assert_called_once_with(path)

    @data(*invalid_paths)
    @patch('os.path.isfile')
    def test_when_creating_video_from_path_with_not_supported_extensions_should_throw_error(self, path: Path, mock_isfile: MagicMock):
        mock_isfile.return_value = None
        self.assertRaises(fll.video.VideoError, lambda: fll.video.Video(path))
        mock_isfile.assert_not_called()

    def test_create_video_with_subtitles_when_file_does_not_exists(self):
        with self.test_video_file() as video_path:
            video = Video(video_path)
            with tempfile.NamedTemporaryFile(suffix=".mp4") as temp_file:
                new_file = str(temp_file.name)
                try:
                    video.apply_subtitles(
                        [AudioTextSegment(0, 1, 'test')], Path(new_file))
                except Exception as e:
                    self.fail(f"Unexpected exception: {e}")
                self.assertFalse(os.path.samefile(video_path, new_file))

    def test_create_video_with_subtitles_when_file_already_exists(self):
        with self.test_video_file() as video_path:
            video = Video(video_path)
            output_file = video.apply_subtitles(
                [AudioTextSegment(0, 1, 'test')], video_path)
            self.assertTrue(os.path.exists(video_path))
            self.assertTrue(os.path.exists(output_file))
            self.assertFalse(os.path.samefile(video_path, output_file))
            self.assertEqual(video_path.parent, output_file.parent)

    def test_create_video_with_subtitles_when_output_path_is_dir(self):
        with self.test_video_file() as video_path:
            video = Video(video_path)
            with tempfile.TemporaryDirectory() as temp_dir:
                save_dir = Path(temp_dir)
                output_file = video.apply_subtitles(
                    [AudioTextSegment(0, 1, 'test')], save_dir)
                self.assertEqual(Path(os.path.join(
                    save_dir, video_path.name)), output_file)
