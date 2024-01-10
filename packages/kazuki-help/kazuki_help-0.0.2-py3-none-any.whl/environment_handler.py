import subprocess
import argparse
from os.path import expanduser
import os

class EnvironmentHandler:
    def initialize_environment(self):
        print('プログラムと環境を初期化およびセットアップします.')
        subprocess.call(["mkdir", expanduser("~")+"/.kazuki_help"])