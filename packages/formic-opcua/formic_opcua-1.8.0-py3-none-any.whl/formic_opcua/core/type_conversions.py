# Copyright Formic Technologies 2023
import hashlib
import logging
import uuid
from datetime import datetime

from asyncua.ua.uatypes import VariantType

logger = logging.getLogger(__name__)


def positive_sha256_hash(obj):
    try:
        logger.debug(f'Trying to cast {obj} to int')
        return int(str(obj))
    except ValueError:
        logger.debug(f'Hashing {obj}')
        sha256_hash = hashlib.sha256()
        sha256_hash.update(str(obj).encode('utf-8'))
        hashed_value = int(
            str(int(sha256_hash.hexdigest(), 16))[:6]
        )  # Make sure there are not too many bytes for UInt32
        logger.debug(f'{obj} was hashed to {hashed_value}')
        return hashed_value


type_map = {
    VariantType.SByte: int,
    VariantType.Byte: int,
    VariantType.ByteString: bytes,
    VariantType.Int32: int,
    VariantType.Int64: int,
    VariantType.UInt16: int,
    VariantType.UInt32: int,
    VariantType.UInt64: int,
    VariantType.Boolean: bool,
    VariantType.Double: float,
    VariantType.Float: float,
    VariantType.String: str,
    VariantType.DateTime: datetime,
    VariantType.Guid: uuid.UUID,
}


def convert_type(value, var_type):
    if isinstance(value, list):
        mapped_value = [type_map[var_type](element) for element in value]
    elif (type_map[var_type] == int or type_map[var_type] == float) and isinstance(value, str):
        mapped_value = type_map[var_type](positive_sha256_hash(value))
    elif (type_map[var_type] == bool) and isinstance(value, str):
        if value.lower() == 'true':
            mapped_value = True
        elif value.lower() == 'false':
            mapped_value = False
        else:
            logger.error('Invalid string for bool type')
            mapped_value = 'ERROR'
    else:
        mapped_value = type_map[var_type](value)

    return mapped_value
