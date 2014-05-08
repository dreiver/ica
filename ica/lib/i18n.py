import os

from babel import Locale, localedata
from babel.core import LOCALE_ALIASES
from pylons import config
from pylons import i18n

import ica.i18n

LOCALE_ALIASES['es'] = 'es_AR'