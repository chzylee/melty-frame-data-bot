import constants

# Returns the message pointing users to the issue report form. The form's
# linked Google Sheet acts as the queue Noah reviews to triage data fixes.
def get_report_message() -> str:
    message = "**Report a frame data issue**"
    message += "\nFound missing or incorrect data? Report it here:"
    message += f"\n{constants.REPORT_FORM_URL}"
    message += ("\nPlease include the character, moon (Crescent/Half/Full), move"
                " input, and what's wrong or missing so it can be fixed reliably.")
    return message
