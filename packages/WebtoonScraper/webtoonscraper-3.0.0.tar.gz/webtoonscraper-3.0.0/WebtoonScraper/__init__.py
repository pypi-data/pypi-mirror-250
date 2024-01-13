"""
░██╗░░░░░░░██╗███████╗██████╗░████████╗░█████╗░░█████╗░███╗░░██╗░██████╗░█████╗░██████╗░░█████╗░██████╗░███████╗██████╗░
░██║░░██╗░░██║██╔════╝██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗████╗░██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
░╚██╗████╗██╔╝█████╗░░██████╦╝░░░██║░░░██║░░██║██║░░██║██╔██╗██║╚█████╗░██║░░╚═╝██████╔╝███████║██████╔╝█████╗░░██████╔╝
░░████╔═████║░██╔══╝░░██╔══██╗░░░██║░░░██║░░██║██║░░██║██║╚████║░╚═══██╗██║░░██╗██╔══██╗██╔══██║██╔═══╝░██╔══╝░░██╔══██╗
░░╚██╔╝░╚██╔╝░███████╗██████╦╝░░░██║░░░╚█████╔╝╚█████╔╝██║░╚███║██████╔╝╚█████╔╝██║░░██║██║░░██║██║░░░░░███████╗██║░░██║
░░░╚═╝░░░╚═╝░░╚══════╝╚═════╝░░░░╚═╝░░░░╚════╝░░╚════╝░╚═╝░░╚══╝╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚══════╝╚═╝░░╚═╝

Scrape webtoons with ease.
"""  # noqa

from .directory_merger import DirectoryMerger
from .webtoon_viewer import add_html_webtoon_viewer
from .miscs import (
    __title__,
    __description__,
    __url__,
    __version_info__,
    __version__,
    __author__,
    __author_email__,
    __license__,
    __github_user_name__,
    __github_project_name__,
)

import sys as _sys
import nest_asyncio as _nest_asyncio

_nest_asyncio.apply()

if _sys.version_info < (3, 11, 0):
    import logging

    logging.warning(
        f"Python version ({_sys.version}) is too low. Program may be run but not tested. "
        "Upgrade Python if program not works well."
    )
