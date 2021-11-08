# ##############################################################################
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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
# ##############################################################################
from setuptools import setup, find_packages

setup(
    name='OSIS CI',
    version='1.0dev',
    description='Osis Continuing Integration commands',
    url='http://github.com/uclouvain/osis-ci',
    author='Université catholique de Louvain',
    author_email='O365G-team-osis-dev@groupes.uclouvain.be',
    license='AGPLv3',
    packages=find_packages(exclude=('osis_ci.tests',)),
    include_package_data=True,
    install_requires=[
        "coverage==6.1.1",
        "pycodestyle==2.4.0",
        "pylint==2.4.4",
        "diff-cover==6.4.2",
        "tblib==1.7.0",
    ],
    entry_points={
        "console_scripts": ['manage_apps=osis_ci.manage_osis_apps:main']
    }
)
