# found on Discord Application -> General Information page
PUBLIC_KEY = "f65af3e8f227b4a24e3abe88ab35835cf20a9523ee3b6b43054c309ffaac588d"
PING_PONG = { "type": 1 }
RESPONSE_TYPES =  {
    "PONG": 1,
    "ACK_NO_SOURCE": 2,
    "MESSAGE_NO_SOURCE": 3,
    "MESSAGE_WITH_SOURCE": 4,
    "ACK_WITH_SOURCE": 5
}

DYNAMODB_TABLE_NAME = "MBAACC-Frame-Data"
DYNAMODB_PARTITION_KEY = "character_name"
DYNAMODB_SORT_KEY = "moon"
