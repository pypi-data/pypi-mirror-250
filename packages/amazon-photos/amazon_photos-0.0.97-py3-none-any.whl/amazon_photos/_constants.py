import logging

MAX_TRASH_BATCH = 50  # max nodes to batch into trash request
MAX_PURGE_BATCH = 50  # max nodes to batch into purge (delete) request
MAX_DOWNLOAD_BATCH = 1200  # max nodes to batch into zip file for download
MAX_NODES = 9999  # this is a real limit, not a large arbitrary number
MAX_LIMIT = 200  # max number of nodes to return in a single request
MAX_NODE_OFFSETS = [i * MAX_LIMIT for i in range(49)] + [MAX_NODES - MAX_LIMIT]
AP_DATE_FMT = "%Y-%m-%dT%H:%M:%S.000Z"  # ISO 8601 with timezone offset

Black = '\x1b[30m'
Red = '\x1b[31m'
Green = '\x1b[32m'
Yellow = '\x1b[33m'
Blue = '\x1b[34m'
Magenta = '\x1b[35m'
Cyan = '\x1b[36m'
White = '\x1b[37m'
Reset = '\x1b[0m'

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s.%(msecs)03d [%(levelname)s] :: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': 'log.log',
            'mode': 'a'
        },
        'console_warning': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'formatter': 'standard'
        },
        'console_info': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'filters': ['info_only']
        }
    },
    'filters': {
        'info_only': {
            '()': lambda: lambda record: record.levelno == logging.INFO
        }
    },
    'loggers': {
        'my_logger': {
            'handlers': ['file', 'console_warning', 'console_info'],
            'level': 'DEBUG'
        }
    }
}

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Safari/605.1.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.",
]

NORTH_AMERICA_TLD_MAP = {
    "ca": "Canada",
    "com": "United States",
}

EUROPEAN_TLD_MAP = {
    "at": "Austria",
    "be": "Belgium",
    "bg": "Bulgaria",
    "hr": "Croatia",
    "ch": "Switzerland",  # todo
    "cy": "Cyprus",
    "cz": "Czech Republic",
    "dk": "Denmark",
    "ee": "Estonia",
    "fi": "Finland",
    "fr": "France",
    "de": "Germany",
    "gr": "Greece",
    "hu": "Hungary",
    "is": "Iceland",  # todo
    "ie": "Ireland",
    "it": "Italy",
    "li": "Liechtenstein",  # todo
    "lv": "Latvia",
    "lt": "Lithuania",
    "lu": "Luxembourg",
    "mt": "Malta",
    "no": "Norway",  # todo
    "nl": "Netherlands",
    "pl": "Poland",
    "pt": "Portugal",
    "ro": "Romania",
    "sk": "Slovakia",
    "si": "Slovenia",
    "es": "Spain",
    "se": "Sweden",
    "uk": "United Kingdom",
}
