"""Minimal generated protobuf module for log.proto."""

from google.protobuf import descriptor_pb2, descriptor_pool, symbol_database
from google.protobuf.message_factory import GetMessageClass

_sym_db = symbol_database.Default()

_file_proto = descriptor_pb2.FileDescriptorProto()
_file_proto.name = "proto/log.proto"
_file_proto.package = "log"
_file_proto.syntax = "proto3"

_log_entry = _file_proto.message_type.add()
_log_entry.name = "LogEntry"

_field = _log_entry.field.add()
_field.name = "service_name"
_field.number = 1
_field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
_field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

_field = _log_entry.field.add()
_field.name = "level"
_field.number = 2
_field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
_field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

_field = _log_entry.field.add()
_field.name = "message"
_field.number = 3
_field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
_field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

_field = _log_entry.field.add()
_field.name = "timestamp"
_field.number = 4
_field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
_field.type = descriptor_pb2.FieldDescriptorProto.TYPE_INT64

_ack = _file_proto.message_type.add()
_ack.name = "Ack"

_field = _ack.field.add()
_field.name = "status"
_field.number = 1
_field.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
_field.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

_service = _file_proto.service.add()
_service.name = "LogService"
_method = _service.method.add()
_method.name = "StreamLogs"
_method.client_streaming = True
_method.input_type = ".log.LogEntry"
_method.output_type = ".log.Ack"

DESCRIPTOR = descriptor_pool.Default().AddSerializedFile(_file_proto.SerializeToString())

LogEntry = GetMessageClass(DESCRIPTOR.message_types_by_name["LogEntry"])
Ack = GetMessageClass(DESCRIPTOR.message_types_by_name["Ack"])

_sym_db.RegisterMessage(LogEntry)
_sym_db.RegisterMessage(Ack)

__all__ = ["Ack", "DESCRIPTOR", "LogEntry"]
