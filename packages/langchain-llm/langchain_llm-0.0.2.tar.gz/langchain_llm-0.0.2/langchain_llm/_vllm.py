from __future__ import annotations

import time
import uuid
from typing import (
    Any,
    List,
    Optional,
)

from langchain_community.llms.vllm import VLLM
from openai.types.completion import Completion
from openai.types.completion_choice import (
    CompletionChoice,
)
from openai.types.completion_usage import CompletionUsage


class XVLLM(VLLM):
    """vllm model."""

    model_name: str
    """The name of a HuggingFace Transformers model."""

    def call_as_openai(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Completion:
        """Run the LLM on the given prompt and input."""

        from vllm import SamplingParams

        # build sampling parameters
        params = {**self._default_params, **kwargs, "stop": stop}
        sampling_params = SamplingParams(**params)
        # call the model
        outputs = self.client.generate([prompt], sampling_params)[0]

        choices = []
        for output in outputs.outputs:
            text = output.text
            choices.append(
                CompletionChoice(
                    index=0,
                    text=text,
                    finish_reason="stop",
                    logprobs=None,
                )
            )

        num_prompt_tokens = len(outputs.prompt_token_ids)
        num_generated_tokens = sum(len(output.token_ids) for output in outputs.outputs)
        usage = CompletionUsage(
            prompt_tokens=num_prompt_tokens,
            completion_tokens=num_generated_tokens,
            total_tokens=num_prompt_tokens + num_generated_tokens,
        )

        return Completion(
            id=f"cmpl-{str(uuid.uuid4())}",
            choices=choices,
            created=int(time.time()),
            model=self.model_name,
            object="text_completion",
            usage=usage,
        )
