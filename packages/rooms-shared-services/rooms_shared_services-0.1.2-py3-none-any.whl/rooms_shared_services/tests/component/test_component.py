import socket
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

def test_component():
    port = 8000
    host = "main_component_run"
    timeout = 2
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #presumably 
    sock.settimeout(timeout)
    try:
        logger.info("Connection attempt")
        sock.connect((host,port))
    except:
        logger.info("Connection failed")
        assert False
    else:
        sock.close()
        logger.info("Connection succeded")        
        assert True