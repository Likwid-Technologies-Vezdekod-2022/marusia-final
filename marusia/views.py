from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from random import randint


class MarusiaRouter(APIView):
    def post(self, request):
        data = request.data
        self.state = data['state']['session']
        self.response = {
            'response': {
                'text': 'Неизвестная команда\nСписок команд:\nпомогите: Список команд\nlikwid technologies '
                        'вездекод: Привет вездекодерам!\nОпросник: Список последовательно задаваемых вопросов\n\n '
                        'Команды работают с любым регистром',
                'tts': 'неизвестная команда',
                'end_session': True
            },
            'version': '1.0',
            'session': data['session'],
            'session_state': {}
        }
        return Response(self.router(data), status.HTTP_200_OK)

    def get_random_card(self):
        return randint(2, 11)

    def router(self, data):
        if 'prev_question' in self.state:
            pass
        return self.game_menu(data['request']['command'])

    def game_menu(self, command: str):
        if command.lower() == 'двадцать один':
            return self.twenty_one_start()

    def twenty_one_start(self):
        cards = [self.get_random_card() for i in range(2)]
        self.response['response'] = {
            'text': f'Вы вытянули 2 карты {cards[0]} и {cards[1]}',
            'end_session': False,
        }
        self.response['session_state']['cards_sum'] = sum(cards)
        self.response['session_state']['cards_count'] = "2"
        return self.response

    def twenty_one_in_progress(self, command):
        if command.lower() == 'ещё':
            new_card = self.get_random_card()
