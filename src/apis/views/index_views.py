import logging
import os
from apis.decorators import private


logger = logging.getLogger("default")
app_name = os.environ.get("APPLICATION_NAME")


@private
def index():
    logger.info("Checking the {} logger".format(app_name))
    return "Welcome to the {} application".format(app_name)