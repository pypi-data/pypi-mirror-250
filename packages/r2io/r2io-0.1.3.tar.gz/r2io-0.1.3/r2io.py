import glob
import itertools
import operator
import os
import types

import numpy

status_messages = types.MappingProxyType({
  b'4D': '{: >16}'.format('OK')
})

gnss_status_messages = types.MappingProxyType({
  b'6': '{: >16}'.format('OFF'),
  b'7': '{: >16}'.format('ON')
})

filter_messages = types.MappingProxyType({
  b'3': '{: >16}'.format('LPF+HPF'),
  b'2': '{: >16}'.format('LPF'),
  b'1': '{: >16}'.format('SINC'),
  b'0': '{: >16}'.format('')
})

gnss_quality_messages = types.MappingProxyType({
  b'B': '{: >16}'.format('STANDARD'),
  b'A': '{: >16}'.format('DIFFERTIAL')
})

channel_messages = types.MappingProxyType({
  b'8': '{: >16}'.format('INTERNAL')
})

R2EncodedDtype = numpy.dtype([
  ('file_type', 'S2'), # 2
  ('line_number', 'S10'), # 12
  ('point_number', 'S10'), # 22
  ('measurement_longitude', 'S11'), # 33
  ('measurement_latitude', 'S11'), # 44
  ('measurement_elevation', 'S6'), # 50
  ('serial_number', 'S10'), # 60
  ('status_code', 'S2'), # 62
  ('deployment_longitude', 'S20'), # 82
  ('deployment_latidude', 'S11'), # 93
  ('deployment_elevation', 'S6'), # 99
  ('date_time', '(6,)S2'), # 111
  ('deployment_line_number', 'S4'), # 115, byte swapped
  ('deployment_point_number', 'S4'), # 119, byte swapped
  ('geophone_resistance', 'S2'), # 121, normal
  ('voltage', 'S2'), # 123
  ('temperature', 'S2'), # 125, t + 50
  ('storage_status', 'S2'), # 127
  #
  ('unkown0', 'S8'), # 135
  #
  ('tilt_angle', 'S2'), # 137, 2t - 256
  #
  ('gnss_status', 'S1'), # 138 
  ('unkown1', 'S1'),
  ('sampling_interval', 'S1'), # 139
  ('filter', 'S1'), # 140
  ('geophone_channel', 'S1'), # 141
  ('gain', 'S1'), # 142
  ('gnss_quality', 'S1'), # 143
  ('gnss_num_gsu', 'S1'), # 144
  ('gnss_num_gsv', 'S2'), # 146
  #
  ('gnss_time', '(6,)S2'), # 158
  ('device_longitude', 'S8'), # 166
  ('device_latitude', 'S8'), # 174
  ('unkown2', 'V2'), # 176
  ('unkown3', 'S8'), # 184
  ('unkown4', 'V11') # 196
])

R2DecodedDtype = numpy.dtype([
  ('line_number', '<u4'),
  ('point_number', '<u4'),
  ('measurement_longitude', '<f8'),
  ('measurement_latitude', '<f8'),
  ('measurement_elevation', '<f8'),
  ('serial_number', 'S8'),
  ('status_code', 'S2'),
  ('deployment_longitude', '<f8'),
  ('deployment_latidude', '<f8'),
  ('deployment_elevation', '<f8'),
  ('date_time', '(6,)<u4'),
  ('deployment_line_number', '<u4'),
  ('deployment_point_number', '<u4'),
  ('voltage', '<u4'),
  ('temperature', '<u4'),
  ('storage_status', 'S16'),
  ('tilt_angle', '<u4'),
  ('gnss_status', 'S16'),
  ('sampling_interval', '<f8'),
  ('filter', 'S16'),
  ('geophone_channel', 'S16'),
  ('gain', '<u4'),
  ('gnss_quality', 'S16'),
  ('gnss_num_gsu', '<u4'),
  ('gnss_num_gsv', '<u4'),
  ('gnss_time', '(6,)<u4'),
  ('device_longitude', '<f8'),
  ('device_latitude', '<f8'),
])

def __pairwise(buffer: bytes) -> bytes:
  '''
  Batch a buffer into pairs of bytes.

  Parameters:
    buffer (bytes): The buffer to batch.

  Returns:
    pairs (list[bytes]): Pairs of bytes from the buffer.
  '''
  length = len(buffer) // 2
  pairs = [b''] * length
  for i in range(length):
    pairs[i] = buffer[2 * i:2 * (i + 1)]
  return pairs 

def __swap_pairs_of_bytes(buffer: bytes) -> bytes:
  '''
  Swap every pair of bytes in a buffer. 

  Parameters:
    buffer (bytes): The buffer to byteswap.

  Returns:
    buffer (bytes): A new buffer with the bytes swapped.
  '''
  pairs = __pairwise(buffer)
  swapped = b''.join(itertools.starmap(
    lambda x, y: b''.join((y, x)), 
    zip(pairs[0::2], pairs[1::2])
  ))

  return swapped

def __load_buffer(fname: str) -> bytes:
  '''
  Load a file into a memory buffer.

  Parameters:
    fname (str): The absolute or relative path to the file.

  Returns:
    buffer (bytes): The bytes representation of the file.
  '''
  with open(fname, 'r+b') as buffer:
    return buffer.read()

def __hex_to_decimal_degrees(buffer: bytes) -> float:
  '''
  Decode coordinate data from hexadecimal.

  Parameters:
    buffer (bytes): The ascii/hex representation of the coordinates.

  Returns:
    coordinate (float): The decimal representation of the coordinate.
  '''
  pairs = __pairwise(buffer)
  coordinate_bytes = b''.join(reversed(pairs))
  coordinate_sign_nibble = coordinate_bytes[0]
  coordinate_sign = -1 if coordinate_sign_nibble == 2 else 1
  coordinate_as_int = str(int(coordinate_bytes[1:], 16))
  coordinate_minutes = coordinate_as_int[-6:]
  coordinate_minutes_as_float = float(coordinate_minutes[:2] + '.' + coordinate_minutes[2:])
  coordinate_degrees = int(coordinate_as_int[:-6])
  coordinate = coordinate_sign * (coordinate_degrees + coordinate_minutes_as_float / 60)
  return coordinate

def __decode_buffer(buffer: bytes) -> tuple:
  '''
  Decode an r2 file stored in a memory buffer.

  Parameters:
    buffer (bytes): The r2 file in memory.

  Returns:  
    r2s (numpy.array): The r2 file as a numpy dtype array.
  '''
  flatbuffer = b''.join(buffer.splitlines())
  lines = numpy.frombuffer(flatbuffer, dtype=R2EncodedDtype)
  return numpy.array([(
    line['line_number'].astype('<u4'),
    line['point_number'].astype('<u4'),
    line['measurement_longitude'].astype('<f8'),
    line['measurement_latitude'].astype('<f8'),
    line['measurement_elevation'].astype('<f8'),
    line['serial_number'],
    line['status_code'],
    line['deployment_longitude'].astype('<f8'),
    line['deployment_latidude'].astype('<f8'),
    line['deployment_elevation'].astype('<f8'),
    line['date_time'].astype('<u4'),
    int(__swap_pairs_of_bytes(line['deployment_line_number']), 16),
    int(__swap_pairs_of_bytes(line['deployment_point_number']), 16),
    int(line['voltage'], 16),
    int(line['temperature'], 16) - 50,
    status_messages[line['storage_status']],
    2 * int(line['tilt_angle'], 16) - 256,
    gnss_status_messages[line['gnss_status']],
    (0.25 * 4 ** (2 - int(line['sampling_interval'], 16))),
    filter_messages[line['filter']],
    channel_messages[line['geophone_channel']],
    int(line['gain'], 16),
    gnss_quality_messages[line['gnss_quality']],
    int(line['gnss_num_gsu'], 16),
    int(line['gnss_num_gsv'], 16),
    [int(i, 16) for i in line['gnss_time']], # By pair
    __hex_to_decimal_degrees(line['device_longitude']),
    __hex_to_decimal_degrees(line['device_latitude']),
  ) for line in lines], dtype=R2DecodedDtype)

def read(fnmatch: str) -> numpy.array:
  '''
  Read/decode r2 files.

  Parameters:
    fnmatch (str): The unix like path/pattern to match r2 files. Multiple 
      files will be resolved.

  Returns:
    r2 (numpy.array): Information decoded from the r2 files in a single array.
  '''
  if not (files := glob.glob(fnmatch)):
    raise ValueError('File not found.')

  for file in files:
    _, ext = os.path.splitext(file)
    if not (ext == '.r2'):
      raise ValueError('Incorrect file type.')

  return numpy.vstack([__decode_buffer(__load_buffer(file)) for file in files])

