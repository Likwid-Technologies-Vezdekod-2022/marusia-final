from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from random import randint


class MarusiaRouter(APIView):
    card_map = {
        2: 'Валет',
        3: "Дама",
        4: "Король",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "10",
        11: "Туз"
    }

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

    def card_decode(self, card):
        return self.card_map[card]

    @staticmethod
    def get_random_card():
        return randint(2, 11)

    def router(self, data):
        if 'cards_sum' in self.state:
            return self.twenty_one_in_progress(data['request']['command'], self.state['cards_sum'], self.state['cards_count'])
        return self.game_menu(data['request']['command'])

    def game_menu(self, command: str):
        if command.lower() == 'двадцать один':
            return self.twenty_one_start()

    def twenty_one_start(self):
        cards = [self.get_random_card() for i in range(2)]
        self.response['response'] = {
            'text': f'Вы вытянули 2 карты {self.card_decode(cards[0])} и {self.card_decode(cards[1])}',
            'end_session': False,
        }
        self.response['session_state']['cards_sum'] = sum(cards)
        self.response['session_state']['cards_count'] = 2
        if sum(cards) == '21':
            self.response['response']['text'] = 'Вы выйграли у вас туз и 10'
            self.response['response']['end_session'] = True
        return self.response

    def twenty_one_in_progress(self, command, last_sum, last_count):
        if command.lower() == 'ещё':
            card = self.get_random_card()
            if card + last_sum > 21:
                self.response['response'] = {
                    'text': f'Вы вытянули {self.card_decode(card)}, вы проиграли',
                    'end_session': True,
                }
            elif card + last_sum == 21:
                self.response['response'] = {
                    'text': f'Вы набрали 21 очко, вы победили, урааа',
                    'end_session': True
                }
            else:
                self.response['response'] = {
                    'text': f'Вы вытянули {self.card_decode(card)}, у вас {last_sum + card} очка(ов)',
                    'end_session': False,
                }
                self.response['session_state']['cards_sum'] = card + last_sum
                self.response['session_state']['cards_count'] = 1 + last_count
        else:
            self.response['response'] = {
                'text': f'Вы набрали {last_sum} очков',
                'end_session': True,
            }
        return self.response
