import shutil
import os
import requests
import json
import requests
from pprint import pprint
import requests
from _utils  import user_select
from threading import Timer


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


def get_browse_history():
    """
    return a list of working directories for current session
    """
    try:
        url = "http://localhost:4040/api/requests/http?limit=50"
        res = requests.get(url)
        j = res.json()
        reqs = j['requests']
        uniq_dirs = []
        sreqs = [req['request']['headers'].get('Referer',[None])[0] for req in reqs]
        for urls in sreqs:
            if urls not in uniq_dirs and urls is not None and "?folder=" in urls:
                uniq_dirs.append(urls)
        uniq_dirs = [urls.split("/?folder=")[1] for urls in uniq_dirs]
        if len(uniq_dirs) > 0:
            print("these work dirs will be saved")
            print(uniq_dirs)
            # save dirs to cache
            from ..._utils import global_status, run_bash
            cache_folder_path = global_status.get("cache_folder_path", None)
            vscode_history = []
            if cache_folder_path:
                vscode_history_path = os.path.join(cache_folder_path, "vscode_history.json")
                if os.path.exists(vscode_history_path):
                    try:
                        vscode_history = json.load(open(vscode_history_path))
                    except:
                        vscode_history = []
                vscode_history = uniq_dirs + vscode_history
                try:
                    with open(vscode_history_path, 'w') as f:
                        json.dump(vscode_history, f)
                        print("browsing history cached...")
                except:
                    print("error in caching browsing history")

        else:
            print("empty dirs.")
    except Exception as e:
        print("error in getting history:" + str(e))


timer = None

def start_timer(func):
    global timer
    print("get history")
    func()
    timer = Timer(20.0, start_timer,[func])
    timer.start()



def start_vscode_loop():
    from pyngrok import ngrok
    from ..._utils import global_status, run_bash
    port = global_status.get("port", 8050)
    vs_commd = f"./code-server-3.5.0-linux-x86_64/bin/code-server --port {port} --auth none"
    try:
        # s.enter(5, 1, do_something, (s,))
        # s.run(blocking=False)
        cache_folder_path = global_status.get("cache_folder_path", None)
        if cache_folder_path:
            t = Timer(20.0, start_timer, [get_browse_history])
            t.start()
        else:
            print("cache is disabled.")
        print("start running code-server")
        run_bash(vs_commd)
    except KeyboardInterrupt:
        # get_browse_history() # get history # TODO: error here!
        ngrok.kill()
    except Exception as e:
        print("error:" + str(e))
    finally:
        if timer is not None:
            timer.cancel()
