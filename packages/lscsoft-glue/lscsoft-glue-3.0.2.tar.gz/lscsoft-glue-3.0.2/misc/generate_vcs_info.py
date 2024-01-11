# generate_vcs_info.py - determine git version info
#
# Based on generateGitID.sh by Reinhard Prix
#
# Copyright (C) 2009,2010, Adam Mercer <adam.mercer@ligo.org>
# Copyright (C) 2009,2010, Nickolas Fotopoulos <nvf@gravity.phys.uwm.edu>
# Copyright (C) 2008,2009, John T. Whelan <john.whelan@ligo.org>
# Copyright (C) 2008, Reinhard Prix <reinhard.ligo.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import subprocess
import time

__author__ = 'Adam Mercer <adam.mercer@ligo.org>'


# version info class
class git_info(object):
    def __init__(self):
        self.id = None
        self.date = None
        self.branch = None
        self.tag = None
        self.author = None
        self.committer = None
        self.status = None


def check_output(command):
    """Wrapper for subprocess.check_output that discards stderr.
    """
    try:
        return subprocess.check_output(
            command,
            encoding="utf-8",
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError as exc:
        raise RuntimeError from exc


def in_git_repository():
    """
    Return True if git is available and we are in a git repository; else
    return False.

    NB: Unfortunately there is a magic number without any documentation to back
    it up. It turns out that git status returns non-zero exit codes for all
    sorts of success conditions, but I cannot find any documentation of them.
    128 was determined empirically. I sure hope that it's portable.
    """
    try:
        return subprocess.call(
            ('git', 'status'),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ) != 128
    except OSError:
        # git is not installed
        return False


def generate_git_version_info():
    if not in_git_repository():
        raise RuntimeError(
            'not in git checkout or cannot find git executable',
        )

    # info object
    info = git_info()

    # determine basic info about the commit
    # %H -- full git hash id
    # %ct -- commit time
    # %an, %ae -- author name, email
    # %cn, %ce -- committer name, email
    (
        git_id,
        git_udate,
        git_author_name,
        git_author_email,
        git_committer_name,
        git_committer_email,
    ) = check_output((
        'git',
        'log',
        '-1',
        '--pretty=format:%H,%ct,%an,%ae,%cn,%ce',
    )).split(",")

    git_date = time.strftime(
        '%Y-%m-%d %H:%M:%S +0000',
        time.gmtime(float(git_udate)),
    )
    git_author = '%s <%s>' % (git_author_name, git_author_email)
    git_committer = '%s <%s>' % (git_committer_name, git_committer_email)

    # determine branch
    branch_match = check_output((
        'git',
        'rev-parse',
        '--symbolic-full-name',
        'HEAD',
    ))
    if branch_match == "HEAD":
        git_branch = None
    else:
        git_branch = os.path.basename(branch_match)

    # determine tag
    try:
        git_tag = check_output((
            'git',
            'describe',
            '--exact-match',
            '--tags',
            git_id,
        ))
    except RuntimeError:
        git_tag = None

    # refresh index
    subprocess.check_call(('git', 'update-index', '-q', '--refresh'))

    # check working copy for changes
    if subprocess.call(('git', 'diff-files', '--quiet')):
        git_status = 'UNCLEAN: Modified working tree'
    elif subprocess.call((
        'git',
        'diff-index',
        '--cached',
        '--quiet',
        'HEAD',
    )):
        git_status = 'UNCLEAN: Modified index'
    else:
        git_status = 'CLEAN: All modifications committed'

    # determine version strings
    info.id = git_id
    info.date = git_date
    info.branch = git_branch
    info.tag = git_tag
    info.author = git_author
    info.committer = git_committer
    info.status = git_status

    return info
