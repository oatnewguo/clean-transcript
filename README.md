# Wentao's tools for cleaning transcripts

These Python scripts help clean auto-generated transcripts.
- merge.py adds info about speakers from one VTT file to another VTT file of the same recording without speaker information. It's useful when you have one VTT with labeled speakers but worse transcription (e.g., Zoom) and another without labeled speakers but better transcription (e.g., OpenAI's Whisper). Note that speaker labels are applied at the caption level, so if the VTT with better transcription doesn't start a new caption when the speaker switches, then you still need to do some manual cleaning whenever the speaker switches.
- clean.py replaces common mistakes and changes the VTT format into one I think is more human-readable for qualitative coding and analysis. You can easily remove and add new replacements to the dictionaries in the code (more detailed instructions documented in the file). You *should* do this, as the current replacements are tailored to my own work, and there are likely some I considered safe that you will not (e.g., if you study witches, you probably don't want to auto-correct *coven* to *COVID*).

You can ignore merge.py and just run clean.py if you're not merging two transcripts. If you are merging, I recommend you run merge.py first and then clean.py on the updated file, as clean.py consolidates consecutive lines if it knows they have the same speaker. Both scripts print output summarizing changes made, but it's still probably best to run before and not after manual cleaning so you can catch mistakes (especially for clean.py, as there may be exceptions to the text replacement rules).

## Running the scripts

Merge: ``python merge.py <text_file_name> <speaker_file_name>``, where ``<text_file_name>`` is the name of the VTT file with better transcription, and ``<speaker_file_name>`` is the name of the VTT file with speaker labels. 

Clean: ``python clean.py <file_name> -n <participant_name> -a <participant_alias>``. You should run this a few times until it stops reporting changes (I plan to fix this issue in the future). ``<participant_name>`` and ``<participant_alias>`` are optional; if provided, all instances of the name are replaced by the alias (e.g., replace "Wentao Guo" with "P1").

## How I finish cleaning transcripts

After cleaning a transcript using these scripts, I do a full manual pass. As a Mac user, I use ExpressScribe, free version, to control audio playback, and I use a plain text editor to edit the transcript. In ExpressScribe, you can customize controls such as play, pause, rewind, and fast-forward and map them to different function keys, and in MacOS's System Preferences, you can toggle the setting ``Keyboard > Keyboard Shortcuts > Function Keys > Use F1, F2, etc. keys as standard function keys`` setting to let you access these controls without holding down ``fn``.
