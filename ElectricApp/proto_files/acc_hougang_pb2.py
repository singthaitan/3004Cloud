# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: acc_hougang.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11\x61\x63\x63_hougang.proto\x12\x0b\x61\x63\x63_hougang\"0\n\rLogin_Request\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"\x1e\n\x0bLogin_Reply\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\xae\x01\n\x10Register_Request\x12\x12\n\nfirst_name\x18\x01 \x01(\t\x12\x11\n\tlast_name\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t\x12\x10\n\x08password\x18\x04 \x01(\t\x12\x0e\n\x06region\x18\x05 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x06 \x01(\t\x12\x0c\n\x04unit\x18\x07 \x01(\t\x12\x0e\n\x06postal\x18\x08 \x01(\t\x12\x13\n\x0bhouseholdID\x18\t \x01(\t\"!\n\x0eRegister_Reply\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\x98\x01\n\x0b\x61\x63\x63_Hougang\x12?\n\x05Login\x12\x1a.acc_hougang.Login_Request\x1a\x18.acc_hougang.Login_Reply\"\x00\x12H\n\x08Register\x12\x1d.acc_hougang.Register_Request\x1a\x1b.acc_hougang.Register_Reply\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'acc_hougang_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _LOGIN_REQUEST._serialized_start=34
  _LOGIN_REQUEST._serialized_end=82
  _LOGIN_REPLY._serialized_start=84
  _LOGIN_REPLY._serialized_end=114
  _REGISTER_REQUEST._serialized_start=117
  _REGISTER_REQUEST._serialized_end=291
  _REGISTER_REPLY._serialized_start=293
  _REGISTER_REPLY._serialized_end=326
  _ACC_HOUGANG._serialized_start=329
  _ACC_HOUGANG._serialized_end=481
# @@protoc_insertion_point(module_scope)
