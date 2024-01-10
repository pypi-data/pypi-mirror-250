import argparse
import os
from os.path import expanduser
import subprocess

# ファイルのバージョン
FILE_VERSION = "1.0"

class VersionHandler:
    def display_version(self):
        print(f'ファイルのバージョン: {FILE_VERSION}')
