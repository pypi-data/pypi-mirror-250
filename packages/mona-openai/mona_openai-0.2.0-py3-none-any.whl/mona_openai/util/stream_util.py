"""
A util module for everything related to supporting streams.
"""
import inspect
import time
from collections.abc import Callable, Iterator
from typing import Optional

from .async_util import run_in_an_event_loop
from .object_util import get_subscriptable_obj


class ResponseGatheringIterator:
    """
    A generator class that takes an original OpenAI stream response generator
    and wraps it with functionality to gather all the stream of responses as
    they come, and create from them a singular reponse object as would have
    been received in non-stream OpenAI usage.

    Once the original generator is done it creates the full response and calls
    a callback with it.

    It acts both as sync and async generator to ease the use of sync/async
    joint code.
    """

    def __init__(
        self,
        delta_choice_text_getter: Callable,
        final_choice_getter: Callable,
        original_iterator: Iterator,
        callback: Callable,
    ) -> None:
        self._original_iterator = original_iterator
        self._delta_choice_text_getter = delta_choice_text_getter
        self._final_choice_getter = final_choice_getter
        self._callback = callback
        self._initial_event_recieved_time: Optional[float] = None
        self._common_response_information: dict = {}
        self._choices: dict = {}

    def __iter__(self):
        return self

    def __aiter__(self):
        return self

    def __next__(self):
        try:
            return self._add_response(self._original_iterator.__next__())
        except StopIteration:
            self._call_callback()
            raise

    async def __anext__(self):
        try:
            return self._add_response(
                await self._original_iterator.__anext__()
            )
        except StopAsyncIteration:
            await self._a_call_callback()
            raise

    def _add_response(self, event: dict) -> dict:
        """
        The main and only exposed function of the ResponseGatherer class. Use
        this function to collect stream events.
        """
        subscriptable_event = get_subscriptable_obj(event)
        if self._initial_event_recieved_time is None:
            self._initial_event_recieved_time = time.time()
            self._common_response_information = {
                x: subscriptable_event[x] for x in subscriptable_event if x != "choices"
            }

        # Gather response events by choice index.
        self._handle_choice(self._get_only_choice(subscriptable_event))

        return event

    def _call_callback(self):
        # We allow an async function as the callback event if this class is
        # used as a sync generator. This code handles this scenario.
        callback_args = (
            self._create_singular_response(),
            self._initial_event_recieved_time,
        )
        if inspect.iscoroutinefunction(self._callback):
            run_in_an_event_loop(self._callback(*callback_args))
            return

        self._callback(*callback_args)

    async def _a_call_callback(self):
        await self._callback(
            self._create_singular_response(),
            self._initial_event_recieved_time,
        )

    def _handle_choice(self, choice: dict) -> None:
        index = choice["index"]
        self._choices[index] = self._choices.get(index, []) + [choice]

    def _get_only_choice(self, event: dict) -> dict:
        # Stream response events have only a single choice that specifies
        # its own index.
        return event["choices"][0]

    def _create_singular_response(self) -> dict:
        choices = [
            self._get_full_choice(choice) for choice in self._choices.values()
        ]
        return {**self._common_response_information, "choices": choices}

    def _get_full_choice(self, choice: dict) -> dict:
        all_tokens = list(self._delta_choice_text_getter(choice_event)
            for choice_event in choice)
        
        full_text = "".join(token for token in all_tokens if token is not None)

        return {
            **self._final_choice_getter(full_text),
            "index": choice[0]["index"],
            "finish_reason": choice[-1]["finish_reason"],
        }
