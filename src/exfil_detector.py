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

import collections

import intervaltree

import data_loader
import utils

import warnings
warnings.filterwarnings('ignore', module='.*')

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

APPLICATION_WINDOW_SIZE_MS = 5000

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

    per_user_mor_intervals = collections.defaultdict(list)

    moriarty_df = data_loader.load_data_file(pathlib2.Path(dataset_dir_name), 'moriarty')
    for userid, user_mor_df in moriarty_df.groupby('userid'):
        target_file_path = target_dir_path.joinpath(userid, EXFIL_DATA_MALICIOUS)
        target_file_path.parent.mkdir(parents=True, exist_ok=True)
        with target_file_path.open('w', newline='') as fout:
            csv_writer = csv.writer(fout, 'excel', delimiter=EXFIL_DATA_SEP)
            csv_writer.writerow(['userid', 'start_time', 'end_time', 'size'])
            csv_writer.writerows(_enum_malicious_send_data_time_intervals(user_mor_df))

            for userid, start_time, end_time, send_size in _enum_malicious_send_data_time_intervals(user_mor_df):
                per_user_mor_intervals[userid].append((start_time, end_time, send_size))

    per_user_iterator_and_current = dict()

    LOG.info(f'per_user_mor_intervals: {per_user_mor_intervals}')

    for df in src_application_reader:
        for userid, user_df in df.groupby('userid'):
            if userid not in per_user_iterator_and_current:
                it = iter(per_user_mor_intervals[userid])
                cur = next(it)
                per_user_iterator_and_current[userid] = (it, cur)

            it, cur = per_user_iterator_and_current[userid]

            target_file_path = target_dir_path.joinpath(userid, EXFIL_DATA_NETWORKING)
            target_file_path.parent.mkdir(parents=True,exist_ok=True)
            user_df['has_mal_upload'] = 0

            if it is not None and cur is not None:
                overlapping_df = user_df[
                    numpy.logical_and(
                        user_df.packagename == MORIARTY_PACKAGENAME,
                        numpy.logical_or(
                            numpy.logical_and(user_df.uuid-APPLICATION_WINDOW_SIZE_MS <= cur[0], cur[0] <= user_df.uuid),
                            numpy.logical_and(user_df.uuid-APPLICATION_WINDOW_SIZE_MS <= cur[1], cur[1] <= user_df.uuid),
                        )
                    )
                ]

                for idx in overlapping_df.index:
                    user_df.at[idx, 'has_mal_upload'] = 1

                if not overlapping_df.empty:
                    LOG.debug(f'Found mal upload:\n{overlapping_df}\ncur: {cur}')
                    try:
                        cur = next(it)
                        LOG.debug(f'New cur: {cur}')
                    except StopIteration:
                        LOG.info('Got StopIteration from it')
                        cur = None
                        it = None

                    per_user_iterator_and_current[userid] = (it, cur)

            data_loader.append_csv(user_df, str(target_file_path))



def load_exfil_data(exfil_data_dir: str, iterator=False):
    exfil_data_dir_path = pathlib2.Path(exfil_data_dir)

    networking_data_reader = pandas.read_csv(str(exfil_data_dir_path.joinpath(EXFIL_DATA_NETWORKING)), sep=EXFIL_DATA_SEP, iterator=iterator, chunksize=4096 if iterator else None)
    mal_df = pandas.read_csv(str(exfil_data_dir_path.joinpath(EXFIL_DATA_MALICIOUS)), sep=EXFIL_DATA_SEP, iterator=False)

    return networking_data_reader, mal_df

def shell(exfil_data_dir: str):
    df, mal_df = load_exfil_data(exfil_data_dir)
    from IPython import embed; embed()

def run(exfil_data_dir: str = r'sample-3\97bb95f55a'):
    df, mal_df = load_exfil_data(exfil_data_dir, iterator=False)

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
