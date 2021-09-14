import shutil
import os
import requests
import json
import requests
from pprint import pprint
import requests
from _utils  import user_select, cprint
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
    # run_bash("tar -xf code-server-3.5.0-linux-x86_64.tar.gz")
    run_bash("tar -xf /content/code-server-3.5.0-linux-x86_64.tar.gz -C /content/")


def get_browse_history(debug = False):
    """
    return a list of working directories for current session
    """
    def remove_duplicates(h_list, max_size = 50):
        filtered = []
        for h in h_list:
            if h not in filtered:
                filtered.append(h)
        return filtered[:max_size]

    silent = not debug
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
            cprint("these work dirs will be saved:", silent)
            cprint(uniq_dirs, silent)
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
                new_vscode_history = uniq_dirs + vscode_history
                new_vscode_history = remove_duplicates(new_vscode_history)
                cprint('new_vscode_history='+str(new_vscode_history), silent)
                try:
                    if new_vscode_history != vscode_history:
                        with open(vscode_history_path, 'w') as f:
                            json.dump(new_vscode_history, f)
                            cprint("browsing history cached...", silent)
                except:
                    cprint("error in caching browsing history", silent)

        else:
            cprint("empty dirs.", silent)
    except Exception as e:
        cprint("error in getting history:" + str(e), silent)


timer = None

def start_timer(func, debug):
    global timer
    silent = not debug
    cprint("get history", silent)
    func(debug)
    timer = Timer(20.0, start_timer,[func, debug])
    timer.start()



def start_vscode_loop(debug = False):
    from pyngrok import ngrok
    from ..._utils import global_status, run_bash
    port = global_status.get("port", 8050)
    if not os.path.exists("/content/code-server-3.5.0-linux-x86_64/bin/code-server"):
        print("error: cannot find code server file. Quit..")
        if timer is not None:
            timer.cancel()
        ngrok.kill()
        return

    vs_commd = f"/content/code-server-3.5.0-linux-x86_64/bin/code-server --port {port} --auth none"
    try:
        # s.enter(5, 1, do_something, (s,))
        # s.run(blocking=False)
        cache_folder_path = global_status.get("cache_folder_path", None)
        if cache_folder_path:
            print("browsing cache is enabled")
            t = Timer(20.0, start_timer, [get_browse_history, debug])
            t.start()
        else:
            print("browsing cache is disabled.")
        print("start running code-server")
        run_bash(vs_commd)
    except KeyboardInterrupt:
        ngrok.kill()
    except Exception as e:
        print("error:" + str(e))
    finally:
        if timer is not None:
            timer.cancel()
        ngrok.kill()
