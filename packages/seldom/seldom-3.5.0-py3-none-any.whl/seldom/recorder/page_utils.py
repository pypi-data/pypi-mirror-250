import re


def is_valid_url(url):
    regex = re.compile(
        r"^(?:http)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+"
        r"(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    if (
        regex.match(url)
        or url.startswith("about:")
        or url.startswith("blob:")
        or url.startswith("chrome:")
        or url.startswith("data:")
        or url.startswith("edge:")
        or url.startswith("file:")
    ):
        return True
    else:
        return False
