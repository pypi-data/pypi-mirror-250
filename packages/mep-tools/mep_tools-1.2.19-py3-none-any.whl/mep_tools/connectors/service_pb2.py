# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rservice.proto\x12\x11\x63onnector.service\x1a\x19google/protobuf/any.proto\"\xcc\x02\n\x07Service\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x12\n\ncreated_at\x18\x03 \x01(\t\x12\x12\n\nupdated_at\x18\x04 \x01(\t\x12\x34\n\x04type\x18\x05 \x01(\x0e\x32&.connector.service.Service.ServiceType\x12\x0c\n\x04icon\x18\x06 \x01(\t\x12\x30\n\reditor_config\x18\x07 \x01(\x0b\x32\x14.google.protobuf.AnyH\x00\x88\x01\x01\"v\n\x0bServiceType\x12\x1c\n\x18SERVICE_TYPE_UNSPECIFIED\x10\x00\x12\x14\n\x10SERVICE_TYPE_ATS\x10\x01\x12\x18\n\x14SERVICE_TYPE_CHANNEL\x10\x02\x12\x19\n\x15SERVICE_TYPE_PLATFORM\x10\x03\x42\x10\n\x0e_editor_config\"%\n\x0fServicesRequest\x12\x12\n\ncompany_id\x18\x01 \x01(\t\"@\n\x10ServicesResponse\x12,\n\x08services\x18\x01 \x03(\x0b\x32\x1a.connector.service.Service\"1\n\x0eServiceRequest\x12\x12\n\ncompany_id\x18\x01 \x01(\t\x12\x0b\n\x03key\x18\x02 \x01(\t\">\n\x0fServiceResponse\x12+\n\x07service\x18\x01 \x01(\x0b\x32\x1a.connector.service.Service2\xb9\x01\n\x10\x43onnectorService\x12S\n\x08Services\x12\".connector.service.ServicesRequest\x1a#.connector.service.ServicesResponse\x12P\n\x07Service\x12!.connector.service.ServiceRequest\x1a\".connector.service.ServiceResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_SERVICE']._serialized_start=64
  _globals['_SERVICE']._serialized_end=396
  _globals['_SERVICE_SERVICETYPE']._serialized_start=260
  _globals['_SERVICE_SERVICETYPE']._serialized_end=378
  _globals['_SERVICESREQUEST']._serialized_start=398
  _globals['_SERVICESREQUEST']._serialized_end=435
  _globals['_SERVICESRESPONSE']._serialized_start=437
  _globals['_SERVICESRESPONSE']._serialized_end=501
  _globals['_SERVICEREQUEST']._serialized_start=503
  _globals['_SERVICEREQUEST']._serialized_end=552
  _globals['_SERVICERESPONSE']._serialized_start=554
  _globals['_SERVICERESPONSE']._serialized_end=616
  _globals['_CONNECTORSERVICE']._serialized_start=619
  _globals['_CONNECTORSERVICE']._serialized_end=804
# @@protoc_insertion_point(module_scope)
