from modules.configs.MyConfig import config

EN = "en_US"
CN = "zh_CN"
JP = "jp_JP"
ORDER = [EN, CN, JP]
def istr(input, use_config = config) -> str:
    """多语言解析器"""
    lang_pack = {}
    lang_type = use_config.softwareconfigdict.get("LANGUAGE", EN)
    if isinstance(input, dict):
        for lang in ORDER:
            if lang in input:
                lang_pack[lang] = input[lang]
    else:
        lang_pack[ORDER[0]] = str(input)
        
    # return the corresponding language
    if lang_type in lang_pack:
        return lang_pack[lang_type]
    elif len(lang_pack) > 0:
        for lang in ORDER:
            if lang in lang_pack:
                return lang_pack[lang]
    else:
        return "No language found"
        