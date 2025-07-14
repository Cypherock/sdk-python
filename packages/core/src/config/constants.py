# Device hardware constants
DEVICE_CONSTANTS = {
    'VENDOR_ID': 0x0483,
    'PRODUCT_ID': 0x5741,
    'USAGE_PAGE': 0xFF00,
    'USAGE': 0x0001,
    'INTERFACE_NUMBER': 0,
    'ENDPOINT_IN': 0x81,
    'ENDPOINT_OUT': 0x01,
    'PACKET_SIZE': 64,
    'TIMEOUT': 1000
}

DEVICE_STATES = {
    'BOOTLOADER': 0,
    'FIRMWARE': 1,
    'INITIAL': 2
}

# Version-specific protocol constants
v1 = {
    'START_OF_FRAME': 'AA',
    'STUFFING_BYTE': 0xaa,
    'ACK_BYTE': '06',
    'CHUNK_SIZE': 32 * 2,
    'ACK_TIME': 2000,
    'RECHECK_TIME': 50,
}

v2 = {
    'START_OF_FRAME': '5A5A',
    'STUFFING_BYTE': 0x5a,
    'ACK_BYTE': '06',
    'CHUNK_SIZE': 32 * 2,
    'ACK_TIME': 2000,
    'RECHECK_TIME': 50,
}

v3 = {
    'START_OF_FRAME': '5555',
    'STUFFING_BYTE': 0x5a,
    'ACK_BYTE': '06',
    'CHUNK_SIZE': 48 * 2,
    'ACK_TIME': 2000,
    'IDLE_TIMEOUT': 4000,
    'CMD_RESPONSE_TIME': 2000,
    'RECHECK_TIME': 2,
    'IDLE_RECHECK_TIME': 200,
}


