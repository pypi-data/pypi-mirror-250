#!/usr/bin/env python3
"""
Generate a wafer map suitable for picking good SiPMs from a wafer using a die
ejector, such that they may be transferred to trays and later installed onto
vTiles.

Identification of good/bad SiPMs:

classification  quality flags
'good'          {0, 1}
'bad'           {2, 4, 5, 6, 8, 9, 10, 12, 14, 16, 17, 18, 20, 21, 22, 24, 26,
                 27, 28, 30}

For picking a wafer, we can just use good/bad classification.

>>> set(dbi.get('sipm_test', classification='bad').data.quality_flag)
{2, 4, 5, 6, 8, 9, 10, 12, 14, 16, 17, 18, 20, 21, 22, 24, 26, 27, 28, 30}
>>> set(dbi.get('sipm_test', classification='good').data.quality_flag)
{0, 1}
"""

import argparse
import asyncio
import functools
import io
import operator
import sys
import types

import aiohttp
import pandas as pd

try:
    from ds20kdb import visual
except ModuleNotFoundError:
    print('Please install ds20kdb-avt')
    sys.exit(3)
except ImportError:
    print('Please upgrade to the latest ds20kdb-avt version')
    sys.exit(3)
else:
    from ds20kdb import interface


##############################################################################
# command line option handler
##############################################################################


def check_arguments():
    """
    handle command line options

    --------------------------------------------------------------------------
    args : none
    --------------------------------------------------------------------------
    returns : none
    --------------------------------------------------------------------------
    """
    parser = argparse.ArgumentParser(
        description='Generate a wafer map suitable for picking good SiPMs\
        from a wafer using a die ejector, such that they may be transferred\
        to trays and later installed onto vTiles. The default behaviour when\
        identifying good/bad SiPMs is to perform a comprehensive check for\
        sipm_test.classification==\'good\' and sipm_test.quality_flag==0,\
        where only the row with the largest value of sipm_test.sipm_qc_id is\
        considered. Support requests to: Alan Taylor, Dept. of Physics,\
        University of Liverpool, avt@hep.ph.liv.ac.uk.')
    parser.add_argument(
        'lot', nargs=1, metavar='lot',
        help='Wafer lot number, e.g. 9346509',
        type=int)
    parser.add_argument(
        'wafer_number', nargs=1, metavar='wafer_number',
        help='Wafer number.',
        type=int)

    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument(
        '-c', '--classification',
        action='store_true',
        help='DEBUG OPTION. Identify good/bad SiPMs using\
        sipm_test.classification alone. This option is useful for\
        reproducing historic wafer maps. Note that this generates\
        "pessamistic" wafer maps, in that if a SiPM has *ever* received a bad\
        test classificaton, that will be reported, even if a subsequent test\
        showed a good result.'
    )
    group1.add_argument(
        '-s', '--sequential',
        action='store_true',
        help='DEBUG OPTION. Access the database sequentially when performing\
        a comprehensive check for SiPM good/bad status, this may take\
        approximately one minute to complete. This option may be useful if the\
        database is under considerable load.'
    )

    args = parser.parse_args()

    return args.lot[0], args.wafer_number[0], args.classification, args.sequential


##############################################################################
# Methods of identifying good/bad SiPMs
##############################################################################


def identify_sipm_status(dbi, classification, wafer_pid, sequential):
    """
    For the given wafer, obtain two sets of wafer (column, row) pairs, for
    good/bad SiPMs respectively. Chooses between two methods of accomplishing
    this goal.

    Notes from 2023 12 06:

    The sipm_test.classification good/bad flag was historically used to
    indicate whether SiPMs were deemed acceptable for use in production. This
    should be true again at some point in the future.

    Currently a more complex lookup is required. For a given SiPM ID, only the
    row with the largest value of sipm_test.sipm_qc_id is considered.
    From that row, for the SiPM to be regarded as good it must have
    sipm_test.classification == 'good' and sipm_test.quality_flag == 0.

    --------------------------------------------------------------------------
    args
        dbi : ds20kdb.interface.Database
            Instance of the Database interface class; allows communication
            with the database.
        full : bool
            Perform a comprehensive check of SiPM status.
        wafer_pid : int
        sequential : bool
    --------------------------------------------------------------------------
    returns (set, set)
    --------------------------------------------------------------------------
    """
    print('Obtaining SiPMs for this wafer')

    dfr = dbi.get('sipm', wafer_id=wafer_pid).data

    if classification:
        return sipm_status_by_classification(dbi, dfr)

    if sequential:
        return sipm_status_full_check(dbi, dfr)

    return sipm_status_full_check_async(dbi, dfr)


def sipm_status_by_classification(dbi, dfr):
    """
    For the given wafer, obtain two sets of wafer (column, row) pairs, for
    good/bad SiPMs respectively.

    Uses just sipm_test.classification for the evaluation.

    Note that this check as currently implemented is overly pessamistic. If a
    SiPM ID has ever been assigned a bad classification, it will show as bad
    here. In Q4 2023, <1% of SiPM IDs had multiple entries, and a later
    corrected entry may contain a good result.

    --------------------------------------------------------------------------
    args
        dbi : ds20kdb.interface.Database
            Instance of the Database interface class; allows communication
            with the database.
        dfr : Pandas DataFrame
    --------------------------------------------------------------------------
    returns (set, set)
    --------------------------------------------------------------------------
    """
    print('Obtaining SiPMs with bad classification(s)')

    bad_sipm_ids = set(dbi.get('sipm_test', classification='bad').data.sipm_id)
    wafer_map_bad = {
        (col, row)
        for sipm_pid, col, row in zip(dfr.sipm_pid, dfr.column, dfr.row)
        if sipm_pid in bad_sipm_ids
    }

    all_locations = set(interface.wafer_map_valid_locations())
    wafer_map_good = all_locations.difference(wafer_map_bad)

    return wafer_map_good, wafer_map_bad


def sipm_status_full_check(dbi, dfr):
    """
    For the given wafer, obtain two sets of wafer (column, row) pairs, for
    good/bad SiPMs respectively.

    Uses sipm_test.classification, sipm_test.quality_flag and
    sipm_test.sipm_qc_id for the evaluation.

    --------------------------------------------------------------------------
    args
        dbi : ds20kdb.interface.Database
            Instance of the Database interface class; allows communication
            with the database.
        dfr : Pandas DataFrame
    --------------------------------------------------------------------------
    returns (set, set)
    --------------------------------------------------------------------------
    """
    print('Identifying good SiPMs for this wafer (this may take a minute)')

    # this will give us 268 SiPM IDs, not 264
    all_sipms_ids_for_wafer = set(dfr.sipm_pid.values)

    columns = ['classification', 'quality_flag', 'sipm_qc_id']

    good_sipm_ids = set()
    for sipm_id in all_sipms_ids_for_wafer:
        dfr_tmp = dbi.get('sipm_test', sipm_id=sipm_id).data

        # Get columns for row with highest sipm_qc_id value.
        try:
            classification, quality_flag, _ = dfr_tmp[columns].sort_values('sipm_qc_id').values[-1]
        except IndexError:
            # We will see IndexError for the four SiPMs at the far left/right
            # edges that are not tested.
            pass
        else:
            if classification == 'good' and quality_flag == 0:
                good_sipm_ids.add(sipm_id)

    wafer_map_good = {
        (col, row)
        for sipm_pid, col, row in zip(dfr.sipm_pid, dfr.column, dfr.row)
        if sipm_pid in good_sipm_ids
    }

    # Since there is more than one test in table 'sipm_test' for each sipm_id,
    # it is possible that a SiPM may have both 'good' and 'bad'
    # classifications. We only care about a bad classification existing, since
    # we won't select that SiPM for use on a vTile.

    all_locations = set(interface.wafer_map_valid_locations())
    wafer_map_bad = all_locations.difference(wafer_map_good)

    if not wafer_map_good:
        print(
            'WARNING: All SiPMs are reported as bad. '
            'If this is an older wafer, consider using --classification'
        )

    return wafer_map_good, wafer_map_bad


async def fetch(url, session, sipm_id):
    """
    Fetch database response for a single SiPM URL.

    Given that the database is unhappy with many concurrent connections, we
    need to ensure that we catch connection errors here and retry as
    appropriate.

    --------------------------------------------------------------------------
    args
        url : string
        session : class aiohttp.client.ClientSession
        sipm_id : int
    --------------------------------------------------------------------------
    returns : dict with single key/value pair
        {int: string}
    --------------------------------------------------------------------------
    """
    data = None
    while data is None:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.text()
        except aiohttp.ClientError:
            await asyncio.sleep(1)

    return {sipm_id: data}


async def fetch_all(dbi, urls):
    """
    Fetch database responses for all SiPM URLs.

    The database cannot cope with the default upper limit of 100 concurrent
    connections, so limit this to something it can handle. Note that the the
    limit set here needs to take into consideration others connecting to the
    database. Too many concurrent connections causes the database to generate
    500 Internal Server Error.

    Could also use the following in this context:

    connector = aiohttp.TCPConnector(limit_per_host=16)

    --------------------------------------------------------------------------
    args
        dbi : ds20kdb.interface.Database
            Instance of the Database interface class; allows communication
            with the database.
        urls : dict
            {int: string, ...} e.g. {sipm_id: url, ...}
    --------------------------------------------------------------------------
    returns : list of dict
        [{int: string}, ...]
        e.g. [
            {307200: 'id,timestamp, ... ,77,good,0,,1.831e-11\n'}, ...
        ]
    --------------------------------------------------------------------------
    """
    connector = aiohttp.TCPConnector(limit=16)
    username, password = dbi.session.auth

    async with aiohttp.ClientSession(
        auth=aiohttp.BasicAuth(username, password=password),
        connector=connector
    ) as session:
        tasks = (fetch(url, session, sipm_id) for sipm_id, url in urls.items())
        return await asyncio.gather(*tasks)


def csv_to_dataframe(response):
    """
    Convert database response text string to a Pandas DataFrame.

    --------------------------------------------------------------------------
    args
        response : string
            'id,timestamp,institute_id, ... ,77,good,0,,1.501e-11'
    --------------------------------------------------------------------------
    returns : pandas.DataFrame
    --------------------------------------------------------------------------
    """
    return pd.read_csv(
        io.StringIO(response), sep=',', encoding='utf-8', low_memory=False,
    )


def sipm_status_full_check_async(dbi, dfr):
    """
    For the given wafer, obtain two sets of wafer (column, row) pairs, for
    good/bad SiPMs respectively.

    Uses sipm_test.classification, sipm_test.quality_flag and
    sipm_test.sipm_qc_id for the evaluation.

    --------------------------------------------------------------------------
    args
        dbi : ds20kdb.interface.Database
            Instance of the Database interface class; allows communication
            with the database.
        dfr : Pandas DataFrame
    --------------------------------------------------------------------------
    returns (set, set)
    --------------------------------------------------------------------------
    """
    print('Identifying good SiPMs for this wafer')

    # this will give us 268 SiPM IDs, not 264
    all_sipms_ids_for_wafer = set(dfr.sipm_pid.values)

    urls = {
        sipm_id: dbi.get_url('sipm_test', sipm_id=sipm_id)
        for sipm_id in all_sipms_ids_for_wafer
    }

    # Fetch the good/bad status for this wafer's SiPMs in parallel.
    # functools.reduce combines the all the individual dicts (one for each
    # SiPM) to form a single dict.
    mapping = functools.reduce(operator.ior, asyncio.run(fetch_all(dbi, urls)), {})

    columns = ['classification', 'quality_flag', 'sipm_qc_id']
    good_sipm_ids = set()
    for sipm_id, dfr_tmp in mapping.items():
        dfr_tmp = csv_to_dataframe(dfr_tmp)

        # Get columns for row with highest sipm_qc_id value.
        try:
            classification, quality_flag, _ = dfr_tmp[columns].sort_values('sipm_qc_id').values[-1]
        except IndexError:
            # We will see IndexError for the four SiPMs at the far left/right
            # edges that are not tested.
            pass
        else:
            if classification == 'good' and quality_flag == 0:
                good_sipm_ids.add(sipm_id)

    wafer_map_good = {
        (col, row)
        for sipm_pid, col, row in zip(dfr.sipm_pid, dfr.column, dfr.row)
        if sipm_pid in good_sipm_ids
    }

    # Since there is more than one test in table 'sipm_test' for each sipm_id,
    # it is possible that a SiPM may have both 'good' and 'bad'
    # classifications. We only care about a bad classification existing, since
    # we won't select that SiPM for use on a vTile.

    all_locations = set(interface.wafer_map_valid_locations())
    wafer_map_bad = all_locations.difference(wafer_map_good)

    if not wafer_map_good:
        print(
            'WARNING: All SiPMs are reported as bad. '
            'If this is an older wafer, consider using --classification'
        )

    return wafer_map_good, wafer_map_bad


##############################################################################
# main
##############################################################################

def main():
    """
    Generate a wafer map suitable for picking good SiPMs from a wafer using a
    die ejector, such that they may be transferred to trays and later
    installed onto vTiles.
    """
    lot, wafer_number, classification, sequential = check_arguments()

    status = types.SimpleNamespace(success=0, unreserved_error_code=3)

    dbi = interface.Database()

    print(f'looking up {lot}.{wafer_number:02}')
    try:
        wafer_pid = int(
            dbi.get('wafer', lot=lot, wafer_number=wafer_number).data.wafer_pid.values[0]
        )
    except AttributeError:
        print('Check Internet connection')
        return status.unreserved_error_code
    except IndexError:
        print('Wafer may not exist in the database')
        return status.unreserved_error_code
    except TypeError:
        print(f'No response from the database for {lot}.{wafer_number:02}')
        return status.unreserved_error_code

    print(f'PID {wafer_pid}')

    ##########################################################################
    # obtain (col, row) locations for good/bad SiPMs

    wafer_map_good, wafer_map_bad = identify_sipm_status(
        dbi, classification, wafer_pid, sequential
    )

    ##########################################################################
    # draw wafer

    print('Saving wafer map')
    sipm_groups = [
        {
            'name': 'good',
            'locations': wafer_map_good,
            'sipm_colour': 'green',
            'text_colour': 'black',
        },
        {
            'name': 'bad',
            'locations': wafer_map_bad,
            'sipm_colour': 'darkred',
            'text_colour': 'lightgrey',
        },
    ]

    visual.DrawWafer(
        wafer_lot=lot,
        wafer_number=wafer_number,
        sipm_groups=sipm_groups
    ).save()

    return status.success


##############################################################################
if __name__ == '__main__':
    sys.exit(main())
