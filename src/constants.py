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

# Google Form used to collect frame data issue reports. Responses land in the
# form's linked Google Sheet, which acts as the review queue.
# Replace the placeholder below with your published form's share link.
REPORT_FORM_URL = "https://forms.gle/tnEANYYhw4jSTHxj9"
