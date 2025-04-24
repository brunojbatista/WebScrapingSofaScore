import re;
import unicodedata as ud

def default_space(name):
    return re.sub(r'([\s ]+)', ' ', re.sub(r'(^[\s ]+|[\s ]+$)', '', str(name), re.M), re.M);

def clear_accents(name):
    return re.sub(r'[\u0300-\u036f]', '', ud.normalize("NFD", name));
    
def default_words(name):
    return re.sub(r'((?<= )(do|da|de|dos|das|ou|e|a|o|i|u|&|as|os)(?= )|[\'\(\)\[\]_\+\-\/\\\-\+\.\º,;\?]+)', ' ', name, flags=re.IGNORECASE);

def default_upper(name):
    converted = default_space(name);
    return converted.upper();

def default_lower(name):
    converted = default_space(name);
    return converted.lower();

def remove_spaces(name: str):
    return re.sub(r"\s", "", name)

def constant_name(name):
    return re.sub(r'([\s ]+)', '', default_upper(name), flags=re.IGNORECASE);

def is_equal_string(str1: str, str2: str):
    str1_prepared = default_space(default_lower(clear_accents(str1)))
    str2_prepared = default_space(default_lower(clear_accents(str2)))
    return str1_prepared == str2_prepared

def clear_break_lines(message):
    return re.sub(r"\n", '', message)

def slug_name(name, isLower=True):
    converted = clear_accents(name);
    converted = default_words(converted);
    converted = default_space(converted);
    converted = re.sub(r'(\s+)', ' ', converted);
    converted = re.sub(r'(\s+)', '_', converted);
    if (isLower):
        return converted.lower();
    else:
        return converted.upper();

def format_code(num, quantity = 3):
    str_number = str(num);
    len_str = len(str_number);
    diff = quantity - len_str;
    if diff <= 0: diff = 0;
    return ("0" * diff) + str_number

def clear_break_lines(content: str) -> str:
    return re.sub('\n', ' ', content, flags=re.I);

def extract_text_by_regex(regex: str, content: str) -> list:
    return re.findall(regex, content, flags=re.I);

def sub_latin_caracters(content: str, repl: str):
    return re.sub(r"[\u00A1-\u00FF]", repl, content)

def create_regex_latin_str(name):
    name_formatted = re.sub(r"[\'\(\)\[\]_\+\-\/\\\-\+\.,;\?\!\$\&\*\=\%]", r'\\\g<0>', name)
    name_formatted = sub_latin_caracters(default_space(re.sub(r'(?<=\s)(do|da|de|dos|das|ou|e|a|o|i|u|&|as|os|no|na|nos|nas)(?=\s)', ' ', name_formatted, flags=re.IGNORECASE)), ".")
    regex = r"^\s*" + re.sub(r"\s", r".+?", name_formatted) + r"\s*$"
    return regex

def remove_special_character(name):
    return re.sub(r"[\'\(\)\[\]_\+\-\/\\\-\+\.\º,;\?\!\$\&\*\=]", "", name)

def create_regex_lowercase_str(name):
    name_formatted = default_lower(clear_accents(name))
    name_formatted = re.sub(r"[\'\(\)\[\]_\+\-\/\\\-\+\.\º,;\?\!\$\&\*\=\%]", ".", name_formatted)
    regex = r"^\s*" + re.sub(r"\s", r".+?", name_formatted) + r"\s*$"
    return regex

def is_exact_occurrence(search, text) -> bool:
    """
    Verifica se 'search' aparece como uma ocorrência completa em 'text'.
    
    Args:
        search (str): A substring que você deseja buscar.
        text (str): O texto onde será feita a busca.

    Returns:
        bool: True se a ocorrência for exata, False caso contrário.
    """
    # Adiciona delimitadores de palavra na expressão regular
    pattern = fr"\b{re.escape(search)}\b"
    return bool(re.search(pattern, text))

def create_regex_filename_windows(name, extension = None):
    name_formatted = default_lower(clear_accents(name))
    name_formatted = re.sub(r"[\'\(\)\[\]_\+\-\/\\\-\+\.\º,;\?\!\$\&\*\=]", ".", name_formatted)
    if not extension is None: 
        regex =  r"^\s*" + re.sub(r"\s", r".+?", name_formatted) + r"\s*(\(\d+\))?\s*" + "\." + default_lower(clear_accents(extension)) + "$"
    else:
        regex = r"^\s*" + re.sub(r"\s", r".+?", name_formatted) + r"\s*(\(\d+\))?\s*$"
    return regex

def search_into_str_i(searched_str: str, search_str: str) -> int:
    searched_dafeult = default_lower(default_space(clear_accents(searched_str)))
    search_default = default_lower(default_space(clear_accents(search_str)))
    return search_default.find(searched_dafeult)

def format_folder_windows(name: str):
    return re.sub(r"[\\\/]", ".", re.sub(r'[\u0300-\u036f]', '', ud.normalize("NFD", name)));

def format_filename_windows(name: str, caract_sub="_"):
    return re.sub(r"[<>:\"\/\\|?*]+", caract_sub, name); 