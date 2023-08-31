import argparse

IP    = '127.0.0.1'
PORT  = 8080

def arguments():
  parser = argparse.ArgumentParser()

  parser.add_argument('--NICKNAME', '-n', help='Define Node Nickname, Default: Host', type=str, default='Host')
  parser.add_argument('--IP', '-ip', help=f'Define Node IP, Default: {IP}', type=str, default=IP)
  parser.add_argument('--PORT', '-p', help=f'Define Node PORT, Default: {PORT}', type=int, default=PORT)
  parser.add_argument('--IP_HOST', '-iph', help='Define Host IP', type=str)
  parser.add_argument('--PORT_HOST', '-pth', help=f'Define Host PORT, Default: {PORT}', type=int, default=PORT)

  args = parser.parse_args()
  return args