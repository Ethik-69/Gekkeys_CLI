#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
import time
import json
import requests
from docopt import docopt
from threading import Thread


class Gekkeys(Thread):
    def __init__(self, arguments, called_from):
        """
        arguments structure:

        {
            'action': 'create-key',
            'data': "{
                'group': 'gekko',
                'key_name': 'aws_key',
                'key_content': '-----BEGIN RSA PRIVATE KEY-----.....'
                }",
            'password': 'FuckingGreatPassWord',
            'stage': 'dev',
            'url': 'https://#################.com',
            'username': 'Jean_Jacques',
        }

        data is the result of:
            json.dumps(python Dict / json)
        """
        # SUPER to call __init__ from Thread
        Thread.__init__(self)

        self.arguments = arguments

        if called_from == "term":
            self.clean_arguments()
            self.arguments['data'] = json.loads(self.arguments['data'])

        self.action = self.arguments['action']

        self.url = self.arguments['url']
        del self.arguments['url']

        self.stage = self.arguments['stage']
        del self.arguments['stage']

        self.headers = None
        self.resource_path = None
        self.request_result = None
        self.token = None
        self.output = []

    def run(self):
        self.conn_request()
        self.action_request()
        self.show_request_result()

    def get_args(self):
        """
        Debug function, will be deleted
        """
        print('------------------------')
        print(self.arguments)
        print('------------------------')

    def clean_arguments(self):
        """
        Parse the arguments
        "Why ?" You'll say !
        Arguments given via terminale are like that:
        {
             '--action': 'create-key',
             '--data': "{'group': 'gekko', 'key_name': 'aws_key', 'key_content': 'ssh_key_file'}",
             '--password': 'FuckingGreatPassWord',
             '--stage': 'dev',
             '--url': 'xxxxxxxx',
             '--username': 'Jean_Jacques',
             '<action>': None,
             '<data>': None,
             '<password>': None,
             '<stage>': None,
             '<url>': None,
             '<username>': None
        }
        So, this need to be cleaned
        """

        # Del all entry with None as value
        filtered = {key: value for key, value in self.arguments.items() if value is not None}
        self.replace_dict(filtered)

        # Del "--" at the start of keys
        filtered = {key[2:] if key[:2] == "--" else key: value for key, value in self.arguments.items()}
        self.replace_dict(filtered)

        # Del "<" at the start and ">" at the end of the keys
        filtered = {key[1:-1] if key[:1] == "<" else key: value for key, value in self.arguments.items()}
        self.replace_dict(filtered)

    def replace_dict(self, filtered):
        """
        Replace old dict (arguments) with the filtered one
        params: Dict
        """
        self.arguments.clear()
        self.arguments.update(filtered)

    def conn_request(self):
        """
        Send request to the given url
        Sent data:
        {
            'action': 'create-key',
            'password': 'FuckingGreatPassWord',
            'username': 'Jean_Jacques'
        }
        """
        # Stringify arguments Dict
        data = json.dumps(self.arguments)

        # Create the request header
        self.headers = {'Content-type': 'application/json'}
        # in headers: 'x-api-key': 'key'  # TODO: dev/mvp tmp

        self.resource_path = self.stage + '/auth'  # TODO: maybe'll change, we'll see, no one know...

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
        Sent data:
        {
            'data': "{
                'group': 'gekko',
                'key_name': 'aws_key',
                'key_content': '-----BEGIN RSA PRIVATE KEY-----.....'
                }",
            'password': 'FuckingGreatPassWord',
            'username': 'Jean_Jacques',
            'token': 'xxxxxxxxxxxxxxxxx',
            'usrid': 'xxxxxxxxxxxxxxxxx'
        }
        """
        # Action entry is useless for this request so del it.
        del self.arguments['action']

        # Add conn token the data
        self.arguments['token'] = self.token['token']
        self.arguments['usrid'] = self.token['usrid']

        # Stringify arguments Dict
        data = json.dumps(self.arguments)
        #print("[.] Data: %s" % data)
        # Create the request header
        self.headers = {'Content-type': 'application/json'}
        # in headers: 'x-api-key': 'key'  # TODO: dev/mvp tmp

        self.resource_path = self.stage + '/' + self.action

        # Create complete url then send the request
        formated_url = '{}/{}'.format(self.url, self.resource_path)
        #print("[.] Url: %s" % formated_url)
        self.request_result = requests.post(formated_url, data=data, headers=self.headers)

    def show_request_result(self):
        self.output.append("[.] Status Code: %s" % self.request_result.status_code)
        #self.output.append("[.] Headers: %s" % self.request_result.headers)
        #self.output.append("[.] Encoding: %s" % self.request_result.encoding)
        self.output.append("[.] Text/Data: %s" % self.request_result.text)
        #self.output.append("[.] Json: %s" % self.request_result.json)


if __name__ == '__main__':

    # Docstring for docopt
    help = """
    Alohomora

    Usage:
      alohomora.py (--action <action> | <action>)
                   (--stage <stage> | <stage>)
                   (--username <username> | <username>)
                   (--password <password> | <password>)
                   (--data <data> | <data>)
                   (--url <url> | <url>)

    Options:
      -h --help                         Show this !
      -a --action=<action>              What to do (show/create/update/del_user/key/group)
      -s --stage=<stage>                Stage on which you want to do the action (Dev/PreProd/Prod...)
      -n --username=<username>          Username.
      -p --password=<password>          Password.
      -d --data=<data>                  Data to send.
      -u --url=<url>                    API's url.

    Example for data:
        '{"group": "gekko", "key_name": "aws_key", "key_content": "ssh_key_content"}'
    """

    arguments = docopt(help)

    # Instantiation of main object with "term" when launched with the terminal
    app = Gekkeys(arguments, "term")

    # Launch the thread
    app.start()

    loader = ["[=     ]",
              "[==    ]",
              "[===   ]",
              "[ ===  ]",
              "[  === ]",
              "[   ===]",
              "[    ==]",
              "[     =]",
              "[      ]"]
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

# Create requi**.txt pipreqs path
# HOWTO: run:
# EXAMPLE  python alohomora.py -a create-user -s dev -n haingo@gekko.fr -p mypass -d '{"username": "ethan", "password": "mypass", "role": "admin", "env": "gekko"}' -u https://x2z4uxl2jd.execute-api.eu-west-1.amazonaws.com
