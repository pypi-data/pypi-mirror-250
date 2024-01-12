import openai
from collections.abc import Mapping, Callable
from .loggers.mona_logger.mona_client import MonaCredsType, get_mona_clients
from .loggers.mona_logger.mona_logger import MonaLogger
from .util.general_consts import EMPTY_DICT
from .util.validation_util import validate_and_get_sampling_ratio
from .endpoints.chat_completion import CHAT_COMPLETION_CLASS_NAME
from .mona_openai_create import create_logic
from .util.async_util import (
    run_in_an_event_loop,
)
from .mona_openai_logging import get_logging_message_for_create
from .endpoints.wrapping_getter import get_endpoint_wrapping


def monitor_client_with_logger(openai_client, logger, specs=EMPTY_DICT):
    sampling_ratio = validate_and_get_sampling_ratio(specs)

    # TODO(itai): We currently support only chat completion and use the legacy
    #   class name. This should be changed and the library refactored to
    #   support the different opneAI endpoints.
    logger.start_monitoring(CHAT_COMPLETION_CLASS_NAME)

    original_create = openai_client.chat.completions.create

    wrapping_logic = get_endpoint_wrapping(CHAT_COMPLETION_CLASS_NAME, specs)

    def _get_logging_message(
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
        return get_logging_message_for_create(
            CHAT_COMPLETION_CLASS_NAME,
            wrapping_logic.get_full_analysis,
            wrapping_logic.get_clean_message,
            kwargs_param,
            start_time,
            is_exception,
            is_async,
            stream_start_time,
            response
        )

    def wrapped_create(*args, **kwargs):
        return run_in_an_event_loop(
            create_logic(False, logger.log, original_create, _get_logging_message,sampling_ratio,wrapping_logic.get_all_prompt_texts, wrapping_logic.get_all_response_texts,wrapping_logic.get_stream_delta_text_from_choice, wrapping_logic.get_final_choice, specs,args,kwargs)
        )
    
    async def async_wrapped_create(*args, **kwargs):
        return await create_logic(True, logger.alog, original_create, _get_logging_message,sampling_ratio,wrapping_logic.get_all_prompt_texts, wrapping_logic.get_all_response_texts,wrapping_logic.get_stream_delta_text_from_choice, wrapping_logic.get_final_choice, specs,args,kwargs)
    
    
    openai_client.chat.completions.create = async_wrapped_create if isinstance(openai_client, openai.AsyncOpenAI) else wrapped_create
    return openai_client



def monitor_client(
    openai_client,
    mona_creds: MonaCredsType,
    context_class: str,
    specs: Mapping = EMPTY_DICT,
    mona_clients_getter: Callable = get_mona_clients,
):
    """
    A simple wrapper around "monitor_with_logger" to use with a Mona logger.
    See "monitor_with_logger" for full documentation.

    Args:
        openai_class: An OpenAI API class to wrap with monitoring
            capabilties.
        mona_creds: Either a dict or pair of Mona API key and secret to
            set up Mona's clients from its SDK
        context_class: The Mona context class name to use for
            monitoring. Use a name of your choice.
        specs: A dictionary of specifications such as monitoring
            sampling ratio.
        mona_clients_getter: Used only for testing purposes.
    """
    return monitor_client_with_logger(
        openai_client,
        MonaLogger(mona_creds, context_class, mona_clients_getter),
        specs,
    )