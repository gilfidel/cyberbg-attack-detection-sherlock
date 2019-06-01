import sys
import os
import logging

import functools
import inspect
import six
import re
import csv

import pathlib2
import pandas
import numpy
import argh

import data_loader
import utils

LOG = logging.getLogger('exfil_detector')

APPLICATION_EXFIL_FIELDS = ['userid', 'uuid', 'packagename', 'uidrxbytes', 'uidrxpackets', 'uidtxbytes', 'uidtxpackets']

DURATION_AND_SIZE_PATTERN = re.compile(r'Successful send to server\(duration \[msec\]_size \[bytes\]\);(\d+);(\d+)')


MORIARTY_PACKAGENAME = 'com.bgu.sherlock.Moriarty'

def _extract_send_duration_and_size(details_text: str):
    #Successful send to server(duration [msec]_size [bytes]);604;27
    mo = DURATION_AND_SIZE_PATTERN.match(details_text)
    if mo is None:
        raise ValueError(f'Invalid details text: {details_text}')

    return [int(x) for x in mo.groups()]

def _enum_malicious_send_data_time_intervals(moriarty_df: pandas.DataFrame):
    """
    Generates (userid, start_time, end_time) tuples for all instances of malicious data sends.
    :param moriarty_df:
    :return:
    """
    send_data_df = moriarty_df[functools.reduce( numpy.logical_and,
                                                 [  moriarty_df.actiontype == 'malicious',
                                                    moriarty_df.action == 'Sending Data',
                                                    moriarty_df.details.str.startswith('Successful send to server')], True)]

    for row_id, r in send_data_df.iterrows():
        end_time = r.uuid
        send_duration, send_size = _extract_send_duration_and_size(r.details)
        start_time = end_time - send_duration

        yield (r.userid, start_time, end_time, send_size)

EXFIL_DATA_NETWORKING = 'networking.tsv'
EXFIL_DATA_MALICIOUS = 'malicious.tsv'

EXFIL_DATA_SEP = '\t'

def extract_exfil_data( dataset_dir_name: str, target_dir: str ):
    """
    Preprocesses a sherlock dataset in _dataset_dir_name_ and narrows it down into a dataset for malicious data exfiltration:
        - creates a subfolder for each unique user id
        - in each such subfolder:
            + creates a filtered application.csv file only containing networking related data
            + creates a malicious.csv file with intervals of sending malicious data

    :param dataset_dir_name:
    :param target_dir:
    :return:
    """
    src_application_reader = data_loader.load_data_file(pathlib2.Path(dataset_dir_name), 'application', usecols=APPLICATION_EXFIL_FIELDS, iterator=True, chunksize=10*1024)

    target_dir_path = pathlib2.Path(target_dir)

    for df in src_application_reader:
        for userid, user_df in df.groupby('userid'):
            target_file_path = target_dir_path.joinpath(userid, EXFIL_DATA_NETWORKING)
            target_file_path.parent.mkdir(parents=True,exist_ok=True)
            data_loader.append_csv(user_df, str(target_file_path))

    moriarty_df = data_loader.load_data_file(pathlib2.Path(dataset_dir_name), 'moriarty')
    for userid, user_mor_df in moriarty_df.groupby('userid'):
        target_file_path = target_dir_path.joinpath(userid, EXFIL_DATA_MALICIOUS)
        target_file_path.parent.mkdir(parents=True,exist_ok=True)
        with target_file_path.open('w', newline='') as fout:
            csv_writer = csv.writer(fout, 'excel', delimiter=EXFIL_DATA_SEP)
            csv_writer.writerow(['userid', 'start_time', 'end_time', 'size'])
            csv_writer.writerows(_enum_malicious_send_data_time_intervals(user_mor_df))

def load_exfil_data(exfil_data_dir: str):
    exfil_data_dir_path = pathlib2.Path(exfil_data_dir)

    networking_data_reader = pandas.read_csv(str(exfil_data_dir_path.joinpath(EXFIL_DATA_NETWORKING)), sep=EXFIL_DATA_SEP, iterator=True, chunksize=4096)
    mal_df = pandas.read_csv(str(exfil_data_dir_path.joinpath(EXFIL_DATA_MALICIOUS)), sep=EXFIL_DATA_SEP, iterator=False)

    return networking_data_reader, mal_df

def shell(exfil_data_dir: str):
    networking_data_reader, mal_df = load_exfil_data(exfil_data_dir)
    from IPython import embed; embed()


def _main():
    utils.init_logging(os.path.join('logs', 'exfil_detector'))
    LOG.info( f'=== STARTED: sys.argv: {sys.argv}')
    out = six.StringIO()
    # Expose all functions that don't begin with an underscore "_" in the current module
    argh.dispatch_commands(
        [obj for name, obj in inspect.getmembers(sys.modules[__name__]) if
         inspect.isfunction(obj) and obj.__module__ == '__main__' and not name.startswith('_')],
        output_file=out
    )

    print(out.getvalue())

if '__main__' == __name__:
    _main()
