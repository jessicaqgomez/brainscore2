import json
from pythonosc import dispatcher
from pythonosc import osc_server


# ----------------------------------------------------------------------
def read_stream(url, data):
    """"""
    data = json.loads(data)
    print(data)


dispatcher = dispatcher.Dispatcher()
dispatcher.map("/BrainRhythms", read_stream)
server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 5005), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()
