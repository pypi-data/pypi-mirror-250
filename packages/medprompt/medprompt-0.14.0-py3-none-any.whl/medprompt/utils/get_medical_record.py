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

from typing import Any
from kink import inject
import logging
_logger = logging.getLogger(__name__)
from ..utils.fhir_server import FhirServer


@inject # Constructor injection will happen here
class GetMedicalRecordUtil:

    def __init__(self, fhir_server: FhirServer):
        self.fhir_server = fhir_server

    def run(
            self,
            patient_id: str = None,
            ) -> Any:
        query = self._format_query(patient_id)
        _response = self.fhir_server.call_fhir_server(query, params=None)
        if _response["total"] >1000:
            _logger.info("Patient record too large")
            return "Sorry, the patient's record is too large to be loaded."
        elif _response["total"] < 1:
            _logger.info("Patient record not found")
            return "This patient does not have a record."
        return _response

    async def arun(
            self,
            patient_id: str = None,
            ) -> Any:
        query = self._format_query(patient_id)
        _response = await self.fhir_server.async_call_fhir_server(query, params=None)
        if _response["total"] >100:
            _logger.info("Patient record too large")
            return "Sorry, the patient's record is too large to be loaded."
        elif _response["total"] < 1:
            _logger.info("Patient record not found")
            return "This patient does not have a record."
        return _response

    def _format_query(self, patient_id):
        query = "Patient?"
        if patient_id:
            query += "_id="+patient_id
            query += "&_revinclude=Observation:subject"
            query += "&_revinclude=Condition:subject"
            query += "&_revinclude=Procedure:subject"
            query += "&_revinclude=MedicationRequest:subject"
        return query
