#!/usr/bin/python3

import argparse
from version_handler import VersionHandler
from environment_handler import EnvironmentHandler
from file_lister import FileLister
from command_describer import CommandDescriber
from git_handler import GitHandler
from configuration_handler import ConfigurationHandler
from create_file import CreateFile
from delete_file import DeleteFile
from edit_file_with_emacs import EditFileWithEmacs

# ファイルのバージョン
FILE_VERSION = "1.0"

def main():
    parser = argparse.ArgumentParser(description='サブコマンドとファイル操作を持つスクリプト')

    subparsers = parser.add_subparsers(title='サブコマンド', dest='subcommand')

    # サブコマンド 'new': ファイルを作成する
    parser_new = subparsers.add_parser('new', help='新しいファイルを作成')
    parser_new.add_argument('filename', help='作成するファイルの名前')

    # サブコマンド 'delete': ファイルを削除する
    parser_delete = subparsers.add_parser('delete', help='指定したファイルを削除')
    parser_delete.add_argument('filename', help='削除するファイルの名前')

    # サブコマンド 'edit': ファイルをEmacsで編集する
    parser_edit = subparsers.add_parser('edit', help='指定したファイルをEmacsで編集')
    parser_edit.add_argument('filename', help='編集するファイルの名前')

    # サブコマンド 'version': ファイルのバージョンを表示
    parser_version = subparsers.add_parser('version', help='ファイルのバージョンを表示')

    # サブコマンド 'init': プログラムおよび環境を初期化およびセットアップ
    parser_init = subparsers.add_parser('init', help='プログラムおよび環境を初期化およびセットアップ')

    # サブコマンド 'list': ファイルを一覧表示（再帰的）
    parser_list = subparsers.add_parser('list', help='ファイルを一覧表示')
    #parser_list.add_argument('directory', nargs='?', default=".", help='内容を表示するディレクトリ（デフォルトはカレントディレクトリ）')
    parser_list.add_argument('filename', nargs='?', default=".", help='内容を表示するディレクトリ（デフォルトはカレントディレクトリ）')
    #parser_list.add_argument('filename', nargs='?', help='表示するファイルの名前')
    parser_list.add_argument('section', nargs='?', help='表示するセクションの名前')


    # サブコマンド 'command': コマンドの説明を表示
    parser_command = subparsers.add_parser('command', help='コマンドの説明を表示')

    # サブコマンド 'git': Git操作
    parser_git = subparsers.add_parser('git', help='Gitを使用した操作')
    parser_git.add_argument('git_command', choices=['pull', 'push'], help='Gitコマンドを選択 (pull, push)')

    # サブコマンド 'set': 設定を行う
    parser_set = subparsers.add_parser('set', help='設定を行う')
    parser_set.add_argument('editor', help='エディターを設定')
    parser_set.add_argument('ext', help='ファイル拡張子を設定')

    # 新しいサブコマンド 'hello': コマンドラインに指定した文字列を表示
    parser_hello = subparsers.add_parser('hello', help='指定した文字列を表示')

    args = parser.parse_args()

    # サブコマンドごとに処理を分岐
    if args.subcommand == 'new':
        file_handler = CreateFile()
        file_handler.create_file(args.filename)

    elif args.subcommand == 'delete':
        file_handler = DeleteFile()
        file_handler.delete_file(args.filename)

    elif args.subcommand == 'edit':
        file_handler = EditFileWithEmacs()
        file_handler.edit_file_with_emacs(args.filename)

    elif args.subcommand == 'version':
        version_handler = VersionHandler()
        version_handler.display_version()

    elif args.subcommand == 'init':
        env_handler = EnvironmentHandler()
        env_handler.initialize_environment()

    elif args.subcommand == 'list':
        lister = FileLister()
        if args.filename and args.section:
            lister.list_file_contents_section(args.filename, args.section)
        else:
            lister.list_files(args.filename)

    elif args.subcommand == 'command':
        command_describer = CommandDescriber()
        command_describer.display_command_description()
    
    elif args.subcommand == 'git':
        git_handler = GitHandler()
        git_handler.git_operation(args.git_command)

    elif args.subcommand == 'set':
        config_handler = ConfigurationHandler()
        config_handler.set_configuration(args.editor, args.ext)

    elif args.subcommand == 'hello':
        # 'hello' サブコマンドの場合、ユーザーにメッセージを入力させて表示
        user_input = input('任意の文字列: ')
        print(f'{user_input}\nHello {user_input}')

'''
if __name__ == "__main__":
    main()
'''