# plugin.py

import re
import os

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from mkdocs import config
from mkdocs import utils

def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def replace_with_file_content(basepath, match, extension, delete):
    filename = os.path.abspath(os.path.join(basepath, match.group(2) + extension))
    utils.log.info("mkdocs-plugin-inline-svg: including SVG: {}".format(
        filename))
    svg = read_file(filename)
    if delete is not None:
        svg = re.sub(delete,'',svg)
    return svg

class InlineSvgPlugin(BasePlugin):

    config_scheme = (
        ('extension', config_options.Type(str, default='.svg')),
        ('delete', config_options.Type(str, default=None))
    )

    def on_config(self, config, **kwargs):
        self.extension = self.config['extension']
        self.delete = self.config['delete']
        return config

    def on_page_markdown(self, markdown, **kwargs):
        basepath = os.path.dirname(kwargs.get("page").file.abs_src_path)
        pattern = re.compile(r"!\[(.*?)\]\((.*?)" + re.escape(self.extension) + "\)", flags=re.IGNORECASE)
        markdown = re.sub(
            pattern, lambda match: replace_with_file_content(basepath, match, self.extension, self.delete), markdown
        )
        return markdown
