import shutil
import os
import requests
import json
import requests
from pprint import pprint
import requests
from _utils  import user_select


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
    except Exception as e:
        print("error in getting history:" + str(e))


import sched, time
s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
    print("Doing stuff...")
    # do your stuff
    s.enter(5, 1, do_something, (sc,))




def start_vscode_loop():
    from pyngrok import ngrok
    from ..._utils import global_status, run_bash
    port = global_status.get("port", 8050)
    vs_commd = f"./code-server-3.5.0-linux-x86_64/bin/code-server --port {port} --auth none"
    try:
        s.enter(5, 1, do_something, (s,))
        s.run(blocking=True)
        print("start running code-server")
        run_bash(vs_commd)
    except KeyboardInterrupt:
        # get_browse_history() # get history # TODO: error here!
        ngrok.kill()
