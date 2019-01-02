# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: getDepo.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='getDepo.proto',
  package='qlua.rpc.getDepo',
  syntax='proto3',
  serialized_options=_b('\n\010qlua.rpcH\001'),
  serialized_pb=_b('\n\rgetDepo.proto\x12\x10qlua.rpc.getDepo\"\xf1\x01\n\x04\x44\x65po\x12#\n\x1b\x64\x65po_limit_locked_buy_value\x18\x01 \x01(\t\x12\x1c\n\x14\x64\x65po_current_balance\x18\x02 \x01(\t\x12\x1d\n\x15\x64\x65po_limit_locked_buy\x18\x03 \x01(\t\x12\x19\n\x11\x64\x65po_limit_locked\x18\x04 \x01(\t\x12\x1c\n\x14\x64\x65po_limit_available\x18\x05 \x01(\t\x12\x1a\n\x12\x64\x65po_current_limit\x18\x06 \x01(\t\x12\x19\n\x11\x64\x65po_open_balance\x18\x07 \x01(\t\x12\x17\n\x0f\x64\x65po_open_limit\x18\x08 \x01(\t\"R\n\x07Request\x12\x13\n\x0b\x63lient_code\x18\x01 \x01(\t\x12\x0e\n\x06\x66irmid\x18\x02 \x01(\t\x12\x10\n\x08sec_code\x18\x03 \x01(\t\x12\x10\n\x08trdaccid\x18\x04 \x01(\t\".\n\x06Result\x12$\n\x04\x64\x65po\x18\x01 \x01(\x0b\x32\x16.qlua.rpc.getDepo.DepoB\x0c\n\x08qlua.rpcH\x01\x62\x06proto3')
)




_DEPO = _descriptor.Descriptor(
  name='Depo',
  full_name='qlua.rpc.getDepo.Depo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='depo_limit_locked_buy_value', full_name='qlua.rpc.getDepo.Depo.depo_limit_locked_buy_value', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='depo_current_balance', full_name='qlua.rpc.getDepo.Depo.depo_current_balance', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='depo_limit_locked_buy', full_name='qlua.rpc.getDepo.Depo.depo_limit_locked_buy', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='depo_limit_locked', full_name='qlua.rpc.getDepo.Depo.depo_limit_locked', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='depo_limit_available', full_name='qlua.rpc.getDepo.Depo.depo_limit_available', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='depo_current_limit', full_name='qlua.rpc.getDepo.Depo.depo_current_limit', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='depo_open_balance', full_name='qlua.rpc.getDepo.Depo.depo_open_balance', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='depo_open_limit', full_name='qlua.rpc.getDepo.Depo.depo_open_limit', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=36,
  serialized_end=277,
)


_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='qlua.rpc.getDepo.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='client_code', full_name='qlua.rpc.getDepo.Request.client_code', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='firmid', full_name='qlua.rpc.getDepo.Request.firmid', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sec_code', full_name='qlua.rpc.getDepo.Request.sec_code', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trdaccid', full_name='qlua.rpc.getDepo.Request.trdaccid', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=279,
  serialized_end=361,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='qlua.rpc.getDepo.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='depo', full_name='qlua.rpc.getDepo.Result.depo', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=363,
  serialized_end=409,
)

_RESULT.fields_by_name['depo'].message_type = _DEPO
DESCRIPTOR.message_types_by_name['Depo'] = _DEPO
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Depo = _reflection.GeneratedProtocolMessageType('Depo', (_message.Message,), dict(
  DESCRIPTOR = _DEPO,
  __module__ = 'getDepo_pb2'
  # @@protoc_insertion_point(class_scope:qlua.rpc.getDepo.Depo)
  ))
_sym_db.RegisterMessage(Depo)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'getDepo_pb2'
  # @@protoc_insertion_point(class_scope:qlua.rpc.getDepo.Request)
  ))
_sym_db.RegisterMessage(Request)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'getDepo_pb2'
  # @@protoc_insertion_point(class_scope:qlua.rpc.getDepo.Result)
  ))
_sym_db.RegisterMessage(Result)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)