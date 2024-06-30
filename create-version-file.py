#
# Copyright (c) Andreas Finkler and contributors. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

# https://pypi.org/project/pyinstaller-versionfile/

import pyinstaller_versionfile

pyinstaller_versionfile.create_versionfile(
    output_file="version.txt",
    version="1.0.0.0",
    company_name="Lunarixus",
    file_description="Download PSN Update Packages",
    internal_name="PyPSNUpdateDownloader",
    legal_copyright="© 2024 Lunarixus. All rights reserved.",
    original_filename="PyPSNUpdateDownloader.exe",
    product_name="PyPSNUpdateDownloader",
    translations=[0, 1200]
)