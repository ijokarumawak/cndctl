import logging
import os
import sys
import json
import requests
import base64
import datetime
import jwt

def read_token(env_file_path):
    token_file = open(env_file_path, "r")
    token = token_file.read()
    token_file.close()

    return token

def check_dk_env(env_file_path):
    if os.path.isfile(env_file_path):
        token = read_token(env_file_path=env_file_path)
    else:
        print("The '{}' not found. Please, generate token using 'cndctl dk update'".format(env_file_path))
        return False
    
    token_payload = jwt.decode(token, options={"verify_signature": False})
    token_expire = datetime.datetime.fromtimestamp(token_payload['exp'])

    if datetime.datetime.now() < token_expire:
        return True
    else:
        print("The token is expired. Please update using `cndctl dk update`")
        return False

# cndctl dk update
def update(DK_AUTH0_URL, DK_CLIENT_ID, DK_CLIENT_SECRETS):
    logging.debug("dreamkast_update()")
    env_file_path = ".dk.env"

    if check_dk_env(env_file_path=env_file_path):
        print("token not expired")
        sys.exit()

    req_url = "https://" + DK_AUTH0_URL + "/oauth/token"
    headers = {
        "content-type": "application/json"
    }
    data = {
        "client_id":"",
        "client_secret":"",
        "audience":"https://event.cloudnativedays.jp/",
        "grant_type":"client_credentials"
    }
    data['client_id'] = DK_CLIENT_ID
    data['client_secret'] = DK_CLIENT_SECRETS

    res = requests.post(req_url, headers=headers, data=json.dumps(data))
    res_payload = res.json()
    print("token update successfully ({})".format(res_payload))

    token_file = open(".dk.env", "w")
    token_file.write(res_payload['access_token'])
    token_file.close()

def talks():
    logging.debug("dreamkast_update()")

    # res = requests.put 

def onair():
    logging.debug("dreamkast_onair()")