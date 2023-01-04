from sys import argv
import os
import allpurpose.files
import time

called = input()

writing_function = False
current_function = ""
current_line = 0

variables = {}
functions = {}

def error(bruh):
    print(bruh)

def isnumberic(what):
    try:
        float(what)
        return True
    except:
        return False

def check(what):
    what = str(what).lstrip(" ")
    if variables.get(what):
        return variables[what]
    elif isnumberic(what):
        if "+" in what or "-" in what or "/" in what or "*" in what:
            return eval(what)
        else:
            return float(what)
    else:
        if what.startswith("'") or what.startswith('"'):
            return str(what).strip('"').strip("'")

    
    return "Nothing"

def debug_check(what):
    what = str(what).lstrip(" ")
    try:
        if variables.get(what):
            return variables[what]
        if "+" in what or "-" in what or "/" in what or "*" in what:
            for variable in variables:
                what = what.replace(variable, str(variables[variable]))
            return eval(what)
        elif what.startswith("'") or what.startswith('"'):
            return str(what).strip('"').strip("'")
        elif what == "input":
            return input()
        else:
            return float(what)

    except Exception as exception:
        print("exc")
        print(exception)

def run_code(code):
    global writing_function 

    for line in code.splitlines():

        args = line.split(" ")
        first = args[0]
        withoutfirst = line.lstrip(first).lstrip(" ")
        
        try:
            if writing_function == False or line.startswith("end"):
                if first == "print":
                    print(debug_check(line.lstrip(first)))
                elif first == "def" or first == "define" or first == "set":
                    line = line.lstrip(first).strip(" ")
                    name = line.split("=")[0].rstrip(" ")
                    value = line.split("=")[1].lstrip(" ")
                    variables[name] = debug_check(value)
                elif first == "fun" or first == "func" or first == "function":
                    writing_function = True
                    current_function = args[1]
                    functions[current_function] = ""
                elif first == "end" or first == "stop" or first == "cancel":            
                    writing_function = False            
                    current_function = ""
                elif first == "win" or first == "cmd" or first == "sys":
                    cmd = str(line).lstrip(first).lstrip(" ")
                    os.system(cmd)
                elif first == "wait" or first == "sleep" or first == "pause":
                    time.sleep(float(debug_check(withoutfirst)))
                else:
                    if first in functions:          
                        run_code(functions[first])
            else:
                functions[current_function] = functions[current_function] + "\n" + line
        except Exception as exc:            
            print(str(exc))

if os.path.exists(called):
    run_code(allpurpose.files.read_file(called))
