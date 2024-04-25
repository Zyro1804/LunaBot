import requests 
import openai 

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f'https://api.telegram.org/bot{token}/'

    def get_updates(self, offset=None):
        try:
            url = f'{self.base_url}getUpdates'
            params = {'offset': offset} if offset else {}
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json().get('result', [])
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Error while fetching updates: {e}")
            return []

    def send_message(self, chat_id, text):
        url = f'{self.base_url}sendMessage'
        data = {'chat_id': chat_id, 'text': text}
        requests.post(url, json=data)

class ChatGPT:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.openai.com/v1/engines/davinci-codex/completions'

    def generate_response(self, prompt):
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            data = {'prompt': prompt, 'max_tokens': 150}  # Aumenta el número de tokens para respuestas más largas
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()['choices'][0]['text']
        except requests.exceptions.RequestException as e:
            print(f"Error while generating response: {e}")
            return "Lo siento, no pude generar una respuesta en este momento."

def main():
    telegram_token = '6886210264:AAGcWoZZnUlABLZ0M_wl4-_YxLzKxgacLLc'
    chatgpt_api_key = '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'

    telegram_bot = TelegramBot(telegram_token)
    chatgpt = ChatGPT(chatgpt_api_key)

    last_update_id = None
    while True:
        updates = telegram_bot.get_updates(last_update_id)
        for update in updates:
            last_update_id = update['update_id'] + 1
            message = update.get('message', {})
            chat_id = message.get('chat', {}).get('id')
            text = message.get('text')

            if chat_id and text:
                # Respuesta inicial del bot
                response = "Hola, me llamo Luna una inteligencia artifical de ayuda psicológica. Puedo proporcionarte apoyo emocional y escucharte. ¿Cómo te sientes hoy?"
                
                # Generar respuesta utilizando ChatGPT
                chatgpt_response = chatgpt.generate_response(text)
                response += f"\n\n{chatgpt_response}"
                
                # Enviar respuesta al usuario
                telegram_bot.send_message(chat_id, response)

if __name__ == '__main__':
    main()