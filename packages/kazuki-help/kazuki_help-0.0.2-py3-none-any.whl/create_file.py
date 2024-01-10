import argparse
import os
from os.path import expanduser
import subprocess

class CreateFile:
    def create_file(self, filename):
        try:
            #with open(filename, 'w') as file:
            #    print(f'{filename} ファイルを作成しました。')
            subprocess.call(["touch", expanduser("~")+"/.kazuki_help/"+filename+".org"])
            print(f'{filename} ファイルを作成しました。')
        except Exception as e:
            print(f'ファイルの作成中にエラーが発生しました: {e}')
