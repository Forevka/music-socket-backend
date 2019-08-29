from multiprocessing import Pool, Process
from http_server_start import run_http_server
from websocket_server import run_websocket_server


if __name__=="__main__":
    process_amount = 0
    p = Process(target=run_http_server)
    p.start()
    p = Process(target=run_websocket_server)
    p.start()
