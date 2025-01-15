from LlmServiceFactory import BaseService

ollama = BaseService(model="llama3.1",api_key="ollama",types='ollama',)
print(ollama.Chat("美國總統是川普嗎"))