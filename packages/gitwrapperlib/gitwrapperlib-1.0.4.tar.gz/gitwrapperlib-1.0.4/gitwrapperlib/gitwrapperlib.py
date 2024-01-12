#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: gitwrapperlib.py
#
# Copyright 2018 Costas Tyfoxylos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for gitwrapperlib.

.. _Google Python Style Guide:
   https://google.github.io/styleguide/pyguide.html

"""

import logging
import sys
import re
try:
    import sh
except ImportError:
    # fallback: emulate the sh API with pbs
    import pbs

    class Sh:
        """
        Overloading pbs to look like sh.

        https://stackoverflow.com/questions/28618906/porting-sh-1-11-based-code-to-windows
        """

        def __getattr__(self, attr):
            return pbs.Command(attr)
    sh = Sh()
from .gitwrapperlibexceptions import (ExecutableNotFound,
                                      BranchNotFound,
                                      RemoteOriginError)

__author__ = '''Costas Tyfoxylos <costas.tyf@gmail.com>'''
__docformat__ = '''google'''
__date__ = '''02-01-2018'''
__copyright__ = '''Copyright 2018, Costas Tyfoxylos'''
__credits__ = ["Costas Tyfoxylos"]
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<costas.tyf@gmail.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


# This is the main prefix used for logging
LOGGER_BASENAME = '''gitwrapperlib'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class Git:
    """Models the git command and constructs some extra helper methods."""

    passthrough_methods = ('init', 'pull')
    argument_methods = ('add', 'clone', 'push')

    def __init__(self, tty_out=True):
        logger_name = f'{LOGGER_BASENAME}.{self.__class__.__name__}'
        self._logger = logging.getLogger(logger_name)
        self._git = self._get_command()
        self._git = self._git.bake(_tty_out=tty_out)

    @staticmethod
    def _get_command():
        if sys.platform in ('win32', 'cygwin'):
            try:
                sh.git()
            except WindowsError:  # pylint: disable=undefined-variable
                raise ExecutableNotFound from None
            except pbs.ErrorReturnCode_1:
                git = sh.git
        else:
            try:
                git = sh.Command('git')
            except sh.CommandNotFound:
                raise ExecutableNotFound from None
        return git

    def __getattr__(self, name):  # pylint: disable=inconsistent-return-statements
        if name in self.passthrough_methods:
            return getattr(self._git, name)
        if name in self.argument_methods:
            def wrapper(*args, **kwargs):  # noqa
                return getattr(self._git, name)(*args, **kwargs)
            return wrapper

    def remove(self, path):
        """Removes a path with force."""
        self._git.rm('-rf', path)

    def add_forced(self, path):
        """Adds a path with force."""
        self._git.add('-f', path)

    def commit(self, message, *args):
        """Commits."""
        self._git.commit('-m', message, *args)

    def add_remote_origin(self, url):
        """Adds the remote origin."""
        self._git.remote('add', 'origin', url)

    def push_default(self):
        """Pushes to the default branch."""
        branch = self.get_default_branch()
        self._git.push('origin', branch)

    def push_force_default(self):
        """Force pushes to the default branch."""
        branch = self.get_default_branch()
        self._git.push('origin', branch, '--force')

    def push_branch(self, branch):
        """Pushes to a branch."""
        self._git.push('origin', branch)

    def push_force_branch(self, branch):
        """Force pushes to a branch."""
        self._git.push('origin', branch, '--force')

    def get_branches(self):
        """Returns a list of the branches."""
        return [self._sanitize(branch)
                for branch in self._git.branch(color="never").splitlines()]

    @staticmethod
    def _sanitize(value):
        if value.startswith('*'):
            value = value.split()[1]
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        value = ansi_escape.sub('', value.strip())
        return value

    def get_current_branch(self):
        """Returns the currently active branch."""
        return next((self._sanitize(branch)
                     for branch in self._git.branch(color="never").splitlines()
                     if branch.startswith('*')),
                    None)

    def get_default_branch(self):
        """Returns the remote default branch."""
        show_origin_text = str(self._git.remote('show', 'origin'))
        try:
            branch = re.search(r'HEAD branch: (\S+)', show_origin_text).group(1)
        except (IndexError, AttributeError):
            raise RemoteOriginError(f'git remote show origin command did not respond as expected, '
                                    f'received :{show_origin_text}') from None
        if branch == '(unknown)':
            message = 'Failed to detect default remote branch, please check your remote settings.'
            self._logger.error(message)
            raise BranchNotFound(message)
        return branch

    def create_branch(self, name):
        """Creates a branch."""
        self._git.branch(name)

    def remove_branch(self, name):
        """Removes a branch."""
        self._git.branch('-d', name)

    def switch_branch(self, name):
        """Switches to a branch."""
        self._git.checkout(name, "--")

    def list_tags(self):
        """Lists existing tags."""
        return self._git.tag().splitlines()

    def add_tag(self, value):
        """Tag with provided value."""
        self._git.tag(value)

    def delete_tag(self, value):
        """Delete the tag provided."""
        self._git.tag('-d', value)

    def create_patch(self, from_tag, to_tag):
        """Create a patch between tags."""
        return str(self._git.diff(f'{from_tag}..{to_tag}', _tty_out=False))
