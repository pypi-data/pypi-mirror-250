import os
import argparse
from os.path import expanduser
import subprocess

class FileLister:
    def list_files(self, directory="."):
        if directory==".":
            target_path = os.path.join(expanduser("~"), ".kazuki_help", directory)
        else:
            target_path = expanduser("~") + "/.kazuki_help/" + directory + ".org"

        if not os.path.exists(target_path):
            print(f'{target_path} が存在しません.')
            return

        if os.path.isdir(target_path):
            files = [f'ファイル: {file}' for file in os.listdir(target_path) if file.endswith('.org')]
            if not files:
                print(f'{target_path} ディレクトリには .org ファイルが存在しません.')
                return

            print("\n".join(files))
        elif os.path.isfile(target_path) and target_path.endswith('.org'):
            print(f'ファイル: {directory} のセクションの内容:')
            self._display_section_content(target_path)
        else:
            print(f'{target_path} は .org ファイルまたはディレクトリではありません.')

    def _display_section_content(self, filename, section=None):
        try:
            #print(filename, section)
            with open(filename, 'r') as file:
                content = file.read()
                lines = content.split('\n')
                in_section = False
                array = []
                for line in lines:
                    if line.startswith('* '):
                        if section is None:
                            print('- ' + line[2:])
                        else:
                            if section in line.strip('* '):
                                in_section = True
                            else:
                                in_section = False
                    
                    if in_section:
                        array.append(line)
                
                for line in array:
                    print(line)

        except Exception as e:
            print(f'ファイル内容の取得中にエラーが発生しました: {e}')

    def list_file_contents_section(self, filename, section):
        if section:
            #target_path = os.path.join(os.getcwd(), ".kazuki_help", filename)
            target_path = expanduser("~")+"/.kazuki_help/"+filename+".org"
            self._display_section_content(target_path, section)
        else:
            self._display_whole_file(filename)

