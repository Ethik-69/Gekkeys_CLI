#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
import time
import json
import requests
import configparser
from docopt import docopt
from threading import Thread


class Geekkeys(Thread):
    def __init__(self, datas, called_from):
        # SUPER to call __init__ from Thread
        Thread.__init__(self)

        self.config_file = "geekkeys.conf"
        self.datas = datas

        if called_from == "term":
            self.clean_datas()
            self.datas['data'] = json.loads(self.datas['data'])

        self.parsing_config()

        self.action = self.datas['action']

        self.url = self.datas['url']
        del self.datas['url']

        self.stage = self.datas['stage']
        del self.datas['stage']

        self.output = []
        self.token = None
        self.headers = None
        self.resource_path = None
        self.request_result = None

    def run(self):
        #self.conn_request()  # TODO: Commented For Debug UnComment Later
        self.action_request()

        if self.action == 'get-key':
            self.save_key_file()

    def clean_datas(self):
        """
        Parse the datas
        "Why ?" You'll say !
        datas given via terminale are like that:
        {
             '--action': 'create-key',
             '--username': 'Jean_Jacques',
             '--password': 'FuckingGreatPassWord',
             '--stage': 'dev',
             '--data': "{'group': 'gekko', 'key_name': 'aws_key', 'key_content': 'ssh_key_file'}",
             '--url': 'xxxxxxxx'
        }
        So, this need to be cleaned
        """

        # TODO: May be deleted
        # Del all entry with None as value
        #filtered = {key: value for key, value in self.datas.items() if value is not None}
        #self.replace_dict(filtered)

        # Del "--" at the start of keys
        filtered = {key[2:] if key[:2] == "--" else key: value for key, value in self.datas.items()}
        self.replace_dict(filtered)

        # TODO: May be deleted
        # Del "<" at the start and ">" at the end of the keys
        #filtered = {key[1:-1] if key[:1] == "<" else key: value for key, value in self.datas.items()}
        #self.replace_dict(filtered)

    def replace_dict(self, filtered):
        """
        Replace old dict (datas) with the filtered one
        params: Dict
        """
        self.datas.clear()
        self.datas.update(filtered)

    def parsing_config(self):
        """
        Get config from config_file
        """

        if not os.path.isfile(self.config_file):
            print("[X] ERROR: Config file does not exist")
            exit()

        config = configparser.ConfigParser()
        config.read(self.config_file)

        for field in config.items('MAIN'):
            if self.datas[field[0]] is None:
                self.datas[field[0]] = field[1]

    def conn_request(self):
        """
        Send request to the given url
        Sent data:
        {
            "action": "get-key",
            "username": "haingo@gekko.fr",
            "password": "mypass",
            "data": {"group": "Harem", "key_name": "virgin0"}
        }
        """
        # Stringify datas Dict
        data = json.dumps(self.datas)

        # Create the request header
        self.headers = {'Content-type': 'application/json'}
        # in headers: 'x-api-key': 'key'  # TODO: dev/mvp tmp

        self.resource_path = self.stage + '/auth'

        # Create complete url then send the request
        formated_url = '{}/{}'.format(self.url, self.resource_path)
        self.request_result = requests.post(formated_url, data=data, headers=self.headers)

        # Get the conn token from the request result
        self.token = json.loads(self.request_result.text)

        if "errorMessage" in self.token.keys():
            print("[X] Error: %s" % self.token["errorMessage"])
            exit()

    def action_request(self):
        """
        Send request to the given url
        """
        # Action entry is useless for this request so del it.
        del self.datas['action']

        # Add conn token/usrid to data dict
        #self.datas['token'] = self.token['token']  # TODO: Commented For Debug UnComment Later
        #self.datas['usrid'] = self.token['usrid']  # TODO: Commented For Debug UnComment Later

        # Stringify datas Dict
        data = json.dumps(self.datas)

        # Create the request header
        self.headers = {'Content-type': 'application/json'}
        # in headers: 'x-api-key': 'key'  # TODO: dev/mvp tmp

        # ex: ['get', 'key']
        action, resource = self.action.split('-')

        self.resource_path = self.stage + '/' + resource

        # Create complete url then send the request
        formated_url = '{}/{}'.format(self.url, self.resource_path)

        method_switch_case = {"create": requests.post,
                              "update": requests.post,  # ?
                              "get": requests.get,
                              "delete": requests.delete
        }

        try:
            self.request_result = method_switch_case[action](formated_url, data=data, headers=self.headers)
        except Exception as e:
            print("[X] ERROR: %s" % e)

        self.show_request_result()  # TODO: Dev 'll be deleted

        self.request_result = json.loads(self.request_result.text)

        if "error" in self.request_result.keys():
            print("[X] Error: %s" % self.request_result["error"])
            exit()

    def save_key_file(self):
        try:
            with open(self.request_result['key_name'], 'x+') as file:
                file.write(self.request_result['key_content'])
            print('[*] File created')

            os.system('mv ' + self.request_result['key_name'] + ' ~/.ssh/' + self.request_result['key_name'])
            print('[*] File moved to ~/.ssh/')

        except Exception as e:
            print('[X] ERROR: %s' % e)

    def show_request_result(self):
        self.output.append("[.] Status Code: %s" % self.request_result.status_code)
        #self.output.append("[.] Headers: %s" % self.request_result.headers)
        #self.output.append("[.] Encoding: %s" % self.request_result.encoding)
        self.output.append("[.] Text/Data: %s" % self.request_result.text)
        #self.output.append("[.] Json: %s" % self.request_result.json)


if __name__ == '__main__':
    start_time = time.time()

    # Docstring for docopt
    help = """
    Geekkeys

    Usage:
      geekkeys.py (--action <action>)
                  [--stage <stage>]
                  [--username <username>]
                  (--password <password>)
                  (--data <data>)
                  [--url <url>]

    Options:
      -h --help                         Show this !
      -a --action=<action>              What to do (show/create/update/del_user/key/group)
      -s --stage=<stage>                Stage on which you want to do the action (Dev/PreProd/Prod...)
      -u --username=<username>          Username.
      -p --password=<password>          Password.
      -d --data=<data>                  Data to send.
      -U --url=<url>                    API's url.

    Example for data:
        '{"group": "gekko", "key_name": "aws_key", "key_content": "ssh_key_content"}'

    Your can put Stage, Username and Url in geekkeys.conf
    """

    arguments = docopt(help)

    # Instantiation of main object with "term" when launched with the terminal
    app = Geekkeys(arguments, "term")

    # Launch the thread
    app.start()

    loader = ["[      ]",
              "[=     ]",
              "[==    ]",
              "[===   ]",
              "[ ===  ]",
              "[  === ]",
              "[   ===]",
              "[    ==]",
              "[     =]"]
    i = 0

    # Wait until the thread is finished
    while app.is_alive():
        time.sleep(0.1)
        if i >= len(loader):
            i = 0

        text = "\r%s" % loader[i]
        # print the beautiful "spinner"
        sys.stdout.write(text)
        sys.stdout.flush()
        i += 1

    # Clean the last "spinner" step from screen
    sys.stdout.write("\r")
    sys.stdout.flush()

    for out in app.output:
        print(out)

    exec_time = time.time() - start_time
    print("[*] Script End")
    print("[*] Execution time: %s second" % round(exec_time, 3))

# Create requi**.txt pipreqs path
