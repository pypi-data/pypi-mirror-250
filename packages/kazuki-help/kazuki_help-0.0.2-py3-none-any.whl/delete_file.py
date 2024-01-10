import argparse
import os
from os.path import expanduser
import subprocess

class DeleteFile:
    def delete_file(self, filename):
        if os.path.exists(expanduser("~")+"/.kazuki_help/"+filename+".org"):
            try:
                os.remove(expanduser("~")+"/.kazuki_help/"+filename+".org")
                print(f'{filename} ファイルを削除しました。')
            except Exception as e:
                print(f'ファイルの削除中にエラーが発生しました: {e}')
        else:
            print(f'{filename} は存在しません。削除できません。')
