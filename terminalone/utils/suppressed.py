# -*- coding: utf-8 -*-
"""Context manager to suppress specified exceptions.

After the exception is suppressed, execution proceeds with the next
statement following the with statement.

    with suppress(FileNotFoundError):
        os.remove(somefile)
    # Execution still resumes here if the file was already removed
"""

try:
    from contextlib import suppress
except ImportError:
    from contextlib import contextmanager

    @contextmanager
    def suppress(*exceptions):
        """Context manager to suppress specified exceptions.

        After the exception is suppressed, execution proceeds with the next
        statement following the with statement.

            with suppress(FileNotFoundError):
                os.remove(somefile)
            # Execution still resumes here if the file was already removed
        """
        try:
            yield
        except exceptions:
            pass
