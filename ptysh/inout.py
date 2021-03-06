# -*- coding: utf-8 -*-

"""
Module responsible for handling input and output in ptysh.
"""

import sys
from os import path
from os import listdir
from yaml import load

from structure import Status
from structure import Singleton
from structure import OrderedDictYAMLLoader

HOST_NAME_FILE_PATH = "/etc/hostname"
CONFIGURE_FILE_PATH = path.join(path.abspath(path.dirname(__file__)), "../ptysh.d/")

class IoControl(Singleton):

    def get_input_command(self):
        """
        Displays a prompt and receives a command from the user.
        """
        prompt = self.get_prompt()
        return input(prompt) if sys.version_info >= (3,0) else raw_input(prompt)

    def get_host_name(self):
        """
        Set the name to be used at the prompt displayed on the screen.
        Get the value from the "/ etc / hostname" file.
        If there is no file, PTYSH is displayed.
        """
        if not path.exists(HOST_NAME_FILE_PATH):
            return "PTYSH"      # default prompt name

        with open(HOST_NAME_FILE_PATH, "rb") as f:
            return f.readline().strip().decode("utf-8")

    def get_prompt(self):
        """
        Set the prompt that appears on the screen.
        Indicates the name of the current node.
        """
        if Status().module_depth > Status().ROOT_DEPTH:
            location = "(%s)" % Status().current_node
        else:
            location = ""

        prompt_delimiter = "#" if Status().login else ">"
        prompt = "%s%s%s " % (self.get_host_name(), location, prompt_delimiter)
        return prompt

    def print_welcome_message(self):
        message = "Hello, This is Python Teletype Shell.\n"
        message += "COPYRIGHT 2017 KyeongSeob Sim. ALL RIGHTS RESERVED.\n"
        self.print_message(message)

    def print_cmd_list(self, command, description):
        self.print_message("  %s%s" % (command.ljust(30), description))

    def print_cmd_usage(self, usage):
        self.print_message("  %s" % usage)

    def print_message(self, message):
        print (message)

    def get_modules_conf(self):
        if not path.isdir(CONFIGURE_FILE_PATH):
            return

        conf_list = []
        for conf_file in listdir(CONFIGURE_FILE_PATH):
            file = ("%s%s" % (CONFIGURE_FILE_PATH, conf_file))
            with open(file, "rb") as f:
                conf_list.append(load(f, OrderedDictYAMLLoader))

        return conf_list
