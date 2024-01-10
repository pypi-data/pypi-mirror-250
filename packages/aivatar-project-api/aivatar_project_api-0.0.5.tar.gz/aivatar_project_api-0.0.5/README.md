aivatar_project_api
=========

## Quick Start

```python
from aivatar_project_api import AivProjectAPI

# todo: get token from Login module
aiv_project_api = AivProjectAPI(token, terminal_type, business_type)

# get project items
p_items = aiv_project_api.get_project_items()
for item in p_items:
    print(item.project_id, item.project_name, item.experiment)

# check validation of local record
aiv_project_api.is_project_record_valid()

# get current project info
pid = aiv_project_api.current_project_id                # int
pname = aiv_project_api.current_project_name            # string
experiment = aiv_project_api.current_project_experiment # 0/1

# set project id
aiv_project_api.current_project_id = 123

# jump to page
aiv_project_api.jump_to_guide_page()
aiv_project_api.jump_to_manager_page()
```


## Customized Config

```python
from aivatar_project_api import AivProjectAPI

# read config
config = aiv_project_api.config()
config.get_projects_query_url()
config.get_guide_page_url()
config.get_manager_page_url()

# change config path
"""A config file should look like:
{
    "host": "",
    "route": "",
    "guide_page_url": "",
    "manager_page_url": ""
}
"""
path = "xxx.json"
aiv_project_api.change_network_config_path(path)
```

## Use LoginBackend to Popup Page
```python
# need arthub_login_widgets >= 0.5.5
# LoginBackend should have attributes with "is_login", "popup_admin", "popup_introduction"

from arthub_login_widgets import LoginBackend
login_backend = LoginBackend(YourTerminalType, YourBusinessType)
aiv_project_api.set_login_backend(login_backend)

# Then if login_backend.is_login(), will:
# call login_backend.popup_introduction() when call jump_to_guide_page()
# call login_backend.popup_admin() when call jump_to_manager_page()
# else: use webbrowser
```

## Test

```python
from aivatar_project_api import AivProjectAPI

# todo: get token from Login module in test env
aiv_project_api = AivProjectAPI(token, terminal_type, business_type, is_test=True)
```

### Tips: Get Token in Test Env
- Way 1
    -  Get from `LoginWidgets` or `LoginBackend` in **dev_mode**，see [arthub_login_widgets](https://git.woa.com/arthub/arthub_login_widgets)
- Way 2
    1. Make sure you can login https://arthub-test.woa.com/login by your email account
    
        a. Click "forget password" if failed at step-1 and set a new password

        b. Contact v_yuliylyu if failed at step-1.a, maybe you're not in the white list of test env.

    2. Run code below
```python
import json
import random
import requests
import string
import time

URL = "https://arthub-service-test.woa.com/account/account/openapi/v3/core/login"
RANDOM_SOURCE = string.ascii_lowercase + string.digits

def get_random_str(num=12):
   return ''.join(random.choice(RANDOM_SOURCE) for i in range(num))


def query_token(email, password, terminal_type, business_type):
    token = ""
    body = {"account_name":email,
        "account_type":"email",
        "password":password,
        "rand_str":"",
        "ticket":"",
        "current_time":int(time.time()),
        "nounce":get_random_str(),
        "oauth_type":"password",
        "terminal_type":terminal_type,
        "business_type":business_type,
        "login_type": "arthub_token"
        }
    res = requests.post(URL, json=body)
    # print(res.content)
    content = json.loads(res.content)
    code = content.get("code", -1)
    if code != 0:
        print("error:", content.get("error", "no error msg"))
    else:
        result = content.get("result", {})
        if result:
            token = result.get("arthub_token", "")
            print("token:", token)
        else:
            print("no result")
    return token
      
      
if __name__ == "__main__":
    # for example
    token = query_token("lavenderyao@tencent.com", "******", "dcc", "AutoLUV")
```