import argparse
import os
from os.path import expanduser
import subprocess

class EditFileWithEmacs:
    def edit_file_with_emacs(self, filename):
        if os.path.exists(expanduser("~")+"/.kazuki_help/"+filename+".org"):
            try:
                # subprocess を使って Emacs を呼び出し、指定したファイルを編集
                subprocess.run(['emacs', expanduser("~")+"/.kazuki_help/"+filename+".org"])
                print(f'{filename} ファイルを Emacs で編集しました。')
            except Exception as e:
                print(f'Emacs でファイルを編集中にエラーが発生しました: {e}')
        else:
            print(f'{filename} は存在しません。編集できません。')