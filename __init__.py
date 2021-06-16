import os
from ._utils import user_select, try_mount_drive, setting_workspace_drive, setting_up_caches, load_token, install_dependencies, run_app

class Code(object):
    def init_env(self, mount_path = '/content/drive', regen_token = False, silent = True):
        from dev.code.codeapp import download_vscode
        if not os.path.exists(mount_path):
            choice = user_select("Mount your google drive?", ["Yes","No"])
            if choice == 1:
                try_mount_drive(mount_path)
        setting_workspace_drive(mount_path)
        setting_up_caches(silent)
        download_vscode(silent)
        load_token(regen_token)
        install_dependencies()

    def start_server(self):
        from dev.code.codeapp import start_vscode_loop
        run_app(desc="visit vscode at {}", func=start_vscode_loop)

    def run(self, mount_path = '/content/drive', regen_token = False, silent = True):
        self.init_env(mount_path, regen_token, silent)
        self.start_server()
        