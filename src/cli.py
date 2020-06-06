import logging
import argparse
from beat import beat
from definitions import path_log

# LOGGING CONFIGURATION
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)
logging.root.addHandler(logging.FileHandler(path_log, mode='w', encoding='UTF-8'))
logging.getLogger("easyprocess").setLevel(logging.WARNING)

# COMMAND LINE ARGUMENT PARSER
parser = argparse.ArgumentParser()
# POSITIONAL ARGS
parser.add_argument('subject', type=str,
                    help='the subject you want to search')
parser.add_argument('state_code', type=str,
                    help='the two letter state abbreviation for where you want to search the subject')
# OPTIONAL ARGS
parser.add_argument('-c', '--city', type=str,
                    help='the city you want to begin the search at (cities are searched alphabetically)')
args = parser.parse_args()
subject = args.subject.strip()
state_code = args.state_code.strip().upper()

# VALIDATE ARG VALUES & RUN BEAT
if len(state_code) != 2:
    print(f"\"{state_code}\"")
    logging.error('State Code is invalid. Must be two letters.')
elif not isinstance(state_code, str):
    logging.error('State Code is invalid. Must be a string.')
elif not isinstance(subject, str):
    logging.error('Subject is invalid. Must be a string.')
else:
    if args.city:
        city = args.city.strip()
        if not isinstance(city, str):
            logging.error('City is invalid. Must be a string.')
        else:
            beat(subject=subject, state_code=state_code, start_city=city)
    else:
        beat(subject=subject, state_code=state_code)
