'''
Adds info about speakers from one VTT file to another VTT file of the same recording without speaker information.
For more help, try python merge.py -h.

Useful when you have one VTT with labeled speakers but worse transcription (e.g., Zoom)
and another without labeled speakers but better transcription (e.g., OpenAI's Whisper).
Note that speaker labels are applied at the caption level, so if the VTT with better transcription
doesn't start a new caption when the speaker switches, then you still need to do some manual cleaning
whenever the speaker switches.
'''

import sys, re, argparse, webvtt, datetime
from collections.abc import Iterator
from typing import Tuple

def merge(text_file_name: str, speaker_file_name: str) -> None:
    '''
    Adds info about speakers from the speaker VTT file to the text VTT file.
    The text file is modified, and the speaker file is unchanged.
    '''

    text_vtt = webvtt.read(text_file_name)
    speaker_vtt = webvtt.read(speaker_file_name)
    speaker_iter = iter(speaker_vtt)
    current_name = None
    (next_speaker_time, next_name) = get_next_info(speaker_iter)
    if next_speaker_time == None:
        sys.exit(f" {speaker_file_name} does not seem to be a valid, non-empty VTT file. No changes made.")

    speaker_counts = {}
    no_speaker_count = 0

    for caption in text_vtt:
        while next_speaker_time and datetime.time.fromisoformat(caption.start) >= next_speaker_time:
            current_name = next_name
            (next_speaker_time, next_name) = get_next_info(speaker_iter)
        if current_name:
            caption.text = f"{current_name}: {caption.text}"
            if current_name in speaker_counts:
                speaker_counts[current_name] += 1
            else:
                speaker_counts[current_name] = 1
        else:
            no_speaker_count += 1

    for speaker in speaker_counts:
        print(f" {speaker} added to {speaker_counts[speaker]} lines.")
    print(f" Skipped {no_speaker_count} lines because the speaker could not be identified.")
    print("")

    text_vtt.save()    

def get_next_info(iter: Iterator[webvtt.structures.Caption]) -> Tuple[datetime.time, str]:
    '''
    Returns a tuple containing the start time and speaker (if found) of the next caption in a VTT iterator,
    or (None, None) if the iterator is at the end.
    '''

    try:
        next_caption = next(iter)
    except StopIteration:
        return (None, None)
    
    speaker_partition = next_caption.text.partition(":")
    return (datetime.time.fromisoformat(next_caption.start), speaker_partition[0] if speaker_partition[2] else None)


parser = argparse.ArgumentParser(description = "Adds info about speakers from one VTT file to another VTT file of the same recording without speaker information. Useful when you have one VTT with labeled speakers but worse transcription (e.g., Zoom) and another without labeled speakers but better transcription (e.g., OpenAI's Whisper). Note that speaker labels are applied at the caption level, so if the VTT with better transcription doesn't start a new caption when the speaker switches, then you still need to do some manual cleaning whenever the speaker switches.")

parser.add_argument("text_file_name", help="name of VTT file with better transcription; this file is updated")
parser.add_argument("speaker_file_name", help="name of VTT file with speaker labels; this file is unchanged")

args = parser.parse_args()
if not args.text_file_name.lower().endswith(".vtt"):
    if input(f"Are you sure you meant {args.text_file_name}? (Y/N): ").lower() not in {"y", "yes"}:
        quit()
if not args.speaker_file_name.lower().endswith(".vtt"):
    if input(f"Are you sure you meant {args.speaker_file_name}? (Y/N): ").lower() not in {"y", "yes"}:
        quit()

merge(args.text_file_name, args.speaker_file_name)
