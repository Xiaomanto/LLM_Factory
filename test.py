from chatModelService.ServiceFactory import ServiceFactory

ollama = ServiceFactory().getService(types='ollama',model="llama3.1",api_key="ollama")
print(ollama.Chat("美國總統是川普嗎"))