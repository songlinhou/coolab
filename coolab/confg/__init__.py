import json

__confg = {
    "pip-libs":[
        {"name": "pyngrok", "install":"pip install pyngrok==5.0.5"},
        {"name": "pylint", "install":"pip install pylint"},
    ],
    "apps":[
        {"name": "localtunnel", "install": "npm install -g localtunnel", "bin": "lt"},
        {"name": "filebrowser", "install": "curl -fsSL https://raw.githubusercontent.com/filebrowser/get/master/get.sh | bash", "bin": "filebrowser"}
    ]
}

def get_config():
    # TODO: load local config jsons
    return __confg