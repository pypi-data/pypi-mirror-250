"""
 Copyright 2023 Bell Eapen

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""


from typing import List

from langchain_core.pydantic_v1 import BaseModel

from ..chains.rag_chain import get_tool as get_rag_tool
from ..tools.create_embedding import CreateEmbeddingTool
from ..tools.fhir_to_text import ConvertFhirToTextTool
from ..tools.find_patient import FhirPatientSearchTool
from .base_medprompt_agent import BaseMedpromptAgent


class FhirAgent(BaseMedpromptAgent):
    def __init__(
        self,
            llm = None,
            input_type: BaseModel = None,
            template_path=None,
            prefix=None,
            suffix=None,
            tools: List = [FhirPatientSearchTool(), CreateEmbeddingTool(), ConvertFhirToTextTool(), get_rag_tool],
        ):
        super().__init__(
            llm=llm,
            input_type=input_type,
            template_path=template_path,
            prefix=prefix,
            suffix=suffix,
            tools=tools,
        )


