import os
import sys
from .template import Template


class Processor:

  @staticmethod
  def save_text(text, filename, append=False):
    if filename == '-':
      with sys.stdout as file:
        file.write(text)

    else:
      wstr = 'a' if filename is not None and os.path.exists(
          filename) and os.path.isfile(filename) and append is True else 'w'
      with open(filename, wstr, encoding='utf8') as file:
        file.write(text)

  @classmethod
  def process(cls, template, output, data=None):
    # You can use a standard Jinja2 Template object or our builtin Template-object
    _template = template.template if isinstance(
        template, Template) else template

    result = _template.render(data)
    cls.save_text(result, output)
