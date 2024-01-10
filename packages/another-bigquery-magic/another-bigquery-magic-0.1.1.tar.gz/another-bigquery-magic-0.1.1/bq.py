# -*- coding: utf-8 -*-

import sys
import warnings
from datetime import datetime
import pandas as pd
from google.cloud import bigquery
from IPython.core.magic import Magics, line_cell_magic, magics_class
try:
    from traitlets.config.configurable import Configurable
    from traitlets import Bool, Int, Unicode
except ImportError:
    from IPython.config.configurable import Configurable
    from IPython.utils.traitlets import Bool, Int, Unicode

__version__ = "0.1.1"

@magics_class
class BigqueryMagic(Magics, Configurable):
    autolimit = Int(
        10000,
        config=True,
        allow_none=True,
        help="Automatically limit the number of rows to be returned (Set None to retrieve all rows)"
    )
    showtime = Bool(
        True,
        config=True,
        help="Show execution time message"
    )
    showbytes = Bool(
        True,
        config=True,
        help="Show total bytes after execution"
    )
    showquery = Bool(
        False,
        config=True,
        help="Show query to run"
    )
    localjson = Unicode(
        None,
        config=True,
        allow_none=True,
        help="Local json file for authenticating to bigquery"
    )

    @line_cell_magic
    def bq(self, line, cell=""):
        query = line or cell
        if self.showquery:
            print(f"Running query: {query}", file=sys.stderr)

        t1 = datetime.now()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # This is to avoid the warning:
            #   Your application has authenticated using end user credentials from Google Cloud SDK without a quota project
            if self.localjson is not None:
                client = bigquery.Client.from_service_account_json(self.localjson)
            else:
                client = bigquery.Client()
            job = client.query(query)
            if self.showtime:
                print(f"Start query at {t1}", file=sys.stderr)
        job.result() # wait until the job finshes
        t2 = datetime.now()
        if self.showtime and self.showbytes:
            print(f"End query at {t2} (Execution time: {t2-t1}, Processed: {round(job.total_bytes_processed/1024**3, 1)} GB)", file=sys.stderr)
        elif self.showtime:
            print(f"End query at {t2} (Execution time: {t2-t1})", file=sys.stderr)
        elif self.showbytes:
            print(f"Processed: {round(job.total_bytes_processed/1024**3, 1)} GB", file=sys.stderr)

        data = []
        for i, row in enumerate(job):
            if self.autolimit is not None and i > self.autolimit:
                print(f"Result is truncated at the row {self.autolimit}", file=sys.stderr)
                break
            data.append(dict(row.items()))
        if len(data) == 0:
            return None  # No result returned
        return pd.DataFrame(data)


def load_ipython_extension(ipython):
    ipython.register_magics(BigqueryMagic)
