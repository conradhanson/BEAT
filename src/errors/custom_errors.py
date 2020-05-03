class Error(Exception):
    """Base class for exceptions in the LeadGenerator_0 project"""
    pass


class StateCodeFormattingError(Error):
    def __init__(self, state_code, message):
        """
        Exception raised for incorrect state code format

        Args:
            state_code: str
                that was incorrect
            message: str
                explanation of the error
        """
        self.state_code = state_code
        self.message = message
