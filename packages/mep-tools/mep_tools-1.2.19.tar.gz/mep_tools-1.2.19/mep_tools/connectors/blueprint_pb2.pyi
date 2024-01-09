from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OperationEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    GET: _ClassVar[OperationEnum]
    CREATE: _ClassVar[OperationEnum]
    READ: _ClassVar[OperationEnum]
    UPDATE: _ClassVar[OperationEnum]
    DELETE: _ClassVar[OperationEnum]
GET: OperationEnum
CREATE: OperationEnum
READ: OperationEnum
UPDATE: OperationEnum
DELETE: OperationEnum

class BlueprintGetRequest(_message.Message):
    __slots__ = ["blueprint_uuid"]
    BLUEPRINT_UUID_FIELD_NUMBER: _ClassVar[int]
    blueprint_uuid: str
    def __init__(self, blueprint_uuid: _Optional[str] = ...) -> None: ...

class BlueprintReadRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class BlueprintResponse(_message.Message):
    __slots__ = ["operation", "success", "uuid", "key", "name", "icon", "configuration", "created_at", "updated_at"]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    operation: OperationEnum
    success: bool
    uuid: str
    key: str
    name: str
    icon: str
    configuration: _any_pb2.Any
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, operation: _Optional[_Union[OperationEnum, str]] = ..., success: bool = ..., uuid: _Optional[str] = ..., key: _Optional[str] = ..., name: _Optional[str] = ..., icon: _Optional[str] = ..., configuration: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class BlueprintsResponse(_message.Message):
    __slots__ = ["operation", "success", "blueprints"]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    BLUEPRINTS_FIELD_NUMBER: _ClassVar[int]
    operation: OperationEnum
    success: bool
    blueprints: _containers.RepeatedCompositeFieldContainer[BlueprintResponse]
    def __init__(self, operation: _Optional[_Union[OperationEnum, str]] = ..., success: bool = ..., blueprints: _Optional[_Iterable[_Union[BlueprintResponse, _Mapping]]] = ...) -> None: ...
