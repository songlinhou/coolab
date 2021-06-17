import os
from ._utils import user_select, try_mount_drive, setting_workspace_drive, setting_up_caches, load_token, run_app

__version__ = "1.0.0"

class Code(object):
    def init_env(self, mount_path = '/content/drive', regen_token = False, silent = True):
        from .dev.code.codeapp import download_vscode
        from ._utils import install_pip_dependencies, install_bash_dependencies
        if not os.path.exists(mount_path):
            choice = user_select("Mount your google drive?", ["Yes","No"])
            if choice == 1:
                try_mount_drive(mount_path)
        setting_workspace_drive(mount_path)
        setting_up_caches(silent)
        download_vscode(silent)
        load_token(regen_token)
        install_pip_dependencies(silent)
        install_bash_dependencies(silent)

    def start_server(self, tunnel, auto_alternative_tunnel):
        from .dev.code.codeapp import start_vscode_loop
        assert tunnel == "ngrok", "The other tunnel options are still un-stable to use. Please use ngrok for now."
        run_app(desc="visit vscode at {}", func=start_vscode_loop, tunnel=tunnel, auto_alternative_tunnel=auto_alternative_tunnel)

    def run(self, mount_path = '/content/drive', regen_token = False, tunnel = "ngrok", auto_alternative_tunnel = True,silent = True):
        self.init_env(mount_path, regen_token, silent)
        self.start_server(tunnel=tunnel, auto_alternative_tunnel=auto_alternative_tunnel)
        