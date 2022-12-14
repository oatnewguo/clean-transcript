'''
Helps clean auto-generated transcripts, by replacing common mistakes and
by replacing Zoom's .vtt format with one I think is more human-readable.

To tailor this script to your needs, you can modify the two dictionaries at the top
that handle replacements: case_sensitive_replacements and case_insensitive_replacements.
Keys and values ({"<key>": "<value>", ...}) are fed into re.subn:
    keys = regex patterns to find and replace
    values = string replacements
You can also add strings to the case_insensitive_repeats set,
which the code will transform and add to case_insensitive_replacements
to look for common repeat words that are safe to replace.

More complex changes that deal with format are documented within the clean method.

Run using "python3 clean.py <file_name>".
Expects P<number>.txt or .vtt for file_name and will double-check if you provide anything else.

To also replace the participant's name with an alias, run using
"python3 clean.py <file_name> <participant_name> <participant_alias>".
Unlike the dictionary-based replacements, <participant_name> is handled as a string, not as regex
(this is to allow easy copy-and-pasting of Zoom names that contain parentheses).
'''

import sys, re, warnings
from typing import Tuple, Dict

case_sensitive_replacements = {
    "i'm": "I'm",
    "i've": "I've",
    "i'll": "I'll",
    "i'd": "I'd",
    "Wentao Guo": "Wentao",
    "homekit": "HomeKit",
    " apple ": " Apple ",
    "APP": "app",
    "DEMO": "demo",
    " nest ": " Nest ",
    " siri ": " Siri ",
    "Siri shortcut": "Siri Shortcut",
    "WEBVTT": "",
    "internet": "Internet",
    "gdpr": "GDPR",
    " US ": " U.S. ",
    "icloud": "iCloud",
    " ios ": " iOS ",
    "iphone": "iPhone",
    "ipad": "iPad",
    "Home Platform": "home platform",
    "adsense": "AdSense",
    "google": "Google",
    "Google assistant": "Google Assistant",
    "bluetooth": "Bluetooth",
    " iot ": " IoT ",
    "discord": "Discord",
    "https": "HTTPS",
    "http": "HTTP",
    "gopro": "GoPro",
    "ethernet": "Ethernet",
    "cpu": "CPU",
    "home depot": "Home Depot",
    "best buy": "Best Buy",
    "hdmi": "HDMI",
    "youtube": "YouTube",
    "android": "Android",
    "fitbit": "Fitbit",
    "huawei": "Huawei",
    "motorola": "Motorola",
    "alexa": "Alexa",
    "vpn": "VPN",
    " seo ": " SEO ",
    "instagram": "Instagram"
}

case_insensitive_replacements = {
    "home kits": "HomeKit",
    "home kit": "HomeKit",
    "home kids": "HomeKit",
    "home kid": "HomeKit",
    "home care": "HomeKit",
    "smart thing": "SmartThing",
    "series shortcut": "Siri Shortcut",
    "smart log": "smart lock",
    "wi fi": "Wi-Fi",
    "internet connected": "Internet-connected",
    "mm hmm": "mmhmm",
    "i cloud": "iCloud",
    "home pod": "HomePod",
    " coven ": " COVID ",
    "mag safe": "MagSafe",
    "wire shark": "Wireshark",
    "deep fake": "deepfake"
}

case_insensitive_repeats = {
    "the", "a", "an", "but", "and", "or", "if", "then", "so", "this", "that", "those", "these",
    "I", "my", "I'm", "I'll", "I've", "I'd", "you", "your", "we", "our", "we're", "we'll", "we've", "we'd", "they", "their", "it", "its", "it's",
    "is", "are", "was", "were", "can", "will", "may", "might",
    "who", "what", "where", "when", "why", "how",
    "about", "as", "at", "by", "for", "from", "in", "like", "of", "on", "to", "with"
}
for word in case_insensitive_repeats:
    case_insensitive_replacements[fr"(?P<first>\W{word})(\W{word})+(?P<end_delimiter>\W)"] = f"\g<first>\g<end_delimiter>"

def clean(file_name: str, case_sensitive_replacements: Dict[str, str], case_insensitive_replacements: Dict[str, str]) -> None:
    '''
    Takes a file containing a Zoom automated transcript and cleans it, partially based on the replacements
    specified in the input dictionaries. Also deletes line numbers, simplifies timestamps, and combines
    consecutive lines that share the same speaker.
    '''

    with open(file_name, "r+") as file:
        text = file.read()

        # basic case-sensitive replacements
        print("\nBasic case-sensitive replacements:")
        for problem in case_sensitive_replacements:
            (text, replace_count) = handle_replacement(text, problem, case_sensitive_replacements[problem])
            if replace_count != 0:
                print(f" {replace_count} replacements for \"{problem}\"")

        # basic case-insensitive replacements
        print("\nBasic case-insensitive replacements:")
        for problem in case_insensitive_replacements:
            (text, replace_count) = handle_replacement(text, problem, case_insensitive_replacements[problem], True)
            if replace_count != 0:
                print(f" {replace_count} replacements for \"{problem}\"")

        print("\nOther changes:")

        # deletes line numbers and complicated timestamps and keeps just a simple start timestamp for each line.
        # I wrote this to work when importing transcript rows to NVivo, before I realized NVivo's transcript rows feature is hot garbage on Mac
        (text, replace_count) = handle_replacement(text, r"\d+\n(?P<start>\d{2}:\d{2}:\d{2}\.\d)\d{2} --> \d{2}:\d{2}:\d{2}\.\d{3}",
                                                   r"\g<start>")
        if replace_count != 0:
            print(f" {replace_count} lines/timestamps processed")

        # combines consecutive lines if they share the same speaker
        (text, replace_count) = handle_replacement(text, r"(?<=\d{2}:\d{2}:\d{2}\.\d\n)(?P<speaker>.+: )(?P<line_1>.+)\n\n\d{2}:\d{2}:\d{2}\.\d\n(?P=speaker)(?P<line_2>.+)",
                                                   r"\g<speaker>\g<line_1> \g<line_2>")
        if replace_count != 0:
            print(f" {replace_count} times consolidating same-speaker lines")

        print("")

        file.seek(0)
        file.truncate()
        file.write(text.strip());

def handle_replacement(text: str, problem: str, replacement: str, case_insensitive: bool = False) -> Tuple[str, int]:
    '''
    Attempts to replace all instances in text of the regex pattern specified by problem.
    Returns a tuple of the updated string, as well as a count of the number of replacements completed.
    Does not handle printing feedback, but a warning may be raised if the function terminated early
    because it seemed to be caught in an infinite loop.
    '''

    replace_count = 0
    loop_counter = 0

    while True:
        loop_counter += 1
        if loop_counter > 20:
            sys.exit(f" Processed the entire text 20 times replacing \"{problem}\" without concluding. Quitting without saving changes. Is the replacement causing an infinite loop?")

        if case_insensitive:
            (text, partial_replace_count) = re.subn(problem, replacement, text, flags = re.IGNORECASE)
        else:
            (text, partial_replace_count) = re.subn(problem, replacement, text)

        if partial_replace_count == 0:
            break
        replace_count += partial_replace_count

    return (text, replace_count)

if len(sys.argv) > 1:
    file_name = sys.argv[1]
    if not re.fullmatch(r"P\d+\.(txt|vtt)", file_name):
        if input(f"Are you sure you want to clean {file_name}? (Y/N): ").lower() not in {"y", "yes"}:
            quit()

    if len(sys.argv) > 3:
        case_sensitive_replacements[re.escape(sys.argv[2])] = sys.argv[3]

    clean(file_name, case_sensitive_replacements, case_insensitive_replacements)
