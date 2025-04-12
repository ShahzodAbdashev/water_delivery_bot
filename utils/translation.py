import gettext

LANGUAGES = ["uz", "ru", "en"]

translations = {
    lang: gettext.translation(
        "messages", localedir="translations", languages=[lang], fallback=True)
    for lang in LANGUAGES
}

def get_translator(lang: str):
    return translations.get(lang, translations["en"])

def _(phrase: str, lang: str):
    translator = get_translator(lang)
    return translator.gettext(phrase)