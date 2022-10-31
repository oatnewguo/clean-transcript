# Wentao's tool for cleaning transcripts

This Python script helps clean auto-generated transcripts, by replacing common mistakes and by replacing Zoom's .vtt format with one I think is more human-readable. It will summarize the changes it makes, but it's still probably best to run before and not after manual cleaning so you can catch mistakes.

You can easily tailor this script to your needs by removing and adding new replacements to the dictionaries in the code (more detailed instructions documented in the code). You should probably do this in any case, as the current replacements are tailored to my own work in human-centered security and privacy, and there are likely some I considered safe that you will not (e.g., if you study witches, you probably don't want to auto-correct *coven* to *COVID*).

## Running the script

Run using ``python3 clean.py <file_name>``. The script expects ``P<number>.txt`` or ``.vtt`` for ``file_name`` and will double-check if you provide anything else.

To also replace the participant's name with an alias, run using ``python3 clean.py <file_name> <participant_name> <participant_alias>``. Unlike the dictionary-based replacements, ``<participant_name>`` is handled as a string, not as regex (this is to allow easy copy-and-pasting of Zoom names that contain parentheses).

## How I finish cleaning transcripts

After downloading a transcript and cleaning it using this script, I do a full manual pass. As a Mac user, I use ExpressScribe, free version, to control audio playback, and I use a plain text editor to edit the transcript. In ExpressScribe, you can customize controls such as play, pause, rewind, and fast-forward and map them to different function keys, and in MacOS's System Preferences, you can toggle the ``Keyboard > Use F1, F2, etc. keys as standard function keys`` setting to let you access these controls without holding down ``fn``.
