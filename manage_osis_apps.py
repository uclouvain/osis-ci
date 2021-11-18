#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2021 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
import argparse
import itertools
import subprocess
from typing import List

import attr

DEFAULT_BRANCH = "dev"


parser = argparse.ArgumentParser(description="A utility to setup osis apps.")
parser.add_argument(
    "-d",
    "--default",
    help="default branch for apps",
    default=DEFAULT_BRANCH,
    type=str,
    metavar="BRANCH_NAME"
)

parser.add_argument(
    "-a",
    "--apps",
    help="precise for an app which branch to take (can be used multiple times)",
    nargs=2,
    type=str,
    action='append',
    metavar=('app', 'branch_name'),
)

args = parser.parse_args()


@attr.s(frozen=True, slots=True)
class PackageInfo:
    name = attr.ib(type=str)
    git_url = attr.ib(type=str)

    @property
    def dir_name(self) -> str:
        return self.name.replace('-', '_')


packages = [
    PackageInfo("osis_async", "https://github.com/uclouvain/osis-async.git"),
    PackageInfo("osis_document", "https://github.com/uclouvain/osis-document.git"),
    PackageInfo("osis_history", "https://github.com/uclouvain/osis-history.git"),
    PackageInfo("osis_notification", "https://github.com/uclouvain/osis-notification.git"),
    PackageInfo("osis_signature", "https://github.com/uclouvain/osis-signature.git"),
    PackageInfo("osis_mail_template", "https://github.com/uclouvain/osis-mail-template.git"),
    PackageInfo("osis_export", "https://github.com/uclouvain/osis-export.git"),
]


def install_apps(default_branch: str, apps: List[List[str]]) -> None:
    packages_name = [package.name for package in packages]

    packages_apps = [app for app in apps if app[0] in packages_name]
    module_apps = [app for app in apps if app[0] not in packages_name]

    install_modules(default_branch, module_apps)

    for package in packages_apps:
        package_info = next(
            (info for info in packages if info.name == package[0]),
            None
        )
        if package_info:
            install_package(
                package_info,
                package[1]
            )


def install_package(package_info: PackageInfo, branch_to_install: str) -> None:
    git_clone_command = [
        "git",
        "clone",
        "--single-branch",
        "-b",
        branch_to_install,
        "--depth",
        "1",
        package_info.git_url,
        package_info.dir_name
    ]

    print(" ".join(git_clone_command))

    subprocess.run(
        git_clone_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    cmd = ["pip", "install", "-e",  package_info.dir_name]

    print(" ".join(cmd))

    subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )


def install_modules(default_branch: str, apps: List[List[str]]) -> None:
    flat_apps = list(itertools.chain.from_iterable(apps))
    cmd = ["python", "manage_submodules.py", default_branch] + flat_apps

    print(" ".join(cmd))

    subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )


def main():
    install_apps(args.default, args.apps)


if __name__ == '__main__':
    main()
