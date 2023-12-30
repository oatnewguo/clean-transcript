'''
Helps clean auto-generated transcripts, by replacing common mistakes and
by replacing Zoom's VTT format with one I think is more human-readable.
For more help, try python clean.py -h

To customize text replacements, modify the data in replacements.py

More complex changes that deal with format are documented within the clean method.
'''

import sys, re, argparse
from typing import Tuple, Dict, Callable
from replacements import case_sensitive_replacements, case_sensitive_entire_word_replacements, case_insensitive_replacements, case_insensitive_entire_word_replacements, case_preserving_replacements, case_preserving_entire_word_replacements, case_insensitive_repeats

for (key, value) in case_sensitive_entire_word_replacements.items():
    case_sensitive_replacements[fr"(?<=\W){key}(?=\W)"] = value
for (key, value) in case_insensitive_entire_word_replacements.items():
    case_insensitive_replacements[fr"(?<=\W){key}(?=\W)"] = value
for (key, value) in case_preserving_entire_word_replacements.items():
    case_preserving_replacements[fr"(?<=\W){key}(?=\W)"] = value

for (key, value) in case_preserving_replacements.items():
    # for an explanation of value=value, see https://docs.python-guide.org/writing/gotchas/#late-binding-closures
    case_insensitive_replacements[key] = lambda r, value=value: f"{value[0].lower()}{value[1:]}" if r.group()[0].islower() else f"{value[0].upper()}{value[1:]}"

for word in case_insensitive_repeats:
    case_insensitive_replacements[fr"(?<=\W{word})([ ,]+{word})+(?=\W)"] = ""

def clean(file_name: str, case_sensitive_replacements: Dict[str, str | Callable], case_insensitive_replacements: Dict[str, str | Callable]) -> None:
    '''
    Takes a file containing a Zoom automated transcript and cleans it, partially based on the replacements
    specified in the input dictionaries. Also deletes line numbers, simplifies timestamps, and combines
    consecutive lines that share the same speaker.
    '''

    with open(file_name, "r+") as file:
        text = file.read()

        print("\nFormatting changes:")

        # deletes line numbers and complicated timestamps and keeps just a simple start timestamp for each line.
        # I originally wrote this to work when importing transcript rows to NVivo, before I realized NVivo's transcript rows feature is hot garbage on Mac
        (text, replace_count) = handle_replacement(text,
                                                   r"(\d+\n)?(?P<start>(\d{2}:)?\d{2}:\d{2}\.\d)\d{2} --> (\d{2}:)?\d{2}:\d{2}\.\d{3}",
                                                   r"\g<start>")
        if replace_count != 0:
            print(f" {replace_count} lines/timestamps processed")

        # combines consecutive lines if they share the same speaker
        (text, replace_count) = handle_replacement(text, r"(?<=\d{2}:\d{2}\.\d\n)(?P<speaker>.+: )(?P<line_1>.+)\n\n(\d{2}:)?\d{2}:\d{2}\.\d\n(?P=speaker)(?P<line_2>.+)",
                                                   r"\g<speaker>\g<line_1> \g<line_2>")
        if replace_count != 0:
            print(f" {replace_count} times consolidating same-speaker lines")

        # case-sensitive replacements
        print("\nCase-sensitive replacements:")
        for problem in case_sensitive_replacements:
            (text, replace_count) = handle_replacement(text, problem, case_sensitive_replacements[problem])
            if replace_count != 0:
                print(f" {replace_count} replacements for \"{problem}\"")

        # case-insensitive replacements
        print("\nCase-insensitive replacements:")
        for problem in case_insensitive_replacements:
            (text, replace_count) = handle_replacement(text, problem, case_insensitive_replacements[problem], True)
            if replace_count != 0:
                print(f" {replace_count} replacements for \"{problem}\"")

        print("")

        file.seek(0)
        file.truncate()
        file.write(text.strip());

def handle_replacement(text: str, problem: str, replacement: str | Callable, case_insensitive: bool = False) -> Tuple[str, int]:
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

parser = argparse.ArgumentParser(description = """Helps clean auto-generated transcripts, by replacing common mistakes and by replacing Zoom's VTT format with one I think is more human-readable.
                                 
To customize text replacements, modify the data in replacements.py
                                 
More complex changes that deal with format are documented within the clean method.""")

parser.add_argument("file_name", help="name of file to clean; TXT or VTT expected")
parser.add_argument("-n", "--p_name", help="participant's name, to be aliased. Unlike other text replacements, <participant_name> is handled as a string, not as regex (to allow copy-and-pasting of Zoom names with parentheses).")
parser.add_argument("-a", "--p_alias", help="alias to replace participant's name.")
args = parser.parse_args()

if (args.p_name == None and args.p_alias != None) or (args.p_name != None and args.p_alias == None):
    sys.exit("Arguments p_name (-n) and p_alias (-a) must be used together or not at all.")

if not (args.file_name.lower().endswith(".txt") or args.file_name.lower().endswith(".vtt")):
    if input(f"TXT or VTT expected. Are you sure you want to clean {args.file_name}? (Y/N): ").lower() not in {"y", "yes"}:
        quit()

if args.p_name != None:
    case_sensitive_replacements[re.escape(args.p_name)] = args.p_alias

clean(args.file_name, case_sensitive_replacements, case_insensitive_replacements)