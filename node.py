from threading import Thread
from datetime import datetime
from udp import Udp

import socket, time

class Node(Udp):
  id: str = None
  address: tuple = None
  host: tuple = None
  peers: dict = {}
  peer_socket: socket.socket = {}

  thread_receive: Thread = None
  thread_send: Thread = None

  alive: bool = True

  def __init__(self, id: str, ip: str, port: int, ip_host: str, port_host: int, __private: bool = False) -> None:
    if not __private: raise RuntimeError('Try Node.create()')

    self.id = id
    self.address = (ip, port)
    self.host = (ip_host, port_host)

  def __start_threads(self) -> None:
    self.thread_receive = Thread(target=self.__receive).start()
    self.thread_send = Thread(target=self.__send).start()
  
  def __to_tuple(self, dict: dict) -> None:
    for attribute in dict.keys():
      dict[attribute] = tuple(dict[attribute])

  def __receive(self) -> None:
    while self.alive:
      peer_addr, peer_json = self.receive_json(self.peer_socket)

      if peer_json['type'] == 'newpeer':
        self.peers[peer_json['data']] = peer_addr
        self.send_json(self.peer_socket, peer_addr, {
          "type": "peers",
          "data": self.peers
        })

      elif peer_json['type'] == 'peers':
        self.__to_tuple(peer_json["data"])
        self.peers.update(peer_json['data'])
        self.broadcast_json(self.peer_socket, self.peers, {
          "type": "introduce",
          "data": self.id,
        })

      elif peer_json['type'] == 'introduce':
        self.peers[peer_json['data']] = peer_addr
        print(f'{peer_json["data"]} entrou no Chat!')

      elif peer_json['type'] == 'input':
        if self.id != peer_json['user']:
          now = datetime.now()
          formatted_now = now.strftime('%d/%m/%y, %H:%M')
          print(f'[{formatted_now}] <{peer_json["user"]}>: {peer_json["data"]}')

      elif peer_json['type'] == 'exit':
        try:
          self.peers.pop(peer_json['data'])
          print(f'{peer_json["data"]} saiu do Chat!')
        except: pass

  def __send(self) -> None:
    while self.alive:
      try:
        message = input("$: ").strip()

        if message == '': continue

        elif message == 'exit':
          try:
            self.broadcast_json(self.peer_socket, self.peers, {
              "type": "exit",
              "data": self.id
            })
          except: pass
          self.alive = False
          time.sleep(0.5)
          break

        self.broadcast_json(self.peer_socket, self.peers, {
          "type": "input",
          "user": self.id,
          "data": message
        })
      except KeyboardInterrupt:
        print('type "exit" to leave!')

  def start(self) -> None:
    if self.host[0] == None:
      self.peers[self.id] = self.address
    else:
      self.send_json(self.peer_socket, self.host, {
        "type": "newpeer",
        "data": self.id
      })

    self.__start_threads()

  @staticmethod
  def create(id: str, ip: str, port: int, ip_host: str, port_host: int) -> 'Node':
    new_node = Node(id, ip, port, ip_host, port_host, True)

    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    peer_socket.bind((ip, port))

    new_node.peer_socket = peer_socket

    return new_node