class QuotaExceededError(Exception):
    """
    Custom exception raised when the quota for a provider has been exceeded.
    """
    description = "Quota Exceeded"


class AppInvokeQuotaExceededError(Exception):
    """
    Custom exception raised when the quota for an app has been exceeded.
    """
    description = "App Invoke Quota Exceeded"
