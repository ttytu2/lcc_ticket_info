import logging.config
import ConfigParser
from .logging_config import LoggingConfig

logging.config.dictConfig(LoggingConfig)

ticket_config = ConfigParser.ConfigParser()
ticket_config.read('/data/config/lcc-ticket-info/config.properties')

