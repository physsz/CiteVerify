"""Evidence-based scholarly reference verification."""

from citeverify.models import (
    FieldComparison,
    IdentifierCandidate,
    JournalLocator,
    ParsedAuthor,
    ParsedReference,
    RegistryRecord,
    VerificationResult,
    VerificationStatus,
)

__all__ = [
    "FieldComparison",
    "IdentifierCandidate",
    "JournalLocator",
    "ParsedAuthor",
    "ParsedReference",
    "RegistryRecord",
    "VerificationResult",
    "VerificationStatus",
]

__version__ = "0.1.0"
