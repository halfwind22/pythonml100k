import logging

logging.basicConfig(filename="run_etl.log",
                    format='%(asctime)s %(message)s',
                    filemode='a+')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
