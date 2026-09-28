import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors
from pydantic import BaseModel, ValidationError

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
FALLBACK_MODEL = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-3.8-flash")

client = genai.Client(api_key=API_KEY)


class GeminiGenerationError(Exception):
    pass


def generate_text(prompt: str) -> str:
    last_error = None
    model_errors = []
    for model in dict.fromkeys((MODEL, FALLBACK_MODEL)):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )
            if response.text:
                return response.text
            raise GeminiGenerationError("Gemini returned an empty response.")
        except errors.APIError as error:
            last_error = error
            model_errors.append((model, error))

    if last_error is not None:
        if all(getattr(error, "code", None) == 429 for _, error in model_errors):
            message = (
                "Gemini quota or rate limit is exhausted for the configured models. "
                "Check Google AI Studio quota and billing, then retry."
            )
        else:
            failed_models = ", ".join(
                f"{model} (HTTP {getattr(error, 'code', 'unknown')})"
                for model, error in model_errors
            )
            message = (
                f"Gemini requests failed for all configured models: {failed_models}. "
                "Check API key, model access, and quota."
            )
        raise GeminiGenerationError(message) from last_error

    raise GeminiGenerationError("No Gemini models are configured.")


def generate_structured(prompt: str, response_schema: type[BaseModel]) -> BaseModel:
    model_errors = []
    for model in dict.fromkeys((MODEL, FALLBACK_MODEL)):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": response_schema,
                },
            )
            parsed = response.parsed or response.text
            if not parsed:
                raise GeminiGenerationError("Gemini returned an empty response.")
            return response_schema.model_validate(parsed)
        except errors.APIError as error:
            model_errors.append((model, error))
        except (TypeError, ValidationError) as error:
            raise GeminiGenerationError(
                "Gemini returned quiz data in an invalid format. Please try again."
            ) from error

    if model_errors:
        if all(getattr(error, "code", None) == 429 for _, error in model_errors):
            message = (
                "Gemini quota or rate limit is exhausted for the configured models. "
                "Check Google AI Studio quota and billing, then retry."
            )
        else:
            failed_models = ", ".join(
                f"{model} (HTTP {getattr(error, 'code', 'unknown')})"
                for model, error in model_errors
            )
            message = (
                f"Gemini requests failed for all configured models: {failed_models}. "
                "Check API key, model access, and quota."
            )
        raise GeminiGenerationError(message) from model_errors[-1][1]

    raise GeminiGenerationError("No Gemini models are configured.")