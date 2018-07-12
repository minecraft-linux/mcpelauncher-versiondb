import subprocess
import re
import struct

split_regex = re.compile("^\s*\d*: ([0-9a-f]{8})\s*\d+ \w+\s+\w+\s+\w+\s+\w+ (.*)$")

def get_value_at(file, offset, size, format):
    if offset == None or offset < 0:
        return -1
    file.seek(offset)
    return struct.unpack(format, file.read(size))[0]

def get_so_info(path):
    cmd = subprocess.Popen(['readelf', '-Ws', path], stdout=subprocess.PIPE)
    beta_off = None
    protocol_ver_off = None
    chunk_format_ver_off = None
    subchunk_format_ver_off = None
    for line in cmd.stdout:
        parts = split_regex.match(line.decode('utf-8'))
        if parts == None:
            continue
        symbol = parts.group(2)
        if symbol == "_ZN15SharedConstants6IsBetaE":
            beta_off = int(parts.group(1), 16)
        if symbol == "_ZN15SharedConstants22NetworkProtocolVersionE":
            protocol_ver_off = int(parts.group(1), 16)
        if symbol == "_ZN15SharedConstants23CurrentLevelChunkFormatE":
            chunk_format_ver_off = int(parts.group(1), 16)
        if symbol == "_ZN15SharedConstants21CurrentSubChunkFormatE":
            subchunk_format_ver_off = int(parts.group(1), 16)

    if beta_off == None:
        return False
    with open(path, 'rb') as file:
        return {
                "is_beta": (get_value_at(file, beta_off, 1, 'B') == 1),
                "protocol_ver": get_value_at(file, protocol_ver_off, 4, 'i'),
                "chunk_format_ver": get_value_at(file, chunk_format_ver_off, 1, 'B'),
                "subchunk_format_ver": get_value_at(file, subchunk_format_ver_off, 1, 'B')
        }

