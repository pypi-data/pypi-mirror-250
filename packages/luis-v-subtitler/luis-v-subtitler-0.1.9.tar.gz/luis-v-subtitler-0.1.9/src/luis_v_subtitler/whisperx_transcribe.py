"""Tools for using whisperx to transcribe a video
"""

import gc
import os
from copy import deepcopy
from typing import Union

import whisperx
from torch import device
from torch.cuda import empty_cache
from torch.cuda import is_available
from whisperx import align
from whisperx import load_align_model

my_device = device("cuda" if is_available() else "cpu")
print(f"Using {my_device}")


def get_phrase_level_timestamps(
    audio_filename: Union[str, os.PathLike],
    language: str,
    batch_size=16,
) -> dict:
    """Use a Whisper model to get time stamps for phrases.

    Parameters
    ----------
    audio_filename : Union[str, os.PathLike]
        File path to the audio to be transcribed
    language : str
        Language code of the audio to be transcribed
    batch_size : int, optional
        batch size for the Whisper model, by default 16

    Returns
    -------
    dict
        A dictionary containing text phrases from the audio, timestamps, and other metadata.
    """

    print("Loading Whisper Model:")
    phrase_model = whisperx.load_model(
        "large-v3",
        device=str(my_device),
        # compute_type = compute_type,
        language=language,
    )

    audio = whisperx.load_audio(audio_filename)
    print("Transcribing phrases")
    phrase_level_transcription = phrase_model.transcribe(audio, batch_size=batch_size, print_progress=True)

    # freeing device memory
    empty_cache()
    gc.collect()
    del phrase_model
    empty_cache()
    gc.collect()

    return phrase_level_transcription


def get_word_level_timestamps(
    audio_filename: Union[str, os.PathLike],
    phrase_level_transcription: dict,
    language: str,
) -> dict:
    """Use a WhisperX model to get time stamps for words in an audio

    Parameters
    ----------
    audio_filename : Union[str, os.PathLike]
        File path to the audio to be transcribed
    phrase_level_transcription : dict
        Transcriptions at the phrase level. It is the output from a Whisper model
    language : str
        Language code of the audio to be transcribed

    Returns
    -------
    dict
        A dictionary containing the words from the audio, timestamps, phrases, and other metadata
    """

    print(f"Loading Whisper X model on device: {my_device}")

    word_alignment_model, metadata = load_align_model(language_code=language, device=my_device)

    print("Aligning at the word level")

    word_level_transcription = align(
        deepcopy(phrase_level_transcription["segments"]), word_alignment_model, metadata, audio_filename, str(my_device)
    )

    # free some device memory
    empty_cache()
    gc.collect()
    del word_alignment_model
    empty_cache()
    gc.collect()

    return word_level_transcription
