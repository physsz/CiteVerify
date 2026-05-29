class CiteVerifyError(Exception):
    """Base exception for CiteVerify."""


class UnsupportedInputError(CiteVerifyError):
    """Raised when an input format is not implemented."""


class ParseError(CiteVerifyError):
    """Raised when an input file cannot be parsed."""
