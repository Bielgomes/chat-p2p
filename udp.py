import socket, json
from typing import Dict, Tuple

BUFF = 3072

class Udp:
  def __receive_json(self, peer_socket: socket.socket) -> Tuple[bytes, any]:
    return peer_socket.recvfrom(BUFF)
  
  def __send_json(self, peer_socket: socket.socket, peer: socket.socket, message: str) -> None:
    peer_socket.sendto(message.encode(), peer)

  def receive_json(self, peer_socket: socket.socket) -> Tuple[bytes, any]:
    data, addr = self.__receive_json(peer_socket)
    
    data = json.loads(data)
    return addr, data

  def send_json(self, peer_socket: socket.socket, peer: socket.socket, message: dict):
    self.__send_json(peer_socket, peer, json.dumps(message))

  def broadcast_json(self, peer_socket: socket.socket, peers: Dict[str, socket.socket], message: dict):
    for peer in peers:
      self.send_json(peer_socket, peers[peer], message)