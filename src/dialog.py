# dialog.py

import os
import re
import random
from .log import log

class Command:
    # properties
    children: list = list()
    parent = None
    level: int = 0
    arguement: str
    response: str
    command_has_vars: bool = False

    # constructor
    def __init__(self, lvl, arguement: str, response: str, setVariable, getVariableValue):
        self.level = lvl
        self.arguement = arguement
        self.response = response
        self.setVariable = setVariable
        self.getVariableValue = getVariableValue
        if re.search("_", self.arguement):
            self.command_has_vars = True

    # return None if it does not match
    # returns the response string if there is a match
    def matches(self, cmd: str):
        # is the command a variable
        result = re.match(r'~([\w]+)', self.arguement)
        if result is not None:
            var_name = result.groups()[0]
            var_value = self.getVariableValue(var_name)
            if var_value is not None:
                if isinstance(var_value, str):
                    return self.responseString()
                elif isinstance(var_value, list) and cmd in var_value:
                    return self.responseString()
        if self.command_has_vars is False:
            if self.arguement == cmd:
                return self.responseString()
            else:
                return None
        # command has variables, so check them
        temp_command_re = self.arguement.replace('_', '([\w]+)')
        cmd_var_result = re.match(temp_command_re, cmd)
        if cmd_var_result is not None:
            response_var_result = re.search(r'\$([\w]+)', self.response)
            cmd_vars = cmd_var_result.groups()
            response_vars = response_var_result.groups()
            for index, i in enumerate(response_vars):
                self.setVariable(i, cmd_vars[index])
            return self.responseString()
        else:
            return None

    def responseString(self):
        response_str = self.response

        result = re.search(r'~([\w]+)', response_str)
        if result is not None:
            var_name = result.groups()[0]
            var_value = self.getVariableValue(var_name)
            # print(type(var_value))
            # response_str = self.getVariableValue(var_name)
            if isinstance(var_value, str):
                response_str = var_value
            elif isinstance(var_value, list):
                random_number = random.randint(0, len(var_value)-1)
                response_str = var_value[random_number]


        # is multi-valued response?
        result = re.search(r'\[.*\]', response_str)
        if result is not None:
            response_str = response_str.strip('[]')
            values = list()
            while True:
                result = re.match(r'([a-zA-Z]+)', response_str)
                if result is None:
                    result = re.match(r'"([a-zA-Z\s]+)"', response_str)
                if result is None:
                    break
                span = result.span()
                values.append(result.groups()[0])
                response_str = response_str[span[1]:].strip()
                if len(response_str) < 1:
                    break
            random_number = random.randint(0, len(values)-1)
            response_str = values[random_number]


        # parse variables
        result_items = re.finditer(r'\$([\w]+)', response_str)
        if result_items is not None:
            for result in result_items:
                var_value = self.getVariableValue(result.groups()[0])
                response_str = response_str.replace(result.group(), var_value)


        return response_str

class Variable:
    # properties
    name: str
    value: any
    multi_value: bool = False

    # constructor
    def __init__(self, name, value):
        self.name = name
        self.value = value
        # check if variable is a multi-value
        if re.search(r'\[.*\]', self.value) is not None:
            self.value = self.value.strip('[]')
            self.multi_value = True
            self.parseMulitValues()

    def parseMulitValues(self):
        values = list()
        while True:
            result = re.match(r'([a-zA-Z]+)', self.value)
            if result is None:
                result = re.match(r'"([a-zA-Z\s]+)"', self.value)
            if result is None:
                break
            span = result.span()
            values.append(result.groups()[0])
            self.value = self.value[span[1]:].strip()
            if len(self.value) < 1:
                break
        self.value = values

    def getValue(self):
        return self.value

class Dialog:

    lines: list = list()
    commands: list = list()
    commands_hierarchy: dict = dict()
    active_command : Command = None
    variables: dict = dict()

    def __init__(self, file: str = 'dialog.txt'):
        self.readFile(file)
        self.parseInstructions()
        self.buildCommandHierarchy()

    def __str__(self):
        txt = ""
        # txt += f"Lines: {self.lines}"
        txt += 'Commands:\n'
        for cmd in self.commands:
            txt += f" - Level: {cmd.level}, Command: {cmd.arguement}, response: {cmd.response}, Num Children: {len(cmd.children)}\n"
        txt += 'Variables:\n'
        for v in self.variables.values():
            txt += f' - Name: "{v.name}", Value: {v.value}\n'
        return txt

    def run(self):
        while True:
            user_input = input(' > ')
            self.handleInput(user_input)

    def handleInput(self, input_cmd):
        result = None
        if self.active_command is not None:
            for cmd in self.active_command.children:
                result = cmd.matches(input_cmd)
                if result is not None:
                    if len(cmd.children) > 0:
                        self.active_command = cmd
                    break
        if result is None:
            for key, cmd in self.commands_hierarchy.items():
                result = cmd.matches(input_cmd)
                if result is not None:
                    if len(cmd.children) > 0:
                        self.active_command = cmd
                    else:
                        self.active_command = None
                    break
        if result is None:
            log.error('Invalid input: "%s"', input_cmd)
        else:
            print(result)

    def readFile(self, file: str):
        if os.path.exists(file):
            with open(file, 'r') as file:
                self.lines = file.readlines()
            # clean lines by stripping whitespace
            for index, line in enumerate(self.lines):
                self.lines[index] = str(line).strip()
            cleaned_lines = list()
            for line in self.lines:
                comment_search = re.search('#', line)
                if comment_search is None:
                    cleaned_lines.append(line)
                    continue
                else:
                    span = comment_search.span()
                    if span[0] == 0:
                        continue
                    line = line[ : span[0]].strip()
                    if len(line) > 0:
                        cleaned_lines.append(line)
            self.lines = cleaned_lines
        else:
            log.critical('Unable to open "%s"', file)

    def setVariable(self, name, value):
        var = Variable(name, value)
        self.variables[var.name] = var

    def getVariableValue(self, name):
        if name not in self.variables:
            return None
        var = self.variables[name]
        return var.getValue()

    def parseInstructions(self):
        if len(self.lines) < 1:
            return
        last_command: Command = None
        for line in self.lines:
            # parse environment variable
            if self.parseLineEnvironmentVariable(line): continue
            self.parseLineCommand(line)

    # parse environment variables - (i.e. take the form "~{var}:[params...]") - Example: ~greetings: [hello howdy "hi there"]
    def parseLineEnvironmentVariable(self, line):
        result = re.search(r'~([\w]+)\s*:\s*(.+)', line)
        if result is None: return False
        groups = result.groups()
        var_name = groups[0]
        var_value = groups[1]
        self.setVariable(var_name, var_value)
        return True

    def parseLineCommand(self, line):
        result = re.search(r'(u\d*)\s*:\s*\(([\w\s~]+)\)\s*:\s*(.+)', line)
        if result is None:
            log.error('Invalid Command: %s', line)
            return
        # get the regular expression result groups
        groups = result.groups()

        # command components
        command_level = groups[0]
        command_arg = groups[1]
        command_response = groups[2]

        # get command_level integer
        command_level_result = re.search(r'[u](\d+)', command_level)
        if command_level_result is None:
            command_level = 0
        else:
            cmd_level_span = command_level_result.span()
            command_level = int(command_level[cmd_level_span[0]+1: cmd_level_span[1]])

        # # create a new command
        command = Command(command_level, command_arg, command_response, getattr(self, 'setVariable'), getattr(self, 'getVariableValue'))

        self.commands.append(command)

    def buildCommandHierarchy(self):
        for index, item in enumerate(self.commands):
            self.commands[index].children = list()
            cmd: Command = self.commands[index]
            if cmd.level == 0:
                self.commands_hierarchy[cmd.arguement] = cmd
            else:
                parent_index = index
                parent_command : Command = self.commands[parent_index]
                while parent_command.level >= cmd.level:
                    parent_command = self.commands[parent_index]
                    parent_index -= 1
                parent_command.children.append(cmd)
                cmd.parent = parent_command

# END
