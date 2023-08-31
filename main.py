from cli import arguments
from node import Node

def main(args):
  node = Node.create(args.NICKNAME, args.IP, args.PORT, args.IP_HOST, args.PORT_HOST)
  node.start()

if __name__ == '__main__':
  args = arguments()
  main(args)