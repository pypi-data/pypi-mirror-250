"""Utilities for the Luis V subtitler package"""

import os
from pathlib import Path
from typing import Union

from moviepy.editor import VideoFileClip
from pytube import YouTube


def basic_test(
    argument_1: int = 1,
    argument_2: int = 2,
):
    """A simple test function

    Parameters
    ----------
    argument_1 : int, optional
        _description_, by default 1
    argument_2 : int, optional
        _description_, by default 2
    """

    print(argument_1, argument_2)
    return


def download_from_youtube(url: Union[str, os.PathLike]) -> str:
    """Download a Youtube video from its URL.
    It does this using the lowest video quality possible, as this package is only interested in audio.

    Parameters
    ----------
    url : Union[str, os.PathLike]
        URL to a youtube video

    Returns
    -------
    str
        A path to the location of the youtube video.
    """
    yt = YouTube(url)
    video_filename = (
        yt.streams.filter(progressive=True, file_extension="mp4")
        .order_by("resolution")  # lowest resolution possible
        .desc()
        .first()
        .download()
    )
    print(video_filename)

    return video_filename


def convert_video_to_audio_ffmpeg(video_filepath: Union[str, os.PathLike], output_ext: str = "wav") -> str:
    """Extract audio from a video file using FFMPEG.
    The audio file will be downloaded in the same folder as the video file.

    Parameters
    ----------
    video_filepath : Union[str, os.PathLike]
        Path to the video file.
    output_ext : str, optional
        Audio format for the output, for example, "wav" or "mp3", by default "wav"

    Returns
    -------
    str
        Path to the extracted audio file
    """

    path_obj = Path(video_filepath)
    filename = path_obj.parent / path_obj.stem
    # ext = path_obj.suffix

    output_file = f"{filename}.{output_ext}"

    # Load the video clip
    video_clip = VideoFileClip(video_filepath)

    # Extract the audio
    audio_clip = video_clip.audio

    # Save the audio to a new file
    audio_clip.write_audiofile(output_file)

    print(output_file)
    return output_file
