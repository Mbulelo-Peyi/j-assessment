import re
import urllib.parse
import ipaddress

# RFC 5322-compliant (practical subset) email regex
EMAIL_REGEX = re.compile(
    r"^(?:(?:[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+"
    r"(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*)|"
    r"(?:\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]"
    r"|\\[\x00-\x7f])*\")"
    r")@(?:(?:[a-zA-Z0-9]"
    r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z]{2,})$"
)

def is_valid_email(email:str) -> (str | None):
    if not isinstance(email, str) or not email or len(email) > 254:
        return None

    if not EMAIL_REGEX.fullmatch(email):
        return None

    try:
        local, domain = email.rsplit('@', 1)
    except ValueError:
        return None

    if len(local.encode('utf-8')) > 64 or len(domain.encode('utf-8')) > 255:
        return None

    return email


def clean_and_verify_url(url:str) -> (str | None):
    if not isinstance(url, str) or not url.strip():
        return None

    url = url.strip()

    # Remove scheme and www, and trailing slashes
    url = re.sub(r'^(https?://)?(www\.)?', '', url)
    url = re.sub(r'/+$', '', url)

    if not url:
        return None

    # Add scheme to parse properly
    full_url = f"https://{url}"

    try:
        parsed = urllib.parse.urlparse(full_url)

        if parsed.scheme not in ('http', 'https'):
            return None

        if not parsed.hostname:
            return None

        hostname = parsed.hostname.strip('[]')

        # Check if IP is valid
        is_ipv6 = False
        try:
            ip = ipaddress.ip_address(hostname)
            is_ipv6 = isinstance(ip, ipaddress.IPv6Address)
        except ValueError:
            # Domain must be valid
            if '..' in hostname or hostname.startswith('-') or hostname.endswith('-'):
                return None
            if not re.match(r'^([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$|^localhost$', hostname):
                return None

        # Check valid port
        if parsed.port is not None and (parsed.port < 0 or parsed.port > 65535):
            return None

        # Rebuild cleaned URL without scheme
        result = f"[{hostname}]" if is_ipv6 else hostname
        if parsed.port:
            result += f":{parsed.port}"
        if parsed.path and parsed.path != '/':
            result += parsed.path
        if parsed.query:
            result += f"?{parsed.query}"
        if parsed.fragment:
            result += f"#{parsed.fragment}"

        return result or None

    except Exception:
        return None
