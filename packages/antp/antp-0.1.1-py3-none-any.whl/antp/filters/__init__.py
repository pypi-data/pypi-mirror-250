from jinja2.filters import FILTERS
from .fromjson import fromjson


def set_filters():
  FILTERS['fromjson'] = fromjson
