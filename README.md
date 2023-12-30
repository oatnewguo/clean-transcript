# Wentao's tools for cleaning transcripts

These Python scripts help clean auto-generated transcripts.
- merge.py adds info about speakers from one VTT file to another VTT file of the same recording without speaker information. It's useful when you have one VTT with labeled speakers but worse transcription (e.g., Zoom) and another without labeled speakers but better transcription (e.g., OpenAI's Whisper). Note that speaker labels will probably be slightly off depending on how lines are split up and timestamped, so some manual cleaning is likely necessary.
- clean.py replaces common mistakes and changes the VTT format into one I think is more human-readable for qualitative coding and analysis. You can easily customize text replacements by modifying the data in replacements.py (instructions in file).

You can ignore merge.py and just run clean.py if you're not merging two transcripts. If you are merging, I recommend you run merge.py first and then clean.py on the updated file, as clean.py consolidates consecutive lines if it knows they have the same speaker. Both scripts print output summarizing changes made, but it's still probably best to run before and not after manual cleaning so you can catch mistakes.

## Running the scripts

Merge: ``python merge.py <text_file_name> <speaker_file_name>``, where ``<text_file_name>`` is the name of the VTT file with better transcription, and ``<speaker_file_name>`` is the name of the VTT file with speaker labels. 

Clean: ``python clean.py <file_name> -n <participant_name> -a <participant_alias>``. ``<participant_name>`` and ``<participant_alias>`` are optional; if provided, all instances of the name are replaced by the alias (e.g., replace "Wentao Guo" with "P1").

## How I finish cleaning transcripts

After cleaning a transcript using these scripts, I do a full manual pass to catch mistakes ranging from these scripts making unintended changes to hallucinations by the transcription algorithm. As a Mac user, I use the free version of ExpressScribe to control audio playback, and I use a separate text editor to edit the transcript. In ExpressScribe, you can customize controls such as play, pause, rewind, and fast-forward and map them to different function keys, and in MacOS's System Preferences, you can toggle the setting ``Keyboard > Keyboard Shortcuts > Function Keys > Use F1, F2, etc. keys as standard function keys`` in order to access these controls without holding down ``fn``.

ExpressScribe sometimes converts installed free versions into trials of the pro version; if you encounter a message saying that your trial of the pro version has expired, you should be able to uninstall ExpressScribe and re-download the free version (make sure it's explicitly the free version) to regain access.