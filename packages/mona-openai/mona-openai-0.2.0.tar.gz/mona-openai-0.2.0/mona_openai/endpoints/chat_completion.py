"""
The Mona wrapping code for OpenAI's ChatCompletion API.
"""
from collections.abc import Callable, Iterable, Mapping
from copy import deepcopy
from functools import wraps

from ..analysis.privacy import PrivacyAnalyzer, get_privacy_analyzers
from ..analysis.profanity import get_has_profanity, get_profanity_prob
from ..analysis.textual import TextualAnalyzer, get_textual_analyzers
from ..analysis.util import create_combined_analyzer
from .endpoint_wrapping import OpenAIEndpointWrappingLogic

CHAT_COMPLETION_CLASS_NAME = "ChatCompletion"


def _get_choices_texts(response: Mapping) -> tuple:
    return tuple(
        choice["message"].get("content") for choice in response["choices"]
    )


def _get_prompt_texts(request: Mapping) -> tuple:
    return tuple(message["content"] for message in request["messages"])


def _get_texts(func: Callable) -> Callable:
    def wrapper(self, input: Mapping, response: Mapping):
        return func(
            self,
            input["messages"][-1]["content"]
            if input["messages"][-1]["role"] == "user"
            else None,
            _get_prompt_texts(input),
            _get_choices_texts(response),
        )

    return wrapper


def _get_analyzers(analyzers_getter: Callable) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(
            self,
            last_user_message: str,
            messages: Iterable[str],
            answers: Iterable[str],
        ):
            return func(
                self,
                analyzers_getter((last_user_message,))[0]
                if last_user_message is not None
                else None,
                analyzers_getter(messages),
                analyzers_getter(answers),
            )

        return wrapper

    return decorator


class ChatCompletionWrapping(OpenAIEndpointWrappingLogic):
    def _get_endpoint_name(self):
        return CHAT_COMPLETION_CLASS_NAME

    def _internal_get_clean_message(self, message: Mapping) -> Mapping:
        """
        Returns a copy of the given message with relevant data removed, for
        example the actual texts, to avoid sending such information, that
        is sometimes sensitive, to Mona.
        """
        new_message = deepcopy(message)
        if not self._specs.get("export_prompt", False):
            for input_message in new_message["input"]["messages"]:
                input_message.pop("content", None)

        if "response" in message and not self._specs.get(
            "export_response_texts", False
        ):
            for choice in new_message["response"]["choices"]:
                choice["message"].pop("content", None)

        return new_message

    @_get_texts
    @_get_analyzers(get_privacy_analyzers)
    def _get_full_privacy_analysis(
        self,
        last_user_message_analyzer: PrivacyAnalyzer,
        messages_privacy_analyzers: Iterable[PrivacyAnalyzer],
        answers_privacy_analyzers: Iterable[PrivacyAnalyzer],
    ) -> dict:
        combined_messages = create_combined_analyzer(
            messages_privacy_analyzers
        )
        combined_answers = create_combined_analyzer(answers_privacy_analyzers)
        ret = {
            "total_prompt_phone_number_count": sum(
                combined_messages.get_phone_numbers_count()
            ),
            "answer_unknown_phone_number_count": (
                combined_answers.get_previously_unseen_phone_numbers_count(
                    messages_privacy_analyzers
                )
            ),
            "total_prompt_email_count": sum(
                combined_messages.get_emails_count()
            ),
            "answer_unknown_email_count": (
                combined_answers.get_previously_unseen_emails_count(
                    messages_privacy_analyzers
                )
            ),
        }
        if last_user_message_analyzer is not None:
            ret.update(
                {
                    "last_user_message_phone_number_count": (
                        last_user_message_analyzer.get_phone_numbers_count()
                    ),
                    "last_user_message_emails_count": (
                        last_user_message_analyzer.get_emails_count()
                    ),
                }
            )
        return ret

    @_get_texts
    @_get_analyzers(get_textual_analyzers)
    def _get_full_textual_analysis(
        self,
        last_user_message_analyzer: TextualAnalyzer,
        messages_textual_analyzers: Iterable[TextualAnalyzer],
        answers_textual_analyzers: Iterable[TextualAnalyzer],
    ) -> dict:
        combined_messages = create_combined_analyzer(
            messages_textual_analyzers
        )
        combined_answers = create_combined_analyzer(answers_textual_analyzers)
        total_prompt_word_count = sum(combined_messages.get_word_count())
        total_prompt_preposition_count = sum(
            combined_messages.get_preposition_count()
        )

        ret = {
            "total_prompt_length": sum(combined_messages.get_length()),
            "answer_length": combined_answers.get_length(),
            "total_prompt_word_count": total_prompt_word_count,
            "answer_word_count": combined_answers.get_word_count(),
            "total_prompt_preposition_count": total_prompt_preposition_count,
            "total_prompt_preposition_ratio": total_prompt_preposition_count
            / total_prompt_word_count
            if total_prompt_word_count != 0
            else None,
            "answer_preposition_count": (
                combined_answers.get_preposition_count()
            ),
            "answer_preposition_ratio": (
                combined_answers.get_preposition_ratio()
            ),
            "answer_words_not_in_prompt_count": (
                combined_answers.get_words_not_in_others_count(
                    messages_textual_analyzers
                )
            ),
            "answer_words_not_in_prompt_ratio": tuple(
                analyzer.get_words_not_in_others_count(
                    messages_textual_analyzers
                )
                / analyzer.get_word_count()
                if analyzer.get_word_count() > 0
                else 0.0
                for analyzer in answers_textual_analyzers
                if not analyzer.is_none_analyzer()
            ),
        }

        if last_user_message_analyzer is not None:
            ret.update(
                {
                    "last_user_message_length": (
                        last_user_message_analyzer.get_length()
                    ),
                    "last_user_message_word_count": (
                        last_user_message_analyzer.get_word_count()
                    ),
                    "last_user_message_preposition_count": (
                        last_user_message_analyzer.get_preposition_count()
                    ),
                    "last_user_message_preposition_ratio": (
                        last_user_message_analyzer.get_preposition_ratio()
                    ),
                }
            )

        return ret

    @_get_texts
    def _get_full_profainty_analysis(
        self,
        last_user_message: str,
        messages: Iterable[str],
        answers: Iterable[str],
    ) -> dict:
        ret: dict = {
            "prompt_profanity_prob": get_profanity_prob(messages),
            "prompt_has_profanity": get_has_profanity(messages),
            "answer_profanity_prob": get_profanity_prob(answers),
            "answer_has_profanity": get_has_profanity(answers),
        }

        if last_user_message is not None:
            ret.update(
                {
                    "last_user_message_profanity_prob": get_profanity_prob(
                        (last_user_message,)
                    )[0],
                    "last_user_message_has_profanity": get_has_profanity(
                        (last_user_message,)
                    )[0],
                }
            )

        return ret

    def get_stream_delta_text_from_choice(self, choice: Mapping) -> str:
        return choice["delta"].get("content", "")

    def get_final_choice(self, text: str) -> dict:
        return {"message": {"role": "assistant", "content": text}}

    def get_all_prompt_texts(self, request: Mapping) -> Iterable[str]:
        return _get_prompt_texts(request)

    def get_all_response_texts(self, response: Mapping) -> Iterable[str]:
        return _get_choices_texts(response)
