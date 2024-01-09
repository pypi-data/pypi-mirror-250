# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: traffic_api.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import common_pb2 as common__pb2
from . import system_api_pb2 as system__api__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11traffic_api.proto\x12\x04\x62\x61se\x1a\x0c\x63ommon.proto\x1a\x10system_api.proto\"\xaa\x01\n\x0cPlaybackMode\x12\x16\n\x0c\x65rrorMessage\x18\x02 \x01(\tH\x00\x12\r\n\x03\x45OF\x18\x03 \x01(\tH\x00\x12\x1a\n\x04mode\x18\x04 \x01(\x0e\x32\n.base.ModeH\x00\x12\x12\n\noffsetTime\x18\x05 \x01(\x04\x12\x11\n\tstartTime\x18\x06 \x01(\x04\x12\x0f\n\x07\x65ndTime\x18\x07 \x01(\x04\x12\x15\n\rtimeDeviation\x18\x08 \x01(\x03\x42\x08\n\x06status\"9\n\rPlaybackInfos\x12(\n\x0cplaybackInfo\x18\x01 \x03(\x0b\x32\x12.base.PlaybackInfo\"d\n\x0ePlaybackConfig\x12.\n\x0f\x66ileDescription\x18\x01 \x01(\x0b\x32\x15.base.FileDescription\x12\"\n\tnamespace\x18\x02 \x01(\x0b\x32\x0f.base.NameSpace\"f\n\x0cPlaybackInfo\x12,\n\x0eplaybackConfig\x18\x01 \x01(\x0b\x32\x14.base.PlaybackConfig\x12(\n\x0cplaybackMode\x18\x02 \x01(\x0b\x32\x12.base.PlaybackMode*;\n\x04Mode\x12\x08\n\x04PLAY\x10\x00\x12\t\n\x05PAUSE\x10\x01\x12\x08\n\x04STOP\x10\x02\x12\n\n\x06RECORD\x10\x03\x12\x08\n\x04SEEK\x10\x04\x32\x86\x01\n\x0eTrafficService\x12\x39\n\x0bPlayTraffic\x12\x13.base.PlaybackInfos\x1a\x13.base.PlaybackInfos\"\x00\x12\x39\n\x11PlayTrafficStatus\x12\x0b.base.Empty\x1a\x13.base.PlaybackInfos\"\x00\x30\x01\x62\x06proto3')

_MODE = DESCRIPTOR.enum_types_by_name['Mode']
Mode = enum_type_wrapper.EnumTypeWrapper(_MODE)
PLAY = 0
PAUSE = 1
STOP = 2
RECORD = 3
SEEK = 4


_PLAYBACKMODE = DESCRIPTOR.message_types_by_name['PlaybackMode']
_PLAYBACKINFOS = DESCRIPTOR.message_types_by_name['PlaybackInfos']
_PLAYBACKCONFIG = DESCRIPTOR.message_types_by_name['PlaybackConfig']
_PLAYBACKINFO = DESCRIPTOR.message_types_by_name['PlaybackInfo']
PlaybackMode = _reflection.GeneratedProtocolMessageType('PlaybackMode', (_message.Message,), {
  'DESCRIPTOR' : _PLAYBACKMODE,
  '__module__' : 'traffic_api_pb2'
  # @@protoc_insertion_point(class_scope:base.PlaybackMode)
  })
_sym_db.RegisterMessage(PlaybackMode)

PlaybackInfos = _reflection.GeneratedProtocolMessageType('PlaybackInfos', (_message.Message,), {
  'DESCRIPTOR' : _PLAYBACKINFOS,
  '__module__' : 'traffic_api_pb2'
  # @@protoc_insertion_point(class_scope:base.PlaybackInfos)
  })
_sym_db.RegisterMessage(PlaybackInfos)

PlaybackConfig = _reflection.GeneratedProtocolMessageType('PlaybackConfig', (_message.Message,), {
  'DESCRIPTOR' : _PLAYBACKCONFIG,
  '__module__' : 'traffic_api_pb2'
  # @@protoc_insertion_point(class_scope:base.PlaybackConfig)
  })
_sym_db.RegisterMessage(PlaybackConfig)

PlaybackInfo = _reflection.GeneratedProtocolMessageType('PlaybackInfo', (_message.Message,), {
  'DESCRIPTOR' : _PLAYBACKINFO,
  '__module__' : 'traffic_api_pb2'
  # @@protoc_insertion_point(class_scope:base.PlaybackInfo)
  })
_sym_db.RegisterMessage(PlaybackInfo)

_TRAFFICSERVICE = DESCRIPTOR.services_by_name['TrafficService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MODE._serialized_start=497
  _MODE._serialized_end=556
  _PLAYBACKMODE._serialized_start=60
  _PLAYBACKMODE._serialized_end=230
  _PLAYBACKINFOS._serialized_start=232
  _PLAYBACKINFOS._serialized_end=289
  _PLAYBACKCONFIG._serialized_start=291
  _PLAYBACKCONFIG._serialized_end=391
  _PLAYBACKINFO._serialized_start=393
  _PLAYBACKINFO._serialized_end=495
  _TRAFFICSERVICE._serialized_start=559
  _TRAFFICSERVICE._serialized_end=693
# @@protoc_insertion_point(module_scope)
