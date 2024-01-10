import argparse
import subprocess
from os.path import expanduser
import os

class FileHandler:
    def create_file(self, filename):
        try:
            #with open(filename, 'w') as file:
            #    print(f'{filename} ファイルを作成しました。')
            subprocess.call(["touch", expanduser("~")+"/.kazuki_help/"+filename+".org"])
            print(f'{filename} ファイルを作成しました。')
        except Exception as e:
            print(f'ファイルの作成中にエラーが発生しました: {e}')

    def delete_file(self, filename):
        if os.path.exists(expanduser("~")+"/.kazuki_help/"+filename+".org"):
            try:
                os.remove(expanduser("~")+"/.kazuki_help/"+filename+".org")
                print(f'{filename} ファイルを削除しました。')
            except Exception as e:
                print(f'ファイルの削除中にエラーが発生しました: {e}')
        else:
            print(f'{filename} は存在しません。削除できません。')

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