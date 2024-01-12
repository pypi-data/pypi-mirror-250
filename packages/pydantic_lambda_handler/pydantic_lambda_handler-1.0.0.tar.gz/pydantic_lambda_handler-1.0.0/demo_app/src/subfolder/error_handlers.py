from handler_app import plh


@plh.get("/error", errors=[(418, ValueError)])
def error_skip():
    raise ValueError("nope")


@plh.get("/multiple_errors", errors=[(422, (ValueError, TypeError))])
def error_multiple():
    raise ValueError("nope")
