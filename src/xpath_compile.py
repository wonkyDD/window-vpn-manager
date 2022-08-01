from .xpath import xpath

def read_xpath(function_name: str, xpath_name: str) -> str:
    return xpath[function_name][xpath_name]