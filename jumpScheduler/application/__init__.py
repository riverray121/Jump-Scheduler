# jumpScheduler/application/__init__.py 

""" Initiation of application 
"""

import os

from flask import Flask

from .config import Config

application = Flask(__name__)

# load Configuration
application.config.from_object( Config ) 

# Import routing to render the pages
from application import routes