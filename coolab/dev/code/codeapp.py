import shutil
import os
import requests

def download_vscode(silent = True):
    from ..._utils import global_status, cprint, setting_up_caches, run_bash
    global global_status

    if "cache_folder_path" not in global_status.keys():
        setting_up_caches()
    
    cache_folder_path = global_status['cache_folder_path']
    url = 'https://github.com/cdr/code-server/releases/download/v3.5.0/code-server-3.5.0-linux-x86_64.tar.gz'
    save_loc = os.path.join(cache_folder_path, os.path.basename(url))
    if not os.path.exists(save_loc):
        cprint("downloading vscode to cache folder", silent)
        r = requests.get(url, allow_redirects=True)
        open(save_loc, 'wb').write(r.content)
        cprint("downloaded", silent)
    else:
        cprint("found cached downloads", silent)
    shutil.copy(save_loc, "/content")
    run_bash("tar -xf code-server-3.5.0-linux-x86_64.tar.gz")


def start_vscode_loop():
    from pyngrok import ngrok
    from ..._utils import global_status, run_bash
    port = global_status.get("port", 8050)
    vs_commd = f"./code-server-3.5.0-linux-x86_64/bin/code-server --port {port} --auth none"
    try:
        run_bash(vs_commd)
    except KeyboardInterrupt:
        ngrok.kill()
    print("vscode has been terminated.")