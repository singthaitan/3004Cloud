# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto_files/ml_hougang.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cproto_files/ml_hougang.proto\x12\nml_hougang\"6\n\x11UsageData_Request\x12\x13\n\x0bhouseholdid\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ys\x18\x02 \x01(\x05\"5\n\tUsageData\x12\x11\n\ttimestamp\x18\x01 \x01(\t\x12\x15\n\relectricusage\x18\x02 \x01(\x02\"7\n\x0fUsageData_Reply\x12$\n\x05items\x18\x01 \x03(\x0b\x32\x15.ml_hougang.UsageData\"-\n\x16PredictionData_Request\x12\x13\n\x0bhouseholdid\x18\x01 \x01(\t\"D\n\x18PredictionDataIndividual\x12\x11\n\ttimestamp\x18\x01 \x01(\t\x12\x15\n\relectricusage\x18\x02 \x01(\x02\"G\n\x1bPredictionDataHouseholdType\x12\x11\n\ttimestamp\x18\x01 \x01(\t\x12\x15\n\relectricusage\x18\x02 \x01(\x02\"\x82\x01\n\x14PredictionData_Reply\x12\x32\n\x04item\x18\x01 \x03(\x0b\x32$.ml_hougang.PredictionDataIndividual\x12\x36\n\x05item2\x18\x02 \x03(\x0b\x32\'.ml_hougang.PredictionDataHouseholdType2\xb7\x01\n\nml_Hougang\x12L\n\x0cGetUsageData\x12\x1d.ml_hougang.UsageData_Request\x1a\x1b.ml_hougang.UsageData_Reply\"\x00\x12[\n\x11GetPredictionData\x12\".ml_hougang.PredictionData_Request\x1a .ml_hougang.PredictionData_Reply\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto_files.ml_hougang_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _USAGEDATA_REQUEST._serialized_start=44
  _USAGEDATA_REQUEST._serialized_end=98
  _USAGEDATA._serialized_start=100
  _USAGEDATA._serialized_end=153
  _USAGEDATA_REPLY._serialized_start=155
  _USAGEDATA_REPLY._serialized_end=210
  _PREDICTIONDATA_REQUEST._serialized_start=212
  _PREDICTIONDATA_REQUEST._serialized_end=257
  _PREDICTIONDATAINDIVIDUAL._serialized_start=259
  _PREDICTIONDATAINDIVIDUAL._serialized_end=327
  _PREDICTIONDATAHOUSEHOLDTYPE._serialized_start=329
  _PREDICTIONDATAHOUSEHOLDTYPE._serialized_end=400
  _PREDICTIONDATA_REPLY._serialized_start=403
  _PREDICTIONDATA_REPLY._serialized_end=533
  _ML_HOUGANG._serialized_start=536
  _ML_HOUGANG._serialized_end=719
# @@protoc_insertion_point(module_scope)