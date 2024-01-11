import _toori

import urllib
import socket
import asyncio
import socketio
import re
from concurrent.futures import ThreadPoolExecutor

# Increase the packet buffer
from engineio.payload import Payload

Payload.max_decode_packets = 2500000

_executor = ThreadPoolExecutor(1)

sio = socketio.AsyncClient()

loop = asyncio.get_event_loop()

LOCAL_IP = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
IPV4_REGEX = re.compile(r"((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}")
# TODO: Add IPV6 regex


def resolve_address(address):
    hostname = address.split("//")[-1:][0].split(":")[0]
    ip = socket.gethostbyname(hostname)

    return ip


def is_valid_ip(ip: str) -> bool:
    try:
        if IPV4_REGEX.match(ip):
            socket.inet_aton(ip)
            return True
    except socket.error:
        pass
    return False


@sio.on("message")
async def print_message(msg):
    print(msg)


@sio.on("connect")
async def on_connect():
    print("Connected to server")


@sio.on("in")
async def handle_incoming(data):
    # await loop.run_in_executor(_executor, _toori.inj, data)
    _toori.inj(data)
    # await asyncio.sleep(0.0)


async def start_client(address, requested_ip, filter_string):
    headers = {"req_ip": requested_ip, "loc_ip": LOCAL_IP}

    try:
        await sio.connect(f"{address}", auth=headers)
    except socketio.exceptions.ConnectionError:
        print(f"Unable to connect to the address {address}")
        exit()

    _toori.init(
        filter_string,
        LOCAL_IP,
    )

    while True:
        data = await loop.run_in_executor(_executor, _toori.get)
        # data = _toori.get()
        if len(data) > 0:
            try:
                await sio.emit(event="out", data=data)
            except Exception:
                pass

        # await asyncio.sleep(0.0001)


def start(address, filter_string=None, requested_ip=None, no_dns=False):
    parsed_url = urllib.parse.urlparse(address)
    server_port = parsed_url.port

    if not parsed_url.scheme:
        address = f"https://{address}"

    # Derive port if not explicitly stated in url
    if not server_port:
        if parsed_url.scheme == "http":
            server_port = 80
        else:
            server_port = 443

    base_filter = "outbound && !loopback"

    # Only resolve address if domain name is given
    filter_ip = address if is_valid_ip(address) else resolve_address(address)

    # Whitelist encapsulated tunnel traffic from being intercepted by WinDivert
    base_filter += f" && (ip.DstAddr != {filter_ip} || tcp.DstPort != {server_port})"

    if filter_string is None:
        filter_string = "ip"

    if no_dns:
        filter_string += " && (!udp || udp.DstPort != 53)"

    try:
        loop.run_until_complete(start_client(address, requested_ip, f"{base_filter} && {filter_string}"))
    except KeyboardInterrupt:
        _toori.stop()
        print("Exited, have a nice day :)")
