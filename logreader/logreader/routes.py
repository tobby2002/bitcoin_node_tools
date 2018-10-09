from logreader import app
import configparser
from flask import render_template
import re
from dateutil import parser
from datetime import datetime, timedelta


def strip_time(line):
    # Strips the time from a log line
    time_strip = re.search(r'(\d+:\d+:\d+)', line)
    return (time_strip)


def strip_date(line):
    # Strips the date from a log line
    date_strip = re.search(r'(\d+-\d+-\d+)', line)
    return(date_strip)


def update_blockchain_stats(update_tip_list, last_n):
    # update_tip_list should be reverse sorted
    # last_n = the last n inputs will be used to calculate
    # estimated times, average speed b/w blocks and other variables

    last_n = int(last_n)
    if last_n > len(update_tip_list):
        last_n = len(update_tip_list)
    update_tip_list_last_n = update_tip_list[0:last_n]
    # grab items from update to report
    last_update = update_tip_list[0]
    first_update = update_tip_list[-1]
    last_new_best = re.search('new best=(.+?) ', last_update)
    last_height = re.search('height=(.+?) ', last_update)
    last_version = re.search('version=(.+?) ', last_update)
    last_tx = re.search('tx=(.+?) ', last_update)
    last_date = re.search('date=(.+?) ', last_update)
    first_progress = re.search('progress=(.+?) ', first_update)
    last_progress = re.search('progress=(.+?) ', last_update)
    last_cache = re.search('cache=(.+?)', last_update)
    # now calculate the average of last n updates
    last_time = datetime.strptime(
        strip_time(last_update).group(0), "%H:%M:%S")
    first_time = datetime.strptime(
        strip_time(first_update).group(0), "%H:%M:%S")
    elapsed_seconds_n = (last_time - first_time).seconds
    progress_per_second = (
        float(last_progress.group(0)[9:]) - float(
            first_progress.group(0)[9:]))/elapsed_seconds_n
    remaining_update = (1-float(last_progress.group(0)[9:]))
    seconds_left = remaining_update / progress_per_second
    synch_eta = datetime.now() + timedelta(seconds=seconds_left)

    update_stats = {
        "current_time": datetime.now(),
        "last_n": last_n,
        "first_time": first_time,
        "last_time": last_time,
        "elapsed_seconds_n": elapsed_seconds_n,
        "last_new_best": last_new_best.group(0)[9:],
        "last_height": last_height.group(0)[7:],
        "last_version": last_version.group(0)[8:],
        "last_tx": last_tx.group(0)[3:],
        "last_date": last_date.group(0)[5:],
        "last_progress": last_progress.group(0)[9:],
        "last_cache": last_cache.group(0)[6:],
        "progress_per_second": progress_per_second,
        "remaining_perc": remaining_update,
        "seconds_left": seconds_left,
        "synch_eta": synch_eta
    }

    return (update_stats)


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

    # Create initial dates as start and end
    start_date = datetime.now()
    end_date = datetime(2000, 1, 1,)

    # Separate into different lists for easier management
    for line in lines:
        try:
            line_date = parser.parse(strip_date(line).group(0))
        except AttributeError:
            line_date = None
        if line_date is not None:
            if line_date < start_date:
                start_date = line_date
            if line_date > end_date:
                end_date = line_date
        if "Bitcoin version" in line:
            bitcoin_version_list.append(line)
        elif "UpdateTip" in line:
            update_tip_list.append(line)
        elif "init message" in line:
            init_message_list.append(line)
        else:
            other_message_list.append(line)

    # Reverse Sort some of the lists
    init_message_list.sort(reverse=True)
    update_tip_list.sort(reverse=True)
    other_message_list.sort(reverse=True)

    # Create a single dictionary to feed the html
    parsed_list = {
        "file_name": filename,
        "start_date": start_date,
        "end_date": end_date,
        "version": bitcoin_version_list,
        "update": update_tip_list,
        "init": init_message_list,
        "other": other_message_list
    }
    return parsed_list


@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def home():
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        filename = config['CONFIG_OPTIONS']['debugfile']
    except KeyError:
        return (
            "Error(2): Cannot read config.ini for debugfile location")

    try:
        last_n = config['CONFIG_OPTIONS']['update_tip_list_last_n']
    except KeyError:
        return (
            "Error(2): Cannot read config.ini for update_tip_list_last_n")

    parsed_return = debug_parser(filename)

    update_stats = update_blockchain_stats(parsed_return["update"], last_n)

    return render_template('home.html', data=parsed_return, stats=update_stats)
