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

import logging
import os
from typing import Any, Optional, Type

from kink import di
from langchain.callbacks.manager import (AsyncCallbackManagerForToolRun,
                                         CallbackManagerForToolRun)
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain.vectorstores import FAISS, Chroma, Redis

from .. import MedPrompter, get_time_diff_from_today
from ..utils.get_medical_record import GetMedicalRecordUtil

logger = logging.getLogger(__name__)


class SearchInput(BaseModel):
    patient_id: str = Field()

class CreateEmbeddingTool(BaseTool):
    """
    Creates an embedding for a patient with id.
    """
    name = "create index for medical record"
    description = """
    Creates a medical record index for a patient with patient_id.
    """
    args_schema: Type[BaseModel] = SearchInput

    # Embedding model
    EMBED_MODEL = di["embedding_model"]

    # Create vectorstore
    embedder = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    # Index schema
    INDEX_SCHEMA = di["index_schema"]
    VECTORSTORE_NAME = di["vectorstore_name"]
    REDIS_URL = di["redis_url"]

    def _run(
            self,
            patient_id: str = None,
            run_manager: Optional[CallbackManagerForToolRun] = None
            ) -> str:
        prompt = MedPrompter()
        bundle_input = GetMedicalRecordUtil().run(patient_id=patient_id)
        chunks = self._process_entries(prompt, bundle_input, patient_id)
        logging.info("Number of chunks in the vector db: {}".format(len(chunks)))

        # Store in Redis
        if self.VECTORSTORE_NAME == "redis":
            db = Redis.from_texts(
                # appending this little bit can sometimes help with semantic retrieval
                # especially with multiple companies
                # texts=[f"Company: {company_name}. " + chunk["page_content"] for chunk in chunks],
                texts=[chunk["page_content"] for chunk in chunks],
                metadatas=[chunk["metadata"] for chunk in chunks],
                embedding=self.embedder,
                index_name=patient_id,
                # index_schema=self.INDEX_SCHEMA,
                redis_url=self.REDIS_URL
            )
            db.write_schema(self.INDEX_SCHEMA)

        # Store in Chroma
        elif self.VECTORSTORE_NAME == "chroma":
            db = Chroma.from_texts(
                persist_directory=di["vectorstore_path"],
                texts=[chunk["page_content"] for chunk in chunks],
                metadatas=[chunk["metadata"] for chunk in chunks],
                embedding=self.embedder,
                ids=[chunk["metadata"]["resourceID"] for chunk in chunks],
                collection_name=patient_id
            )

        # Store in FAISS
        elif self.VECTORSTORE_NAME == "faiss":
            fname = di["vectorstore_path"] + "/" + patient_id + ".index"
            if not os.path.exists(fname):
                db = FAISS.from_texts(
                    texts=[chunk["page_content"] for chunk in chunks],
                    metadatas=[chunk["metadata"] for chunk in chunks],
                    embedding=self.embedder,
                )
                db.save_local(fname)
        return "Embeddings created for patient with id: {}".format(patient_id)

    async def _arun(
            self,
            patient_id: str = None,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None
            ) -> Any:
        raise NotImplementedError("Async not implemented yet")
        # return self._run(patient_id, run_manager)


    #* Override if required
    def _process_entries(self, prompt, bundle, patient_id):
        chunks = []
        for entry in bundle["entry"]:
            resource = entry["resource"]

            if resource["resourceType"] == "Patient" or resource["resourceType"] == "Observation" \
                or resource["resourceType"] == "DocumentReference":
                resource["time_diff"] = get_time_diff_from_today
                template_name = resource['resourceType'].lower() + "_v1.jinja"
                prompt.set_template(template_name=template_name)
                chunk = {
                    "page_content": prompt.generate_prompt(resource).replace("\n", " "),
                    "metadata": {
                        "resourceType": resource["resourceType"],
                        "resourceID": str(resource["id"]),
                        "patientID": str(patient_id)
                    }
                }
                chunks.append(chunk)
        return chunks