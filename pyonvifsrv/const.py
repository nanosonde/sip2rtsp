from enum import Enum

class ERROR_TYPE(str, Enum):
    WELLFORMED = "WellFormed"
    TAG_MISMATCH = "TagMismatch"
    TAG = "Tag"
    NAMESPACE = "Namespace"
    MISSING_ATTR = "MissingAttr"
    PROHIB_ATTR = "ProhibAttr"
    INVALID_ARGS = "InvalidArgs"
    INVALID_ARGS_VAL  = "InvalidArgVal"
    UNKNOWN_ACTION = "UnknownAction"
    OPERATION_PROHIBITED = "OperationProhibited"
    NOT_AUTHORIZED = "NotAuthorized"
    ACTION_NOT_SUPPORTED = "ActionNotSupported"
    ACTION = "Action"
    OUT_OF_MEMORY = "OutofMemory"
    CRITICAL_ERROR = "CriticalError"
