import sys
import os
from dataclasses import dataclass
import logging
from typing import Optional, List
import inspect
import re

import six
import argh
import pathlib2
import pandas
import numpy
import filelike.wrappers.translate


@dataclass
class _DataFileDescriptor:
    name: str #Friendly name later to be used as the record_source field value
    file_name: str #file name or pattern of the file in the dataset folder
    fields: List[tuple] #List of field descriptors of the form (name, data_type, is_relevant)

    def relevant_field_names(self):
        return [x[0] for x in self.fields if x[-1]]

    def type_mappings(self):
        return {x[0]:x[1] for x in self.fields}

    def __str__(self):
        return f'DataFileDescriptor< {self.name} >'

DATA_FILE_DESCRIPTORS = [
    _DataFileDescriptor(name='t4', file_name='*t4.*sv', fields=[("userid", str, True), ("uuid", 'Int64', True), ("version", str, True), ("cpuhertz", str, True), ("cpu_0", numpy.float32, True), ("cpu_1", numpy.float32, True), ("cpu_2", numpy.float32, True), ("cpu_3", numpy.float32, True), ("total_cpu", numpy.float32, True), ("totalmemory_freesize", 'Int64', True), ("totalmemory_max_size", 'Int64', True), ("totalmemory_total_size", 'Int64', True), ("totalmemory_used_size", 'Int64', True), ("traffic_mobilerxbytes", 'Int64', True), ("traffic_mobilerxpackets", 'Int64', True), ("traffic_mobiletxbytes", 'Int64', True), ("traffic_mobiletxpackets", 'Int64', True), ("traffic_totalrxbytes", 'Int64', True), ("traffic_totalrxpackets", 'Int64', True), ("traffic_totaltxbytes", 'Int64', True), ("traffic_totaltxpackets", 'Int64', True), ("traffic_totalwifirxbytes", 'Int64', True), ("traffic_totalwifirxpackets", 'Int64', True), ("traffic_totalwifitxbytes", 'Int64', True), ("traffic_totalwifitxpackets", 'Int64', True), ("traffic_timestamp", str, True), ("battery_charge_type", 'Int64', True), ("battery_current_avg", 'Int64', True), ("battery_health", 'Int64', True), ("battery_icon_small", 'Int64', True), ("battery_invalid_charger", 'Int64', True), ("battery_level", 'Int64', True), ("battery_online", 'Int64', True), ("battery_plugged", 'Int64', True), ("battery_present", str, True), ("battery_scale", 'Int64', True), ("battery_status", 'Int64', True), ("battery_technology", str, True), ("battery_temperature", 'Int64', True), ("battery_timestamp", str, True), ("battery_voltage", 'Int64', True), ("memtotal", 'Int64', True), ("memfree", 'Int64', True), ("buffers", 'Int64', True), ("cached", 'Int64', True), ("swapcached", 'Int64', True), ("active", 'Int64', True), ("inactive", 'Int64', True), ("active_anon", 'Int64', True), ("inactive_anon", 'Int64', True), ("active_file", 'Int64', True), ("inactive_file", 'Int64', True), ("unevictable", 'Int64', True), ("mlocked", 'Int64', True), ("hightotal", 'Int64', True), ("highfree", 'Int64', True), ("lowtotal", 'Int64', True), ("lowfree", 'Int64', True), ("swaptotal", 'Int64', True), ("swapfree", 'Int64', True), ("dirty", 'Int64', True), ("writeback", 'Int64', True), ("anonpages", 'Int64', True), ("mapped", 'Int64', True), ("shmem", 'Int64', True), ("slab", 'Int64', True), ("sreclaimable", 'Int64', True), ("sunreclaim", 'Int64', True), ("kernelstack", 'Int64', True), ("pagetables", 'Int64', True), ("commitlimit", 'Int64', True), ("committed_as", 'Int64', True), ("vmalloctotal", 'Int64', True), ("vmallocused", 'Int64', True), ("vmallocchunk", 'Int64', True), ("msmgpio_cpu0", 'Int64', True), ("msmgpio_sum_cpu123", 'Int64', True), ("wcd9xxx_cpu0", 'Int64', True), ("wcd9xxx_sum_cpu123", 'Int64', True), ("pn547_cpu0", 'Int64', True), ("pn547_sum_cpu123", 'Int64', True), ("cypress_touchkey_cpu0", 'Int64', True), ("cypress_touchkey_sum_cpu123", 'Int64', True), ("synaptics_rmi4_i2c_cpu0", 'Int64', True), ("synaptics_rmi4_i2c_sum_cpu123", 'Int64', True), ("sec_headset_detect_cpu0", 'Int64', True), ("sec_headset_detect_sum_cpu123", 'Int64', True), ("flip_cover_cpu0", 'Int64', True), ("flip_cover_sum_cpu123", 'Int64', True), ("home_key_cpu0", 'Int64', True), ("home_key_sum_cpu123", 'Int64', True), ("volume_down_cpu0", 'Int64', True), ("volume_down_sum_cpu123", 'Int64', True), ("volume_up_cpu0", 'Int64', True), ("volume_up_sum_cpu123", 'Int64', True), ("companion_cpu0", 'Int64', True), ("companion_sum_cpu123", 'Int64', True), ("slimbus_cpu0", 'Int64', True), ("slimbus_sum_cpu123", 'Int64', True), ("function_call_interrupts_cpu0", 'Int64', True), ("function_call_interrupts_sum_cpu123", 'Int64', True), ("cpu123_intr_prs", 'Int64', True), ("tot_user", 'Int64', True), ("tot_nice", 'Int64', True), ("tot_system", 'Int64', True), ("tot_idle", 'Int64', True), ("tot_iowait", 'Int64', True), ("tot_irq", 'Int64', True), ("tot_softirq", 'Int64', True), ("ctxt", 'Int64', True), ("btime", 'Int64', True), ("processes", 'Int64', True), ("procs_running", 'Int64', True), ("procs_blocked", 'Int64', True), ("connectedwifi_ssid", str, True), ("connectedwifi_level", 'Int64', True)]),
    _DataFileDescriptor(name='application', file_name='application*.*sv', fields=[("userid", str, True), ("uuid", 'Int64', True), ("applicationname", str, True), ("cpu_usage", numpy.float64, True), ("packagename", str, True), ("packageuid", 'Int64', True), ("uidrxbytes", 'Int64', True), ("uidrxpackets", 'Int64', True), ("uidtxbytes", 'Int64', True), ("uidtxpackets", 'Int64', True), ("cguest_time", 'Int64', True), ("cmaj_flt", 'Int64', True), ("cstime", 'Int64', True), ("cutime", 'Int64', True), ("dalvikprivatedirty", 'Int64', True), ("dalvikpss", 'Int64', True), ("dalvikshareddirty", 'Int64', True), ("guest_time", 'Int64', True), ("importance", 'Int64', True), ("importancereasoncode", 'Int64', True), ("importancereasonpid", 'Int64', True), ("lru", 'Int64', True), ("nativeprivatedirty", 'Int64', True), ("nativepss", 'Int64', True), ("nativeshareddirty", 'Int64', True), ("num_threads", 'Int64', True), ("otherprivatedirty", 'Int64', True), ("otherpss", 'Int64', True), ("othershareddirty", 'Int64', True), ("pgid", 'Int64', True), ("pid", 'Int64', True), ("ppid", 'Int64', True), ("priority", 'Int64', True), ("rss", 'Int64', True), ("rsslim", 'Int64', True), ("sid", 'Int64', True), ("start_time", 'Int64', True), ("state", str, True), ("stime", 'Int64', True), ("tcomm", str, True), ("utime", 'Int64', True), ("vsize", 'Int64', True), ("version_code", 'Int64', True), ("version_name", str, True), ("sherlock_version", str, True), ("tgpid", 'Int64', True), ("flags", str, True), ("wchan", str, True), ("exit_signal", 'Int64', True), ("minflt", 'Int64', True), ("cminflt", 'Int64', True), ("majflt", 'Int64', True), ("startcode", 'Int64', True), ("endcode", 'Int64', True), ("nice", 'Int64', True), ("itrealvalue", 'Int64', True), ("processor", 'Int64', True), ("rt_priority", 'Int64', True)]),
    _DataFileDescriptor(name='sms', file_name='sms.*sv', fields=[('userid', str, True), ('uuid', 'Int64', True), ('address', str, True), ('containURL', bool, True), ('date', 'Int64', True), ('fromcontacts', bool, True), ('type', 'Int64', True)]),
    _DataFileDescriptor(name='screenon', file_name='screenon.*sv', fields=[('userid', str, True), ('uuid', 'Int64', True), ('screenon', bool, True), ('timtestamp', str, True)] ),
    _DataFileDescriptor(name='userpresent', file_name='userpresent*.*sv', fields=[('userid', str, True), ('uuid', 'Int64', True), ('timestamp', str, True)]),
    _DataFileDescriptor(name='moriarty', file_name='moriarty*.*sv', fields=[('userid', str, True), ('uuid', 'Int64', True), ('version', str, True), ('action', str, True), ('actionType', str, True), ('details', str, True), ('sessionId', numpy.float32, True), ('sessionType', 'str', True), ('behavior', str, True)]),
]

LOG = logging.getLogger(__name__)

PARENTHESIS_PATTERN = re.compile(r'(\(.*?\))')

def _normalize_commas(text):
    def _remove_commas(mo):
        return mo.group(0).replace(',', '_')
    return PARENTHESIS_PATTERN.sub(_remove_commas, text)

def _read_csv(fpath: pathlib2.Path, dfd: _DataFileDescriptor, user_ids: Optional[List[str]] = None, usecols=None, iterator=False) -> pandas.DataFrame:
    """

    :param fpath: path of csv file to load
    :param dfd: _DataFileDescriptor
    :param user_ids: optional list of user_ids to load
    :param usecols: optional list of columns to load
    :return: DataFrame read from csv
    """
    if fpath.suffix.lower() == '.csv':
        f = fpath.open('r', encoding='utf8')
        f = filelike.wrappers.translate.Translate(f, _normalize_commas)
        header = f.readline().lower().replace('\ufeff', '').strip() #strip utf8 marker
        header_fields = header.split(',')
        field_to_type = {name : t for (name, t, _) in dfd.fields}
        reader = pandas.read_csv(
            f,
            sep=',',
            iterator=True,
            header=None,
            skiprows=1,
            names=header_fields,
            dtype=field_to_type,
            usecols=usecols,
            chunksize=1024
        )
    elif fpath.suffix.lower() == '.tsv':
        f = fpath.open('r', encoding='latin1')
        reader = pandas.read_csv(f, sep='\t', header=None,
                                 names=[x[0] for x in dfd.fields] if not usecols else usecols,
                                 usecols=dfd.relevant_field_names() if not usecols else usecols,
                                 dtype=dfd.type_mappings(), iterator=True, chunksize=1024)
    else:
        raise ValueError( f'{fpath} has unsupported extension: {fpath.suffix}')

    if not iterator:
        try:
            if user_ids:
                df = pandas.concat((chunk[chunk.userid.isin(user_ids)] for chunk in reader))
            else:
                df = pandas.concat(reader)
        finally:
            f.close()
        return df
    #else
    return reader

def _write_csv(df: pandas.DataFrame, target_file_name: str):
    df.to_csv(target_file_name, sep='\t', index=False)

def _enum_relevant_data_files(dirpath: pathlib2.Path):
    for dfd in DATA_FILE_DESCRIPTORS:
        if not dfd.fields:
            LOG.warning(f'{dfd} has no fields defined, skipping')
            continue

        try:
            fpath = next(dirpath.glob(dfd.file_name))  #We assume there's exactly one
        except StopIteration:
            continue
        yield fpath, dfd

def _load(dirname: str, user_ids: Optional[List[str]] = None, iterator=False) -> dict:
    dirpath = pathlib2.Path(dirname)

    if user_ids:
        user_ids = user_ids.split(',')

    df: pandas.DataFrame = None

    data_frames = {}

    for fpath, dfd in _enum_relevant_data_files(dirpath):
        LOG.debug(f'Loading {dfd} from {fpath} (iterator={iterator})')
        cur_df = _read_csv(fpath, dfd, user_ids, iterator=iterator)
        data_frames[dfd.name] = cur_df

    return data_frames

def load_shell(dirname: str, user_ids: Optional[List[str]] = None, iterator=False) -> pandas.DataFrame:
    """
    Load all relevant csv/tsv files into pandas dataframes into a dict indexed by data file type (see DATA_FILE_DESCRIPTORS)
    open an ipython shell to interactively play with the data
    :param dirname:
    :param user_ids:
    :param iterator:
    :return:
    """
    dfs = _load(dirname, user_ids, iterator)
    from IPython import embed; embed()

def list_users(dirname: str):
    """
    List all unique user ids found in relevant csv/tsv files in given dir
    :param dirname:
    :return:
    """
    users = set()
    for fpath, dfd in _enum_relevant_data_files(pathlib2.Path(dirname)):
        for df in _read_csv(fpath, dfd, user_ids=None, usecols=['userid'], iterator=True):
            for uid in df['userid'].unique():
                users.add(uid)

    return users

# def gather_and_split_users(src_dir: str, target_dir: str = None):
#     src_path = pathlib2.Path(src_dir)
#     if not target_dir:
#         target_dir = src_path.name
#     target_path = pathlib2.Path(target_dir)
#
#     df = _load(src_dir)
#     target_path.mkdir(exist_ok=True)
#
#     for user_id, user_df in df.groupby('userid'):
#         target_file_path = target_path.joinpath(f'{user_id}.tsv')
#         _write_csv(user_df, str(target_file_path))

def _split_csv_users(csv_file_path: pathlib2.Path, target_file_name_prefix: str):
    reader = pandas.read_csv(str(csv_file_path),
                             sep='\t',
                             header=None,
                             iterator=True,
                             encoding='windows-1252',
                             chunksize=1024,
                             )

    for chunk_df in reader:
        for user_id, user_df in chunk_df.groupby(0):  # type: tuple[str, pandas.DataFrame]
            user_df.to_csv(f'{target_file_name_prefix}-{user_id}.tsv', sep='\t', mode='a', header=False)

def split_users(csv_file_name: str, target_dir: str = None):
    """
    Split given csv/tsv file to different files - one for each userid, put results in given target dir
    :param csv_file_name:
    :param target_dir:
    :return:
    """
    src_path = pathlib2.Path(csv_file_name)
    if not target_dir:
        target_dir = pathlib2.Path(f'{src_path.parent.name}')
    target_path = pathlib2.Path(target_dir)
    target_path.mkdir(exist_ok=True)

    _split_csv_users(src_path, str(target_path.joinpath(src_path.stem)))

def split_users_in_dir(dir_name: str, target_dir: str = None):
    """
    Split all csv/tsv files in dir_name by user
    :param dir_name:
    :param target_dir:
    :return:
    """
    src_dir_path = pathlib2.Path(dir_name)
    if not target_dir:
        target_dir = src_dir_path.name
    target_path = pathlib2.Path(target_dir)
    target_path.mkdir(exist_ok=True)

    for src_file_path in src_dir_path.iterdir():
        if src_file_path.match('*.tsv'):
            LOG.debug(f'Splitting {src_file_path} => {target_dir}')
            split_users(src_file_path, target_dir)

def shell():
    from IPython import embed; embed()

def _main():
    out = six.StringIO()
    import utils
    utils.init_logging(pathlib2.Path(__file__).parent.joinpath('logs', 'data_loader.log'))
    # Expose all functions that don't begin with an underscore "_" in the current module
    argh.dispatch_commands(
        [obj for name, obj in inspect.getmembers(sys.modules[__name__]) if
         inspect.isfunction(obj) and obj.__module__ == '__main__' and not name.startswith('_')],
        output_file=out
    )

    print(out.getvalue())

if '__main__' == __name__:
    _main()
