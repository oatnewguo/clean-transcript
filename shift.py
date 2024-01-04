'''
Shifts all timestamps in one VTT file.
Behaves incorrectly if timestamps go (or would be shifted) over 24 hours.
For more help, try python shift.py -h.

For cases when two VTT files are not aligned (e.g., a recording was split into segments
to feed into Whisper).
'''

import argparse, webvtt, datetime

def shift(file_name: str, seconds: int) -> None:
    '''
    Shifts timestamps by the specified number of seconds. Updates the provided file.
    '''

    vtt = webvtt.read(file_name)

    for caption in vtt:
        new_start = datetime.datetime.combine(datetime.date.today(), datetime.time.fromisoformat(caption.start)) + datetime.timedelta(seconds=seconds)
        caption.start = new_start.time().isoformat("milliseconds")

        new_end = datetime.datetime.combine(datetime.date.today(), datetime.time.fromisoformat(caption.end)) + datetime.timedelta(seconds=seconds)
        caption.end = new_end.time().isoformat("milliseconds")

    vtt.save()

parser = argparse.ArgumentParser(description = "Shifts all timestamps in one VTT file. Behaves incorrectly if timestamps go over 24 hours. For cases when two VTT files are not aligned (e.g., a recording was split into segments to feed into Whisper).")

parser.add_argument("file_name", help="name of VTT file; this file is updated")
parser.add_argument("seconds", help="number of seconds to shift timestamps (forward) by; negative values shift timestamps backwards")

args = parser.parse_args()
if not args.file_name.lower().endswith(".vtt"):
    if input(f"VTT expected. Are you sure you meant {args.file_name}? (Y/N): ").lower() not in {"y", "yes"}:
        quit()

shift(args.file_name, int(args.seconds))
