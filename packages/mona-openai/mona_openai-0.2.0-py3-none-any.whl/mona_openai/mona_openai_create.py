import time
from collections.abc import Callable
from .util.async_util import (
    call_non_blocking_sync_or_async
)
from .util.func_util import add_conditional_sampling
from .util.openai_util import get_model_param
from .util.stream_util import ResponseGatheringIterator
from .util.tokens_util import get_usage
from .util.object_util import get_subscriptable_obj

MONA_ARGS_PREFIX = "MONA_"
CONTEXT_ID_ARG_NAME = MONA_ARGS_PREFIX + "context_id"
EXPORT_TIMESTAMP_ARG_NAME = MONA_ARGS_PREFIX + "export_timestamp"
ADDITIONAL_DATA_ARG_NAME = MONA_ARGS_PREFIX + "additional_data"




async def create_logic(
        is_async,
        export_function: Callable,
        super_function: Callable,
        logging_message_getter,
        sampling_ratio,
        all_prompt_texts_getter,
        all_response_texts_getter,
        stream_delta_text_from_choice_getter,
        final_choice_getter,
        specs,
        args,
        kwargs):
    is_stream = kwargs.get("stream", False)

    response = None

    # will be used only when stream is enabled
    stream_start_time = None

    async def _inner_log_message(is_exception):
        subscriptable_response = get_subscriptable_obj(response)
        
        return await call_non_blocking_sync_or_async(
            export_function,
            (
                logging_message_getter(
                    kwargs,
                    start_time,
                    is_exception,
                    is_async,
                    stream_start_time,
                    subscriptable_response,
                ),
                kwargs.get(
                    CONTEXT_ID_ARG_NAME,
                    subscriptable_response["id"] if subscriptable_response else None,
                ),
                kwargs.get(EXPORT_TIMESTAMP_ARG_NAME, start_time),
            ),
        )

    log_message = add_conditional_sampling(
        _inner_log_message, sampling_ratio
    )

    start_time = time.time()

    async def inner_super_function():
        # Call the actual openai create function without the Mona
        # specific arguments.
        return await call_non_blocking_sync_or_async(
            super_function,
            args,
            {
                x: kwargs[x]
                for x in kwargs
                if not x.startswith(MONA_ARGS_PREFIX)
            },
        )

    async def inner_handle_exception():
        if not specs.get("avoid_monitoring_exceptions", False):
            await log_message(True)

    if not is_stream:
        try:
            response = await inner_super_function()
        except Exception:
            await inner_handle_exception()
            raise

        await log_message(False)

        return response

    # From here it's stream handling.

    async def _stream_done_callback(
        final_response, actual_stream_start_time
    ):
        nonlocal response
        nonlocal stream_start_time
        # There is no usage data in returned stream responses, so
        # we add it here.
        response = final_response | {
            "usage": get_usage(
                model=get_model_param(kwargs),
                prompt_texts=all_prompt_texts_getter(kwargs),
                response_texts=all_response_texts_getter(
                    final_response
                ),
            )
        }
        stream_start_time = actual_stream_start_time
        await log_message(False)

    try:
        # Call the actual openai create function without the Mona
        # specific arguments.
        return ResponseGatheringIterator(
            original_iterator=await inner_super_function(),
            delta_choice_text_getter=(
                stream_delta_text_from_choice_getter
            ),
            final_choice_getter=final_choice_getter,
            callback=_stream_done_callback,
        )

    except Exception:
        await inner_handle_exception()
        raise

