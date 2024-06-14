import socket
import re

# List of WHOIS servers for different TLDs
whois_servers = {
     "ac": "whois.nic.ac",  # Ascension Island
    "ae": "whois.nic.ae",  # United Arab Emirates
    "aero": "whois.aero",
    "af": "whois.nic.af",  # Afghanistan
    "ag": "whois.nic.ag",  # Antigua And Barbuda
    "ai": "whois.ai",  # Anguilla
    "al": "whois.ripe.net",  # Albania
    "am": "whois.amnic.net",  # Armenia
    "arpa": "whois.iana.org",
    "as": "whois.nic.as",  # American Samoa
    "asia": "whois.nic.asia",
    "at": "whois.nic.at",  # Austria
    "au": "whois.aunic.net",  # Australia
    "ax": "whois.ax",  # Aland Islands
    "az": "whois.ripe.net",  # Azerbaijan
    "be": "whois.dns.be",  # Belgium
    "bg": "whois.register.bg",  # Bulgaria
    "bi": "whois.nic.bi",  # Burundi
    "biz": "whois.biz",
    "bj": "whois.nic.bj",  # Benin
    "bn": "whois.bn",  # Brunei Darussalam
    "bo": "whois.nic.bo",  # Bolivia
    "br": "whois.registro.br",  # Brazil
    "bt": "whois.netnames.net",  # Bhutan
    "by": "whois.cctld.by",  # Belarus
    "bz": "whois.belizenic.bz",  # Belize
    "ca": "whois.cira.ca",  # Canada
    "cat": "whois.cat",  # Spain
    "cc": "whois.nic.cc",  # Cocos (Keeling) Islands
    "cd": "whois.nic.cd",  # Congo, The Democratic Republic Of The
    "ch": "whois.nic.ch",  # Switzerland
    "ci": "whois.nic.ci",  # Cote d'Ivoire
    "ck": "whois.nic.ck",  # Cook Islands
    "cl": "whois.nic.cl",  # Chile
    "cn": "whois.cnnic.net.cn",  # China
    "co": "whois.nic.co",  # Colombia
    "com": "whois.verisign-grs.com",
    "coop": "whois.nic.coop",
    "cx": "whois.nic.cx",  # Christmas Island
    "cz": "whois.nic.cz",  # Czech Republic
    "de": "whois.denic.de",  # Germany
    "dk": "whois.dk-hostmaster.dk",  # Denmark
    "dm": "whois.nic.dm",  # Dominica
    "dz": "whois.nic.dz",  # Algeria
    "ec": "whois.nic.ec",  # Ecuador
    "edu": "whois.educause.edu",
    "ee": "whois.eenet.ee",  # Estonia
    "eg": "whois.ripe.net",  # Egypt
    "es": "whois.nic.es",  # Spain
    "eu": "whois.eu",
    "fi": "whois.ficora.fi",  # Finland
    "fo": "whois.nic.fo",  # Faroe Islands
    "fr": "whois.nic.fr",  # France
    "gd": "whois.nic.gd",  # Grenada
    "gg": "whois.gg",  # Guernsey
    "gi": "whois2.afilias-grs.net",  # Gibraltar
    "gl": "whois.nic.gl",  # Greenland (Denmark)
    "gov": "whois.nic.gov",
    "gs": "whois.nic.gs",  # South Georgia And The South Sandwich Islands
    "gy": "whois.registry.gy",  # Guyana
    "hk": "whois.hkirc.hk",  # Hong Kong
    "hn": "whois.nic.hn",  # Honduras
    "hr": "whois.dns.hr",  # Croatia
    "ht": "whois.nic.ht",  # Haiti
    "hu": "whois.nic.hu",  # Hungary
    "ie": "whois.domainregistry.ie",  # Ireland
    "id": "whois.id",
    "il": "whois.isoc.org.il",  # Israel
    "im": "whois.nic.im",  # Isle of Man
    "in": "whois.inregistry.net",  # India
    "info": "whois.afilias.net",
    "int": "whois.iana.org",
    "io": "whois.nic.io",  # British Indian Ocean Territory
    "iq": "whois.cmc.iq",  # Iraq
    "ir": "whois.nic.ir",  # Iran, Islamic Republic Of
    "is": "whois.isnic.is",  # Iceland
    "it": "whois.nic.it",  # Italy
    "je": "whois.je",  # Jersey
    "jobs": "jobswhois.verisign-grs.com",
    "jp": "whois.jprs.jp",  # Japan
    "ke": "whois.kenic.or.ke",  # Kenya
    "kg": "www.domain.kg",  # Kyrgyzstan
    "ki": "whois.nic.ki",  # Kiribati
    "kr": "whois.kr",  # Korea, Republic Of
    "kz": "whois.nic.kz",  # Kazakhstan
    "la": "whois.nic.la",  # Lao People's Democratic Republic
    "li": "whois.nic.li",  # Liechtenstein
    "lt": "whois.domreg.lt",  # Lithuania
    "lu": "whois.dns.lu",  # Luxembourg
    "lv": "whois.nic.lv",  # Latvia
    "ly": "whois.nic.ly",  # Libya
    "ma": "whois.iam.net.ma",  # Morocco
    "md": "whois.nic.md",  # Moldova
    "me": "whois.nic.me",  # Montenegro
    "mg": "whois.nic.mg",  # Madagascar
    "mil": "whois.nic.mil",
    "mk": "whois.rnids.rs",  # Serbia
    "ml": "whois.dot.ml",  # Mali
    "mn": "whois.nic.mn",  # Mongolia
    "mo": "whois.monic.mo",  # Macao
    "mobi": "whois.dotmobiregistry.net",
    "ms": "whois.nic.ms",  # Montserrat
    "mu": "whois.nic.mu",  # Mauritius
    "museum": "whois.museum",
    "mx": "whois.mx",  # Mexico
    "my": "whois.domainregistry.my",  # Malaysia
    "na": "whois.na-nic.com.na",  # Namibia
    "name": "whois.nic.name",
    "nc": "whois.nc",  # New Caledonia
    "net": "whois.verisign-grs.net",
    "nf": "whois.nic.nf",  # Norfolk Island
    "ng": "whois.nic.net.ng",  # Nigeria
    "nl": "whois.domain-registry.nl",  # Netherlands
    "no": "whois.norid.no",  # Norway
    "nu": "whois.nic.nu",  # Niue
    "nz": "whois.srs.net.nz",  # New Zealand
    "om": "whois.registry.om",  # Oman
    "org": "whois.pir.org",
    "pe": "kero.yachay.pe",  # Peru
    "pf": "whois.registry.pf",  # French Polynesia
    "pl": "whois.dns.pl",  # Poland
    "pm": "whois.nic.pm",  # Saint Pierre and Miquelon (France)
    "post": "whois.dotpostregistry.net",
    "pr": "whois.nic.pr",  # Puerto Rico
    "pro": "whois.dotproregistry.net",
    "pt": "whois.dns.pt",  # Portugal
    "pw": "whois.nic.pw",  # Palau
    "qa": "whois.registry.qa",  # Qatar
    "re": "whois.nic.re",  # Reunion (France)
     "ro": "whois.rotld.ro",  # Romania
    "rs": "whois.rnids.rs",  # Serbia
    "ru": "whois.tcinet.ru",  # Russian Federation
    "rw": None,  # Rwanda - no WHOIS server assigned
    "sa": "whois.nic.net.sa",  # Saudi Arabia
    "sb": "whois.nic.net.sb",  # Solomon Islands
    "sc": "whois2.afilias-grs.net",  # Seychelles
    "sd": None,  # Sudan - no WHOIS server assigned
    "se": "whois.iis.se",  # Sweden
    "sg": "whois.sgnic.sg",  # Singapore
    "sh": "whois.nic.sh",  # Saint Helena
    "si": "whois.arnes.si",  # Slovenia
    "sk": "whois.sk-nic.sk",  # Slovakia
    "sl": None,  # Sierra Leone - no WHOIS server assigned
    "sm": "whois.nic.sm",  # San Marino
    "sn": "whois.nic.sn",  # Senegal
    "so": "whois.nic.so",  # Somalia
    "sr": None,  # Suriname - no WHOIS server assigned
    "st": "whois.nic.st",  # Sao Tome And Principe
    "su": "whois.tcinet.ru",  # Russian Federation
    "sv": None,  # El Salvador - no WHOIS server assigned
    "sx": "whois.sx",  # Sint Maarten (Dutch part)
    "sy": "whois.tld.sy",  # Syrian Arab Republic
    "sz": None,  # Swaziland - no WHOIS server assigned
    "tc": "whois.meridiantld.net",  # Turks And Caicos Islands
    "td": None,  # Chad - no WHOIS server assigned
    "tel": "whois.nic.tel",
    "tf": "whois.nic.tf",  # French Southern Territories
    "tg": None,  # Togo - no WHOIS server assigned
    "th": "whois.thnic.co.th",  # Thailand
    "tj": "whois.nic.tj",  # Tajikistan
    "tk": "whois.dot.tk",  # Tokelau
    "tl": "whois.nic.tl",  # Timor-leste
    "tm": "whois.nic.tm",  # Turkmenistan
    "tn": "whois.ati.tn",  # Tunisia
    "to": "whois.tonic.to",  # Tonga
    "tp": "whois.nic.tl",  # Timor-leste
    "tr": "whois.trabis.gov.tr",  # Turkey
    "travel": "whois.nic.travel",
    "tt": None,  # Trinidad And Tobago - no WHOIS server assigned
    "tv": "tvwhois.verisign-grs.com",  # Tuvalu
    "tw": "whois.twnic.net.tw",  # Taiwan
    "tz": "whois.tznic.or.tz",  # Tanzania, United Republic Of
    "ua": "whois.ua",  # Ukraine
    "ug": "whois.co.ug",  # Uganda
    "uk": "whois.nic.uk",  # United Kingdom
    "us": "whois.nic.us",  # United States
    "uy": "whois.nic.org.uy",  # Uruguay
    "uz": "whois.cctld.uz",  # Uzbekistan
    "va": None,  # Holy See (Vatican City State) - no WHOIS server assigned
    "vc": "whois2.afilias-grs.net",  # Saint Vincent And The Grenadines
    "ve": "whois.nic.ve",  # Venezuela
    "vg": "whois.adamsnames.tc",  # Virgin Islands, British
    "vi": None,  # Virgin Islands, US - no WHOIS server assigned
    "vn": None,  # Viet Nam - no WHOIS server assigned
    "vu": None,  # Vanuatu - no WHOIS server assigned
    "wf": "whois.nic.wf",  # Wallis and Futuna
    "ws": "whois.website.ws",  # Samoa
    "xxx": "whois.nic.xxx",
    "ye": None,  # Yemen - no WHOIS server assigned
    "yt": "whois.nic.yt",  # Mayotte
    "yu": "whois.ripe.net",  # Former Yugoslavia
    "app": "whois.nic.google",
    "social": "whois.nic.social",
    "xyz": "whois.nic.xyz"
}

def lookup_domain(domain):
    domain_parts = domain.split(".")
    tld = domain_parts[-1].lower()
    whois_server = whois_servers.get(tld)
    if not whois_server:
        return f"Error: No appropriate Whois server found for {domain} domain!"
    
    result = query_whois_server(whois_server, domain)
    if not result:
        return f"Error: No results retrieved from {whois_server} server for {domain} domain!"
    else:
        while "Whois Server:" in result:
            secondary_server_match = re.search(r"Whois Server: (.*)", result)
            if secondary_server_match:
                secondary_server = secondary_server_match.group(1).strip()
                result = query_whois_server(secondary_server, domain)
                whois_server = secondary_server

    # Remove the URL of the ICANN Whois Inaccuracy Complaint Form
    result = re.sub(r"URL of the ICANN Whois Inaccuracy Complaint Form:.*", "", result, flags=re.DOTALL)
    
    return f"{domain} domain lookup results from {whois_server} server:\n\n{result}"

def validate_domain(domain):
    if not re.match(r"^([-a-z0-9]{2,100})\.([a-z\.]{2,8})$", domain, re.IGNORECASE):
        return False
    return domain

def query_whois_server(whois_server, query):
    port = 43
    timeout = 10
    result = ""
    try:
        with socket.create_connection((whois_server, port), timeout) as sock:
            sock.sendall((query + "\r\n").encode("utf-8"))
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                result += data.decode("utf-8")
    except Exception as e:
        return f"Socket Error: {e}"
    
    if "error" not in result.lower() and "not allocated" not in result.lower():
        filtered_result = "\n".join([line.strip() for line in result.splitlines() if line.strip() and not line.startswith(("#", "%"))])
        return filtered_result
    return ""

# Example usage:
if __name__ == "__main__":
    domain = input("Please enter a domain name without http / https and www (e.g., example.com): ").strip()
    if validate_domain(domain):
        print(lookup_domain(domain))
    else:
        print("Invalid domain name")
