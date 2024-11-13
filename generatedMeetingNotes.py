import requests
import json

class contentGenerationAPI:
    # set API URL for watsonxPrompterAPI - granite-13b-chat
    API_URL = "http://127.0.0.1:8000/shotPrompts"

    def __init__(self, exampleInputs, exampleOutputs, systemPrompt, userPrompt, inputData):
        self.systemPrompt = systemPrompt
        self.userPrompt = userPrompt
        self.exampleInputs = exampleInputs
        self.exampleOutputs = exampleOutputs
        self.inputData = inputData

    def callMultiShot(self):
        headers = {
            "Content-Type":"application/json"
        }
        requestBody = {
            "systemPrompt": self.systemPrompt,
            "userPrompt": self.userPrompt,
            "exampleInputs": self.exampleInputs,
            "exampleOutputs": self.exampleOutputs,
            "inputData": self.inputData
        }
        jsonRequest = json.dumps(requestBody)
        contentResponse = requests.post(url=self.API_URL, headers=headers, data=jsonRequest)
        jsonContentResponse = json.loads(contentResponse.text)
        self.contentResponse = jsonContentResponse


def watsonxContentGeneration(data):
    content = contentGenerationAPI(data["exampleInputs"],data["exampleOutputs"], data["systemPrompt"], data["userPrompt"], data["inputData"])
    content.callMultiShot()
    return content.contentResponse["watsonxGeneratedResult"]
