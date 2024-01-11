"""Tools for detecting the language using the Speechbrain library"""

import gc
import os
from pathlib import Path
from typing import Union

from pydub import AudioSegment
from speechbrain.pretrained import EncoderClassifier
from torch.cuda import empty_cache


def extract_subclip(audio_filepath: Union[str, os.PathLike]) -> str:
    """Extracts a subclip from an audio file, which will be used for language identification.
    The maximum length of the sublic is 3 minutes.
    If the audio is shorter than 3 minutes, then the whole audio is used.
    Otherwise, a clip of 3 minutes is extracted from the middle of the audio.

    Parameters
    ----------
    audio_file : Union[str, os.PathLike]
        Path to the full audio file.

    Returns
    -------
    str
        Path to the subclip audio file. It is in the same folder as the original audio file.
    """
    audio_clip = AudioSegment.from_file(audio_filepath)
    audio_duration = len(audio_clip) / 1000.0  # from miliseconds to seconds

    # at least 3 minutes

    min_secs_duration = 180

    if audio_duration < min_secs_duration:
        return audio_filepath
    else:
        # cut from the middle
        start_cut_timestamp = int(audio_duration / 2 - min_secs_duration / 2) * 1000
        end_cut_timestamp = int(audio_duration / 2 + min_secs_duration / 2) * 1000

    sub_audio_clip = audio_clip[start_cut_timestamp:end_cut_timestamp]

    # save the sub clip
    path_obj = Path(audio_filepath)
    filename = path_obj.parent / path_obj.stem
    ext = path_obj.suffix

    sub_clip_filepath = f"{filename}-subclip{ext}"
    sub_audio_clip.export(sub_clip_filepath)

    return sub_clip_filepath


# https://huggingface.co/speechbrain/lang-id-voxlingua107-ecapa
def identify_language(audio_filepath: Union[str, os.PathLike]) -> str:
    language_id_classifier = EncoderClassifier.from_hparams(source="speechbrain/lang-id-voxlingua107-ecapa", savedir="tmp")
    signal = language_id_classifier.load_audio(audio_filepath)

    prediction = language_id_classifier.classify_batch(signal)
    detected_language = prediction[3][0].split(":")[0]  # only get language code

    # free some GPU memory
    empty_cache()
    gc.collect()
    del language_id_classifier
    empty_cache()
    gc.collect()

    return detected_language
