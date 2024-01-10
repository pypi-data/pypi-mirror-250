import subprocess

class GitHandler:
    def git_operation(self, git_command):
        try:
            subprocess.run(['git', git_command])
            print(f'Git コマンド "{git_command}" を実行しました。')
        except Exception as e:
            print(f'Git コマンドの実行中にエラーが発生しました: {e}')