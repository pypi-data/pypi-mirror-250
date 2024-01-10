from optparse import OptionParser

from DataTransfer.network.network import SenderNetwork, ReceiverNetwork
from DataTransfer.transferer.sender import SenderTransferer
from DataTransfer.transferer.receiver import ReiceiverTransferer


def return_arguments():
    parser = OptionParser()
    parser.add_option('--sender', dest='sender', action='store_true', help='sender')
    parser.add_option('--receiver', dest='receiver', action='store_true', help='receiver')
    parser.add_option('-p', '--port', dest='port', type=int, help='port')
    parser.add_option('-i', '--ip', dest='ip', help='ip address')
    parser.add_option('-m', '--max-receiver', dest='max_receiver', type=int, help='Set the maximum of receiver')
    options = parser.parse_args()[0]
    _check_arguments(options, parser)
    return options


def _check_arguments(options, parser):
    if not options.sender and not options.receiver:
        parser.error('[-] Role not found')
    if options.sender and options.receiver:
        parser.error('[-] Choose one option only "--send" or "--receive"')
    if not options.port:
        parser.error('[-] Port not found')
    if not options.ip:
        parser.error('[-] Ip address not found')
    if not options.max_receiver and options.sender:
        parser.error('[-] Maximum receiver not found')


def run_sender(ip, port, max_receiver):
    network = SenderNetwork(ip, port)
    sender = SenderTransferer(network, max_receiver)
    sender.run()


def run_receiver(ip, port):
    network = ReceiverNetwork(ip, port)
    receiver = ReiceiverTransferer(network)
    receiver.run()


def main():
    options = return_arguments()

    ip = options.ip
    port = options.port
    max_receiver = options.max_receiver if options.max_receiver else None

    if options.sender:
        run_sender(ip, port, max_receiver)
    elif options.receiver:
        run_receiver(ip, port)


if __name__ == '__main__':
    main()
