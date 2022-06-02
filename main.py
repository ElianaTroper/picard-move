PLUGIN_NAME = "Move"
PLUGIN_AUTHOR = "Eliana Troper"
PLUGIN_DESCRIPTION = "This plugin moves files with specified endings"
PLUGIN_VERSION = '0.1'
PLUGIN_API_VERSIONS = ['2.2']
PLUGIN_LICENSE = "GPL-2.0-or-later"
PLUGIN_LICENSE_URL = "https://www.gnu.org/licenses/gpl-2.0.html"

import types
from os.path import isfile
from picard import log
from picard.file import register_file_post_load_processor
from picard.util.filenaming import (
    get_available_filename,
    move_ensure_casing,
    replace_extension,
)


def _move_or_rename(old_filename, new_filename, file_type):
    mod_filename = old_filename + file_type
    if not isfile(mod_filename):
        return
    mod_new_filename = new_filename + file_type
    mod_new_filename = get_available_filename(mod_new_filename, mod_filename)
    log.debug('Moving ' + file_type + ' file %r => %r', mod_filename, mod_new_filename)
    move_ensure_casing(mod_filename, mod_new_filename)


def new_move(self, old_filename, new_filename, config):
    _move_or_rename(old_filename, new_filename, '.asd')
    self._old_move_additional_files(old_filename, new_filename, config)


def move_other_file(file):
    file._old_move_additional_files = file._move_additional_files
    file._move_additional_files = types.MethodType(new_move, file)


register_file_post_load_processor(move_other_file)
