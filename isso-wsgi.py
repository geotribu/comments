#! python3

"""
    WSGI script to allow launch isso through Apache mod_wsgi.
"""

import site

site.addsitedir("./.venv")

import os
from pathlib import Path

from isso import config, dist, make_app

# globals
isso_conf_file = Path(__file__).parent / "isso-prod.cfg"

application = make_app(
    config.load(
        default=os.path.join(dist.location, dist.project_name, "defaults.ini"),
        user=str(isso_conf_file.resolve()),
    ),
    multiprocessing=True,
    threading=True,
)
