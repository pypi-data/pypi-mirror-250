import time
from copy import deepcopy
from collections.abc import Callable, Mapping
from typing import Optional
from .util.general_consts import EMPTY_DICT

MONA_ARGS_PREFIX = "MONA_"
ADDITIONAL_DATA_ARG_NAME = MONA_ARGS_PREFIX + "additional_data"

def get_logging_message(
    api_name: str,
    request_input: Mapping,
    start_time: float,
    is_exception: bool,
    is_async: bool,
    stream_start_time: Optional[float],
    response: Optional[Mapping],
    analysis_getter: Callable[[Mapping, Mapping], dict],
    message_cleaner: Callable[[Mapping], dict],
    additional_data: Mapping,
) -> dict:
    """
    Returns a dict object containing all the monitoring analysis to be used
    for data logging.
    """

    message = {
        "input": request_input,
        "latency": time.time() - start_time,
        "stream_start_latency": stream_start_time - start_time
        if stream_start_time is not None
        else None,
        "is_exception": is_exception,
        "api_name": api_name,
        "is_async": is_async,
    }

    if additional_data:
        message["additional_data"] = additional_data

    if response:
        message["response"] = response
        message["analysis"] = analysis_getter(request_input, response)

    return message_cleaner(message)


def get_logging_message_for_create(
    api_name,
    analysis_getter,
    message_cleaner,
    kwargs_param: Mapping,
    start_time: float,
    is_exception: bool,
    is_async: bool,
    stream_start_time: float,
    response: Mapping,
) -> dict:
    """
    Returns a dict to be used for data logging.
    """
    # Recreate the input dict to avoid manipulating the caller's data,
    # and remove Mona-related data.
    request_input = deepcopy(
        {
            x: kwargs_param[x]
            for x in kwargs_param
            if not x.startswith(MONA_ARGS_PREFIX)
        }
    )

    additional_data: Mapping = kwargs_param.get(
        ADDITIONAL_DATA_ARG_NAME, EMPTY_DICT
    )

    return get_logging_message(
        api_name=api_name,
        request_input=request_input,
        start_time=start_time,
        is_exception=is_exception,
        is_async=is_async,
        stream_start_time=stream_start_time,
        response=response,
        analysis_getter=analysis_getter,
        message_cleaner=message_cleaner,
        additional_data=additional_data,
    )