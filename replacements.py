'''
Modify the data structures in this file to customize text replacements.
    The two case-sensitive dictionaries are mainly for correcting capitalization errors.
    The two case-insensitive dictionaries are mainly for correcting transcription and style errors for words with their own capitalization rules (e.g., proper nouns and words that are always lowercase, like k-anonymity).
    The two case-preserving dictionaries are mainly for correcting transcription and style errors for words without their own capitalization rules.
    The list at the end contains words that are generally safe to delete when they are repeated (e.g., "and," "the").

Keys and values ({"<key>": "<value>", ...}) are fed into re.subn:
    keys = regex patterns to find and replace
    values = replacements (either regex patterns or callables) corresponding to the parameter repl for re.sub: https://docs.python.org/3/library/re.html#re.sub

Replacements are carried out in order, which can affect outputs.
'''

# Makes replacements exactly as specified. May cause unintended replacements if a key is part of another word (e.g., "ios": "iOS" causes "curiosity" to become "curiOSity"). Mainly useful for replacements that have plurals and conjugations (e.g., "vpn": "VPN" also causes "vpns" to become "VPNs").
case_sensitive_replacements = {
    # capitalization errors
    "cpu": "CPU",
    "vpn": "VPN",
    "iphone": "iPhone",
    "ipad": "iPad",
    "google": "Google",
    "Google assistant": "Google Assistant",
    "youtube": "YouTube",
    "instagram": "Instagram",
    "android": "Android",
    "huawei": "Huawei",
    "motorola": "Motorola",
    "fitbit": "Fitbit",
    "gopro": "GoPro",
    "Siri shortcut": "Siri Shortcut",

    # removing ums and uhs but preserving capitalization for the word that follows
    r"(?<=\W)U[mh],? (?P<lower>[a-z]?)": lambda r: r.group('lower').upper(),
    r"(?<=\W)u[mh],? ": ""
}

# Only makes replacements if the key is a full word on its own (i.e., surrounded by spaces or punctuation). This means plurals and conjugations need to be added separately to be replaced.
case_sensitive_entire_word_replacements = {
    # capitalization errors
    "i": "I",
    "homekit": "HomeKit",
    "siri": "Siri",
    "icloud": "iCloud",
    "ios": "iOS",
    "iot": "IoT",
    "discord": "Discord",
    "https": "HTTPS",
    "http": "HTTP",
    "home depot": "Home Depot",
    "best buy": "Best Buy",
    "alexa": "Alexa",
    "seo": "SEO",
    "hello fresh": "Hello Fresh",
    "internet": "Internet",
    "gdpr": "GDPR",
    "adsense": "AdSense",
    "bluetooth": "Bluetooth",
    "ethernet": "Ethernet",
    "hdmi": "HDMI",

    # formatting proper nouns and abbreviations
    "US": "U.S."
}

# Makes replacements ignoring case. Keys and values must have differences other than capitalization; otherwise, they trigger an infinite loop.
case_insensitive_replacements = {
    # transcription errors
    "k-animity": "k-anonymity",
    r"home kits?": "HomeKit", # use regex to match both "home kit" and "home kits"
    r"home kids?": "HomeKit",
    "smart thing": "SmartThing",
    "series shortcut": "Siri Shortcut",
    "home pod": "HomePod",
    "nord vpn": "NordVPN",
    "more vpn": "NordVPN",
    "nordvpns": "NordVPN's",
    "express vpn": "ExpressVPN",
    "wi fi": "Wi-Fi",
    "wifi": "Wi-Fi",

    # style nitpicks
    "internet connected": "Internet-connected",

    # miscellaneous replacements
    "Wentao Guo": "Wentao",
    "WEBVTT": ""
}

# Only makes replacements (ignoring case) if the key is a full word on its own.
case_insensitive_entire_word_replacements = {
    # transcription errors
    "coven": "COVID",
    "i cloud": "iCloud",
    "mag safe": "MagSafe",
    "wire shark": "Wireshark"
}

# Makes replacements in re.IGNORECASE mode but capitalizes the replacement if the replaced text was capitalized. Keys and values must have differences other than capitalization; otherwise, they trigger an infinite loop.
case_preserving_replacements = {
    # transcription errors
    "deep fake": "deepfake",
    "the identification": "de-identification",
    "de identification": "de-identification",
    "smart log": "smart lock",

    # style nitpicks
    "data set": "dataset"
}

# Only makes replacements (in re.IGNORECASE mode) if the key is a full word on its own. Capitalizes the replacement if the replaced text was capitalized.
case_preserving_entire_word_replacements = {
}

# Deletes repeated words from this list, regardless of case. Words are considered repeated if they are separated only by spaces and/or commas.
case_insensitive_repeats = {
    "the", "a", "an", "but", "and", "or", "if", "then", "so", "this", "that", "those", "these",
    "I", "my", "I'm", "I'll", "I've", "I'd", "you", "your", "we", "our", "we're", "we'll", "we've", "we'd", "they", "their", "it", "its", "it's",
    "is", "are", "was", "were", "can", "will", "may", "might",
    "who", "what", "where", "when", "why", "how",
    "about", "as", "at", "by", "for", "from", "in", "like", "of", "on", "to", "with"
}