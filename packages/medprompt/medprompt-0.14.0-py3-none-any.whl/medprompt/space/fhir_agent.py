from agency.agent import Agent, action

from ..agents.fhir_agent import FhirAgent


class SpaceFhirAgent(Agent):

    @action
    def say(self, content: str, current_patient_context: str = ""):
        """Search for a patient in the FHIR database."""
        #! TODO: Needs bootstrapping here.

        message = {
            "input": content,
            "current_patient_context": current_patient_context,
        }
        response_content = FhirAgent().get_agent().invoke(message)
        self.send({
          "to": self.current_message()['from'],
          "action": {
            "name": "say",
            "args": {
                "content": response_content["output"],
            }
          }
        })
        return True