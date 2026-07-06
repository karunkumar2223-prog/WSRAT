import logging

logging.basicConfig(

    filename="logs/wsrat.log",

    level=logging.INFO,

    format="%(asctime)s %(levelname)s %(message)s"

)

logger = logging.getLogger("WSRAT")