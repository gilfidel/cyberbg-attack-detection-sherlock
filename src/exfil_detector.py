import sys
import os
import logging

import functools
import pathlib2
import inspect
import six
import re

import pandas
import numpy
import argh

import data_loader
import utils

LOG = logging.getLogger('exfil_detector')

APPLICATION_EXFIL_FIELDS = ['userid', 'uuid', 'packagename', 'uidrxbytes', 'uidrxpackets', 'uidtxbytes', 'uidtxpackets']

DURATION_AND_SIZE_PATTERN = re.compile(r'Successful send to server\(duration \[msec\]_size \[bytes\]\);(\d+);(\d+)')

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

        yield (r.userid, start_time, end_time)

def extract_exfil_related_data( dataset_dir_name: str, target_file_name: str ):
    src_reader = data_loader.load_data_file(pathlib2.Path(dataset_dir_name), 'application', usecols=APPLICATION_EXFIL_FIELDS, iterator=True)

    target_file_path = pathlib2.Path(target_file_name)
    target_file_path.parent.mkdir(exist_ok=True)

    LOG.debug( f'Extracting data to: {target_file_path}')

    for df in src_reader:
        data_loader._append_csv(df, str(target_file_path))

def run( dataset_dir_name: str ):
    app_reader = data_loader.load_data_file(pathlib2.Path(dataset_dir_name), 'application', usecols=APPLICATION_EXFIL_FIELDS, iterator=True)
    moriarty_df = data_loader.load_data_file(pathlib2.Path(dataset_dir_name), 'moriarty')

    malicious_sends = _enum_malicious_send_data_time_intervals(moriarty_df)

    ms = list(malicious_sends)
    from IPython import embed; embed()

    # for df_chunk in app_reader:
    #     for userid, user_df in df_chunk.group():
    #         pass

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
