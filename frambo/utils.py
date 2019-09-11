# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from contextlib import contextmanager
import jinja2
from logging import getLogger
import os
import subprocess

logger = getLogger(__name__)


def run_cmd(cmd, return_output=False, ignore_error=False, shell=False, **kwargs):
    """
    Run provided command on host system using the same user as invoked this code.
    Raises subprocess.CalledProcessError if it fails.

    :param cmd: list or str
    :param return_output: bool, return output of the command
    :param ignore_error: bool, do not fail in case nonzero return code
    :param shell: bool, run command in shell
    :param kwargs: pass keyword arguments to subprocess.check_* functions; for more info,
            please check `help(subprocess.Popen)`
    :return: None or str
    """
    logger.debug("command: %r", cmd)
    try:
        if return_output:
            return subprocess.check_output(
                cmd,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                shell=shell,
                **kwargs,
            )
        else:
            return subprocess.check_call(cmd, shell=shell, **kwargs)
    except subprocess.CalledProcessError as cpe:
        if ignore_error:
            if return_output:
                return cpe.output
            else:
                return cpe.returncode
        else:
            logger.error(f"failed with code {cpe.returncode} and output:\n{cpe.output}")
            raise cpe


@contextmanager
def cwd(target):
    """
    Manage cwd in a pushd/popd fashion.

    Usage:
    with cwd(tmpdir):
      do something in tmpdir
    """
    curdir = os.getcwd()
    os.chdir(target)
    try:
        yield
    finally:
        os.chdir(curdir)


def text_from_template(template_dir, template_filename, template_data):
    """
    Create text based on template in path template_dir/template_filename
    :param template_dir: string, directory containing templates
    :param template_filename: template for text in jinja
    :param template_data: dict, data for substitution in template
    :return: string
    """

    if not os.path.exists(os.path.join(template_dir, template_filename)):
        raise FileNotFoundError("Path to template not found.")

    template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template_filename)
    output_text = template.render(template_data=template_data)
    logger.debug("Text from template created:")
    logger.debug(output_text)

    return output_text
