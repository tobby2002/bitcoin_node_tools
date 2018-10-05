from logreader import app
import configparser
from flask import render_template


def strip_date(line):
    return(line.split(" ")[0])


def debug_parser(filename):

    try:
        with open(filename, 'r') as debugfile:
            lines = [line.rstrip('\n') for line in debugfile]
            # lastline = debugfile.readlines()[-1]

    except FileNotFoundError:
        return (f"Error(1): File {filename} not Found")

    bitcoin_version_list = []
    update_tip_list = []
    init_message_list = []
    other_message_list = []

    # Separate into different lists for easier management
    for line in lines:
        if "Bitcoin version" in line:
            bitcoin_version_list.append(line)
        elif "UpdateTip" in line:
            update_tip_list.append(line)
        elif "init message" in line:
            init_message_list.append(line)
        else:
            other_message_list.append(line)

    parsed_list = {
        "version": bitcoin_version_list,
        "update": update_tip_list,
        "init": init_message_list,
        "other": other_message_list
    }
    return parsed_list


@app.route("/")
@app.route("/home")
def home():
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        filename = config['CONFIG_OPTIONS']['debugfile']
    except KeyError:
        return (
            "Error(2): Cannot read config.ini for debugfile location")

    parsed_return = debug_parser(filename)
    print(strip_date(parsed_return["version"][0]))

    # print(parsed_return)

    return render_template('home.html')
