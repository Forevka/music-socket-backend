from multiprocessing import Pool, Process
from http_server_start import run_http_server
from websocket_server import run_websocket_server
from DBdriver.db_worker import DBWorker
import requests
import json


if __name__=="__main__":
    db = DBWorker()
    # print(db.get_channel_list(page = 1, sort_by = 'name', asc = True))
    '''
    # users = json.loads(requests.get("https://randomuser.me/api/?results=100&inc=login,email").text)['results']
    channels = json.loads(requests.get("http://names.drycodes.com/120").text)
    films = json.loads(requests.get("http://names.drycodes.com/120?nameOptions=films").text)
    for i in range(0, 100, 1):
        print(i)
        try:
            db.add_channel(channels[i].replace("_", " "), description = films[i].replace("_", " "))
        except:
            pass
    '''
    process_amount = 0
    p = Process(target=run_http_server)
    p.start()
    p = Process(target=run_websocket_server)
    p.start()
