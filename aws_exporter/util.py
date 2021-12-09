# -*- coding: utf-8 -*-
# ISC License
#
# Copyright 2019 FL Fintech E GmbH
#
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import logging
import sys
from functools import wraps

from aws_exporter.aws.sts import get_account_id

LOGGER = logging.getLogger(__name__)


def paginate(data_function, process_function, data_function_kwargs=None, process_function_kwargs=None):
    """
    paginate a data function and execute a process function on results
    """
    data_function_kwargs = data_function_kwargs if data_function_kwargs is not None else dict()

    response = data_function(**data_function_kwargs)

    process_function_kwargs = process_function_kwargs if process_function_kwargs is not None else dict()

    while True:
        process_function(response, **process_function_kwargs)

        if "NextToken" not in response:
            break

        response = data_function(NextToken=response["NextToken"])


def success_metric(metric):
    def decorator(collector_function):
        @wraps(collector_function)
        def function_wrapper(*args, **kwargs):
            try:
                return collector_function(*args, **kwargs)
            except Exception:
                LOGGER.exception("caught exception in collector function")
            finally:
                metric.labels(get_account_id()).set(0 if sys.exc_info()[0] is not None else 1)

        return function_wrapper

    return decorator


def strget(dict_obj, value, default=None):
    return str(dict_obj.get(value, default))
