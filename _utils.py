from google.colab import drive
import os
import json
import requests
import shutil
import subprocess
import sys
from tqdm.notebook import tqdm


global_status = {
    "cache_folder_name": ".colabvs_cache",
    "token_json": "token.json"
}

class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def user_select(question, options):
    print(f"{Bcolors.BOLD}[?] {question} {Bcolors.ENDC}")
    assert len(options) > 1, "length of options must be greater than 1."
    for idx, op in enumerate(options):
        print(f"{idx + 1})\t{op}")
    while 1:
        try:
            print(f"{Bcolors.BOLD}input your option number({Bcolors.OKBLUE}1-{len(options)}{Bcolors.ENDC}){Bcolors.ENDC}:")
            choice = int(input(""))
            if not (1 <= choice <= len(options)):
                raise Exception("")
            else:
                break
        except:
            print(f"{Bcolors.FAIL}only numbers (1-{len(options)}) are acceptable.{Bcolors.ENDC}")
    return choice



def cprint(content, silent = False):
    if silent:
        return
    print(content)

def run_bash(bash):
    subprocess.call(bash, shell = True)

def get_drive_name(mount_path = '/content/drive'):
    global global_status
    drive_folders = os.listdir('/content/drive')
    drive_folders = [d for d in drive_folders if not d.startswith(".") and os.path.isdir(f'/content/drive/{d}')]
    assert len(drive_folders) > 0, "No available drive found."
    if len(drive_folders) == 1:
        drive_name = drive_folders[0]
    else:
        question = "Which drive do you plan to use (as workspace)?"
        choice = user_select(question, drive_folders)
        drive_name = drive_folders[choice]
    global_status['work_drive'] = drive_name
    return drive_name



def try_mount_drive(mount_path = '/content/drive', force_remount = False, drive_name = None):
    global global_status
    global_status['workspace_drive'] = None
    if force_remount:
        drive.mount(mount_path,force_remount=True)
        cprint(f"Google drive is re-mounted on {mount_path}")

    if not os.path.exists(mount_path):
        drive.mount(mount_path)
        # cprint(f"Google drive is mounted on {mount_path}")
    
    if drive_name is None:
        drive_name = get_drive_name()
    cprint(f"Drive is mounted and {Bcolors.OKGREEN}{Bcolors.BOLD}{drive_name}{Bcolors.ENDC}{Bcolors.ENDC} is used as workspace.")
    global_status['workspace_drive'] = f"{mount_path}/{drive_name}"
    return drive_name

def setting_workspace_drive(mount_path = '/content/drive', silent = True):
    global global_status
    if global_status.get('workspace_drive', None):
        global_status['workspace_drive'] = None
    if os.path.exists(mount_path):
        drive_name = global_status.get('workspace_drive', None)
        if drive_name:
            global_status['workspace_drive'] = f"{mount_path}/{drive_name}"
        else:
            drive_name = get_drive_name(mount_path)
            global_status['workspace_drive'] = f"{mount_path}/{drive_name}"
    cprint(f"workspace drive = {global_status['workspace_drive']}", silent)
    
def input_user_token():
    question = "Input your ngrok token in your workspace:"
    print(f"")
    token_input = ""
    while(1):
        token_input = input(question).strip()
        while len(token_input) == 0:
            print("Empty token is not allowed.")
            token_input = input(question).strip()
        save_confirm = input("Are you sure the token is correct?[y/N]").strip().lower()
        if save_confirm == "y":
            break
        else:
            question = "Re-input your token in your workspace:"
    return token_input


def load_token(regenerate_token = False):
    global global_status
    workspace_drive = global_status.get("workspace_drive", "/content")
    cache_folder_name = global_status["cache_folder_name"]
    token_json_name = global_status["token_json"]
    token_json = f"{workspace_drive}/{cache_folder_name}/{token_json_name}"

    if regenerate_token and os.path.exists(token_json):
        os.remove(token_json)

    if os.path.exists(token_json):
        try:
            token = json.load(open(token_json))['token']
            print(f"using token {token}")
        except:
            print(f"{Bcolors.BOLD} token file damaged. Regenerate a new token file. {Bcolors.ENDC}")
            token_input = input_user_token()
            with open(token_json, 'w') as f:
                json.dump({'token':token_input}, f)
                print(f"{Bcolors.OKBLUE}Your token is saved at {token_json}{Bcolors.ENDC}")
                token = token_input
    else:
        token_input = input_user_token()
        with open(token_json, 'w') as f:
            json.dump({'token':token_input}, f)
            print(f"{Bcolors.OKBLUE}Your token is saved at {token_json}{Bcolors.ENDC}")
            token = token_input
    global_status['token'] = token
    run_bash(f"ngrok authtoken {token}")
    return token

def setting_up_caches(silent = False):
    global global_status
    workspace_drive = global_status.get("workspace_drive", "/content")
    cache_folder_name = global_status["cache_folder_name"]
    cache_folder_path = os.path.join(workspace_drive, cache_folder_name)
    global_status["cache_folder_path"] = cache_folder_path

    if not os.path.exists(cache_folder_path):
        os.makedirs(cache_folder_path)
        cprint(f"cache folder created at {cache_folder_path}", silent)
    else:
        cprint(f"cache folder {cache_folder_path} found", silent)


def start_ngrok():
    from pyngrok import ngrok
    ngrok.kill()
    run_bash
    port = global_status.get("port", 8050)
    public_url = ngrok.connect(port)
    workspace_drive = global_status.get("workspace_drive", "/content")
    open_folder = f"?folder={workspace_drive}"
    url = public_url.public_url.replace('http','https') + open_folder
    return url

def run_app(desc = "open app at: {}", func = None):
    url = start_ngrok()
    print(desc.format(url))
    func()

def install_pip_dependencies(silent = True):
    commands = ['pip install pyngrok==5.0.5', 'pip install pylint']
    lib_names = ['pyngrok', 'pylint']
    cmds_to_install = []
    cprint("resolving dependencies", silent)
    output = subprocess.check_output("pip freeze", shell = True).decode(sys.stdout.encoding)
    installed_libs = [f.split("==")[0] for f in output.split("\n")]
    for idx,lib in enumerate(lib_names):
        if lib not in installed_libs:
            cmds_to_install.append(commands[idx])

    if len(cmds_to_install) > 0:
        for c in tqdm(cmds_to_install):
            run_bash(c)