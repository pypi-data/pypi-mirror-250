from typing import Literal, Optional, Sequence

import pydantic
from typing_extensions import Annotated

from ..types.completion_usage import CompletionUsage
from ..types.finish_reason import FinishReason
from ..types.model import Model


class CommonCreateCompletion(pydantic.BaseModel):
    model: Model
    stream: bool = False
    max_tokens: Optional[int] = None
    stop: Annotated[Sequence[str], pydantic.Field(str, max_length=8)] = []
    temperature: pydantic.NonNegativeFloat = 0.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    top_p: Annotated[float, pydantic.Field(float, gt=0.0, le=1.0)] = 1.0
    top_k: Optional[int] = None


class _CreateCompletion(pydantic.BaseModel):
    prompt: str = pydantic.Field(
        description="Defines the initial context for auto regressive text generation.",
    )


class CreateCompletion(CommonCreateCompletion, _CreateCompletion):
    pass


class CommonChoice(pydantic.BaseModel):
    finish_reason: FinishReason = pydantic.Field(
        description="Specifies the reason for the token generation termination, indicating either a natural stopping point `stop` or a reach of a maximum token count constraint.",
    )
    index: int = pydantic.Field(
        description="The position of the choice in the choices array.",
    )


class Choice(CommonChoice):
    text: str = pydantic.Field(
        description="Generated text response.",
    )


class CommonCompletion(pydantic.BaseModel):
    id: str = pydantic.Field(
        description="A unique identifier that serves as a reference for the generated completion."
    )
    created: int = pydantic.Field(
        description="A Unix timestamp, indicating the time of completion creation."
    )
    model: str = pydantic.Field(
        description="Identifier of the model used to create the completion."
    )
    usage: Optional[CompletionUsage] = pydantic.Field(
        description="Identifier of the model used to create the completion."
    )


class Completion(CommonCompletion):
    choices: Sequence[Choice] = pydantic.Field(
        default="A list of generated text responses."
    )
    object: Literal["completion"] = pydantic.Field(description="Constant `completion`")
