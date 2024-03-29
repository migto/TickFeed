# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rcvdata.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='rcvdata.proto',
  package='tornadofeed',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\rrcvdata.proto\x12\x0btornadofeed\"\xff\x04\n\tRcvReport\x12\x0f\n\x07\x63\x62_size\x18\x01 \x01(\r\x12\x0c\n\x04time\x18\x02 \x01(\r\x12\x0e\n\x06market\x18\x03 \x01(\r\x12\r\n\x05label\x18\x04 \x01(\x0c\x12\x0c\n\x04name\x18\x05 \x01(\x0c\x12\x12\n\nlast_close\x18\x06 \x01(\x02\x12\x0c\n\x04open\x18\x07 \x01(\x02\x12\x0c\n\x04high\x18\x08 \x01(\x02\x12\x0b\n\x03low\x18\t \x01(\x02\x12\x11\n\tnew_price\x18\n \x01(\x02\x12\x0e\n\x06volume\x18\x0b \x01(\x02\x12\x0e\n\x06\x61mount\x18\x0c \x01(\x02\x12\x13\n\x0b\x62uy_price_1\x18\r \x01(\x02\x12\x13\n\x0b\x62uy_price_2\x18\x0e \x01(\x02\x12\x13\n\x0b\x62uy_price_3\x18\x0f \x01(\x02\x12\x13\n\x0b\x62uy_price_4\x18\x10 \x01(\x02\x12\x13\n\x0b\x62uy_price_5\x18\x11 \x01(\x02\x12\x14\n\x0c\x62uy_volume_1\x18\x12 \x01(\x02\x12\x14\n\x0c\x62uy_volume_2\x18\x13 \x01(\x02\x12\x14\n\x0c\x62uy_volume_3\x18\x14 \x01(\x02\x12\x14\n\x0c\x62uy_volume_4\x18\x15 \x01(\x02\x12\x14\n\x0c\x62uy_volume_5\x18\x16 \x01(\x02\x12\x14\n\x0csell_price_1\x18\x17 \x01(\x02\x12\x14\n\x0csell_price_2\x18\x18 \x01(\x02\x12\x14\n\x0csell_price_3\x18\x19 \x01(\x02\x12\x14\n\x0csell_price_4\x18\x1a \x01(\x02\x12\x14\n\x0csell_price_5\x18\x1b \x01(\x02\x12\x15\n\rsell_volume_1\x18\x1c \x01(\x02\x12\x15\n\rsell_volume_2\x18\x1d \x01(\x02\x12\x15\n\rsell_volume_3\x18\x1e \x01(\x02\x12\x15\n\rsell_volume_4\x18\x1f \x01(\x02\x12\x15\n\rsell_volume_5\x18  \x01(\x02\"4\n\x07RcvData\x12)\n\tlstReport\x18\x01 \x03(\x0b\x32\x16.tornadofeed.RcvReportb\x06proto3')
)




_RCVREPORT = _descriptor.Descriptor(
  name='RcvReport',
  full_name='tornadofeed.RcvReport',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cb_size', full_name='tornadofeed.RcvReport.cb_size', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='time', full_name='tornadofeed.RcvReport.time', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='market', full_name='tornadofeed.RcvReport.market', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='label', full_name='tornadofeed.RcvReport.label', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='tornadofeed.RcvReport.name', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='last_close', full_name='tornadofeed.RcvReport.last_close', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='open', full_name='tornadofeed.RcvReport.open', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='high', full_name='tornadofeed.RcvReport.high', index=7,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='low', full_name='tornadofeed.RcvReport.low', index=8,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='new_price', full_name='tornadofeed.RcvReport.new_price', index=9,
      number=10, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='volume', full_name='tornadofeed.RcvReport.volume', index=10,
      number=11, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='amount', full_name='tornadofeed.RcvReport.amount', index=11,
      number=12, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='buy_price_1', full_name='tornadofeed.RcvReport.buy_price_1', index=12,
      number=13, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='buy_price_2', full_name='tornadofeed.RcvReport.buy_price_2', index=13,
      number=14, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='buy_price_3', full_name='tornadofeed.RcvReport.buy_price_3', index=14,
      number=15, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='buy_price_4', full_name='tornadofeed.RcvReport.buy_price_4', index=15,
      number=16, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='buy_price_5', full_name='tornadofeed.RcvReport.buy_price_5', index=16,
      number=17, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='buy_volume_1', full_name='tornadofeed.RcvReport.buy_volume_1', index=17,
      number=18, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='buy_volume_2', full_name='tornadofeed.RcvReport.buy_volume_2', index=18,
      number=19, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='buy_volume_3', full_name='tornadofeed.RcvReport.buy_volume_3', index=19,
      number=20, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='buy_volume_4', full_name='tornadofeed.RcvReport.buy_volume_4', index=20,
      number=21, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='buy_volume_5', full_name='tornadofeed.RcvReport.buy_volume_5', index=21,
      number=22, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sell_price_1', full_name='tornadofeed.RcvReport.sell_price_1', index=22,
      number=23, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sell_price_2', full_name='tornadofeed.RcvReport.sell_price_2', index=23,
      number=24, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sell_price_3', full_name='tornadofeed.RcvReport.sell_price_3', index=24,
      number=25, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sell_price_4', full_name='tornadofeed.RcvReport.sell_price_4', index=25,
      number=26, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sell_price_5', full_name='tornadofeed.RcvReport.sell_price_5', index=26,
      number=27, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sell_volume_1', full_name='tornadofeed.RcvReport.sell_volume_1', index=27,
      number=28, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sell_volume_2', full_name='tornadofeed.RcvReport.sell_volume_2', index=28,
      number=29, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sell_volume_3', full_name='tornadofeed.RcvReport.sell_volume_3', index=29,
      number=30, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sell_volume_4', full_name='tornadofeed.RcvReport.sell_volume_4', index=30,
      number=31, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sell_volume_5', full_name='tornadofeed.RcvReport.sell_volume_5', index=31,
      number=32, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=31,
  serialized_end=670,
)


_RCVDATA = _descriptor.Descriptor(
  name='RcvData',
  full_name='tornadofeed.RcvData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='lstReport', full_name='tornadofeed.RcvData.lstReport', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=672,
  serialized_end=724,
)

_RCVDATA.fields_by_name['lstReport'].message_type = _RCVREPORT
DESCRIPTOR.message_types_by_name['RcvReport'] = _RCVREPORT
DESCRIPTOR.message_types_by_name['RcvData'] = _RCVDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RcvReport = _reflection.GeneratedProtocolMessageType('RcvReport', (_message.Message,), {
  'DESCRIPTOR' : _RCVREPORT,
  '__module__' : 'rcvdata_pb2'
  # @@protoc_insertion_point(class_scope:tornadofeed.RcvReport)
  })
_sym_db.RegisterMessage(RcvReport)

RcvData = _reflection.GeneratedProtocolMessageType('RcvData', (_message.Message,), {
  'DESCRIPTOR' : _RCVDATA,
  '__module__' : 'rcvdata_pb2'
  # @@protoc_insertion_point(class_scope:tornadofeed.RcvData)
  })
_sym_db.RegisterMessage(RcvData)


# @@protoc_insertion_point(module_scope)
