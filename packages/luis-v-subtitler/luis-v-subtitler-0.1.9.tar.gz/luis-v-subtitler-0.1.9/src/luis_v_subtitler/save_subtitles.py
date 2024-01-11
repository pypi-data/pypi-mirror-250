"""Tools for saving files with subtitles
"""

import codecs  # This package supports all Unicode characters!
import os
from pathlib import Path
from typing import Union

from whisperx.utils import WriteSRT


def save_to_txt_file(annotated_transcription_result: dict, txt_path: Union[str, os.PathLike]) -> str:
    """Save the transcriptions into a TXT file.
    Extracts the list of phrases from the transcription, and writes them to a TXT file.

    Parameters
    ----------
    annotated_transcription_result : dict
        transcription result from a Whisper model
    txt_path : Union[str, os.PathLike]
        File path for the TXT file.

    Returns
    -------
    str
        Returns the `txt_path` input
    """
    sentence_list = [entry["text"].strip() for entry in annotated_transcription_result["segments"]]
    with codecs.open(txt_path, "w", "utf-8") as fp:
        fp.write("\n".join(sentence_list))
    return txt_path


def generate_txt_path(input_file_path: Union[str, os.PathLike], extension: str = "txt") -> str:
    """Generate a file path for a text file. This file path will be in the same parent directory as `input_file_path`

    Parameters
    ----------
    input_file_path : Union[str, os.PathLike]
        File path in the directory where the text file should be saved.
    extension : str, optional
        Extension for the text file, for example, "txt" or "srt", by default "txt"

    Returns
    -------
    str
        File path for the text file.
    """
    path_obj = Path(input_file_path)
    filename = path_obj.parent / path_obj.stem
    # ext = path_obj.suffix
    result = f"{filename}.{extension}"
    print(result)
    return result


# https://github.com/mshakirDr/whisperX/blob/653680008ce62e4622c14c250cc9d1a3c5b65b13/whisperx/utils.py#L73
def save_to_srt_file(
    subtitles_path: Union[str, os.PathLike],
    annotated_transcription_result: dict,
):
    """Save the transcriptions from a WhisperX model into a SRT file.

    Parameters
    ----------
    subtitles_path : Union[str, os.PathLike]
        File path where the subtitles will be stored
    annotated_transcription_result : dict
        Output from WhisperX model
    """
    path_obj = Path(subtitles_path)
    parent_directory = path_obj.parent

    subtitle_writer = WriteSRT(parent_directory)
    with codecs.open(subtitles_path, "w", "utf-8") as fp:
        subtitle_writer.write_result(
            result=annotated_transcription_result,
            file=fp,
            options={
                "highlight_words": False,
                "max_line_count": None,
                "max_line_width": None,
            },
        )
