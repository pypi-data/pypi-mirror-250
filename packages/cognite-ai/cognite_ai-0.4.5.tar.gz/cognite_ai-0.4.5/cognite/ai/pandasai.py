from cognite.client import CogniteClient

import pandas as pd
from typing import Optional
import asyncio
import sys
import site
import os

is_patched = False
_RUNNING_IN_BROWSER = sys.platform == "emscripten" and "pyodide" in sys.modules

async def patch_pandasai():
    import micropip
    import sys

    # Need to mock OpenAI class and DuckDB class
    class MockOpenAI:
        def __getattr__(self, attr):
            return "If you need openai package, restart notebook"

    class MockDuckDb:
        def connect(self, path):
            pass
    
    sys.modules["openai"] = MockOpenAI()
    sys.modules["openai.openai_object"] = MockOpenAI()
    sys.modules["duckdb"] = MockDuckDb()

    await micropip.install("pandasai==1.5.8", deps=False)
    await micropip.install("pydantic<2")
    await micropip.install("astor==0.8.1")
    await micropip.install("sqlalchemy==2.0.7")

    site_packages_dir = site.getsitepackages()[0]
    
    # dotenv is not available in pyodide.
    # we therefor just mock the _load_dotenv function
    # and skip the import of dotenv in env.py, line 1
    env_py_path = os.path.join(site_packages_dir, "pandasai", "helpers", "env.py")
    
    with open(env_py_path) as f:
        lines = f.readlines()
    skip_lines = [1] # Skip import of dotenv
    with open(env_py_path, "w") as f:
        f.write("def _load_dotenv(dotenv_path):\n    pass\n\n")
        for i in range(0,len(lines)):
            if i not in skip_lines:
                f.write(lines[i])
    
    # The pipeline always tries to create a Cache which uses DuckDB
    # which is not available in pyodide. We therefor override and don't use cache
    pipeline_context_path = os.path.join(site_packages_dir, "pandasai", "pipelines", "pipeline_context.py")
    
    with open(pipeline_context_path) as f:
        content = f.read()
    content = content.replace(
        "self._cache = cache if cache is not None else Cache()",
        "self._cache = cache")
    with open(pipeline_context_path, "w") as f:
        f.write(content)

async def load_pandasai():
    # TODO: This is a series of hacks to make pandasai work in JupyterLite
    # Multiple of these hacks are workarounds for aiohttp 3.6.2 does not work
    # with Python 3.11, and later packages don't exist as pure python wheels.
    # However, we are not using them, this is only happening because openai is not
    # an optional package, and we are providing our own LLM into this mix.
    # In addition, we are using a wip duckdb implementation which can be fully
    # mocked as long as we don't use caching.

    global is_patched
    if not is_patched and _RUNNING_IN_BROWSER:
        await patch_pandasai()

    from pandasai.llm import LLM
    from pandasai import SmartDataframe as SDF
    from pandasai import SmartDatalake as SDL

    class CogniteLLM(LLM):
        cognite_client = CogniteClient
        temperature = 0.0
        model = "gpt-35-turbo"
        max_tokens = 1000
        frequency_penalty = 0
        presence_penalty = 0.6
        stop: Optional[list[str]] = None
        
        def __init__(self, cognite_client, params):
            LLM.__init__(self)
            self.validate_params(params)
            
            self.cognite_client = cognite_client
            self.model = params.get("model", self.model)
            self.temperature = params.get("temperature", self.temperature)
            self.max_tokens = params.get("maxTokens", self.max_tokens)
            self.frequency_penalty = params.get("frequencyPenalty", self.frequency_penalty)
            self.presence_penalty = params.get("presencePenalty", self.presence_penalty)
            self.stop = params.get("stop", self.stop)
        
        def validate_params(self, params):
            valid_models = ["gpt-35-turbo", "gpt-35-turbo-16k", "gpt-4", "gpt-4-32k"]
            if "model" in params:
                if params['model'] not in valid_models:
                    raise ValueError(f"model must be one of {valid_models}")
            if "temperature" in params:
                if params['temperature'] < 0:
                    raise ValueError("temperature must be at least 0")
            if "maxTokens" in params:
                if params['maxTokens'] < 1:
                    raise ValueError("maxTokens must be at least 1")
            
        def _set_params(self, **kwargs):
            """
            Set Parameters
            Args:
                **kwargs: ["model", "temperature","maxTokens",
                "frequencyPenalty", "presencePenalty", "stop", ]

            Returns:
                None.

            """

            valid_params = [
                "model",
                "temperature",
                "maxTokens",
                "frequencyPenalty",
                "presencePenalty",
                "stop",
                "model",
            ]
            for key, value in kwargs.items():
                if key in valid_params:
                    setattr(self, key, value)

        @property
        def _default_params(self):
            """
            Get the default parameters for calling OpenAI API

            Returns
                Dict: A dict of OpenAi API parameters.

            """

            return {
                "temperature": self.temperature,
                "maxTokens": self.max_tokens,
                "frequencyPenalty": self.frequency_penalty,
                "presencePenalty": self.presence_penalty,
                "model": self.model
            }

        def chat_completion(self, value):
            body = {
                    "messages": [
                        {
                            "role": "system",
                            "content": value,
                        }
                    ],
                    **self._default_params,
                }
            response = self.cognite_client.post(
                url=f"/api/v1/projects/{self.cognite_client.config.project}/gpt/chat/completions",
                json=body
            )
            return response.json()["choices"][0]["message"]["content"]
        
        def call(self, instruction, suffix = ""):
            self.last_prompt = instruction.to_string() + suffix
            
            response = self.chat_completion(self.last_prompt)
            return response

        @property
        def type(self) -> str:
            return "cognite"

            
    class SmartDataframe(SDF):
        def __init__(self, df: pd.DataFrame, cognite_client: CogniteClient, params: dict = {}):
            llm = CogniteLLM(cognite_client=cognite_client, params=params)
            super().__init__(df, config={"llm": llm, "enable_cache": False})
    
    class SmartDatalake(SDL):
        def __init__(self, dfs: list[pd.DataFrame], cognite_client: CogniteClient, params: dict = {}):
            llm = CogniteLLM(cognite_client=cognite_client, params=params)
            super().__init__(dfs, config={"llm": llm, "enable_cache": False})
    
    return SmartDataframe, SmartDatalake