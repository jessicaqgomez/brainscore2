from pythonosc.udp_client import SimpleUDPClient


########################################################################
class OSCStreamer(SimpleUDPClient):
  """"""

  # ----------------------------------------------------------------------
  def __init__(self, ip, port):
    """Constructor"""
    super().__init__(ip, port)

  # ----------------------------------------------------------------------
  def write(self, data):
    """"""
    self.send_message("/BrainRhythms", data)

