class ConfigurationHandler:
    def set_configuration(self, editor, ext):
        try:
            with open('config.txt', 'w') as config_file:
                config_file.write(f'Editor: {editor}\n')
                config_file.write(f'Extension: {ext}\n')
            print('設定を保存しました.')
        except Exception as e:
            print(f'設定の保存中にエラーが発生しました: {e}')
