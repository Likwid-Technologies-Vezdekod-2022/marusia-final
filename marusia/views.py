from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from random import randint, choice


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
    eatable = [
        'Яблоко',
        'Груша',
        'Пончик',
        'Помидор',
        'Белый гриб',
    ]
    uneatable = [
        'Арматура',
        'Сверлильный станок',
        'Компьютер',
        'Волчья ягода',
        'Мухомор',
        'Телефон',
        'Пианино',
    ]

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
        if 'eat_count' in self.state:
            return self.eat_in_progress(data['request']['command'], self.state['eat_count'])
        return self.game_menu(data['request']['command'])

    def game_menu(self, command: str):
        if command.lower() == 'двадцать один':
            return self.twenty_one_start()
        if command.lower() == 'съедобное не съедобное':
            return self.eat_start()
        return self.get_help_response()

    def eat_start(self):
        self.response['response'] = {
            'text': f'Вы зашли в игру съедобное/не съедобное',
            'end_session': False,
        }
        self.response['session_state']['eat_count'] = 0
        self.response['session_state']['food'] = choice(self.eatable) if randint(0, 1) else choice(self.uneatable)
        return self.response

    def eat_in_progress(self, command, last_count):
        pass

    def get_help_response(self):
        self.response['response'] = {
            'text': 'Команды:\n Двадцать один \n Съедобное не съедобное \n',
            'end_session': True
        }
        return self.response

    def twenty_one_start(self):
        user_cards = [self.get_random_card() for i in range(2)]
        bot_cards = [self.get_random_card() for i in range(randint(2, 4))]
        self.response['response'] = {
            'text': f'Вы вытянули 2 карты {self.card_decode(user_cards[0])} и {self.card_decode(user_cards[1])}',
            'end_session': False,
        }
        self.response['session_state']['user_cards_sum'] = sum(user_cards)
        self.response['session_state']['bot_cards_sum'] = sum(bot_cards)
        return self.response

    def twenty_one_in_progress(self, command, last_sum, bot_sum):
        if command.lower() == 'ещё':
            card = self.get_random_card()
            if card + last_sum > 21:
                if bot_sum > card + last_sum:
                    self.response['response'] = {
                        'text': f'Вы вытянули {self.card_decode(card)}, вы набрали {last_sum + card} очков, у бота {bot_sum}, вы побелили',
                        'end_session': True,
                    }
                else:
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
                self.response['session_state']['cards_count'] = bot_sum
        elif 'всё' == command.lower():
            self.response['response'] = {
                'text': f'Вы набрали {last_sum} очков',
                'end_session': True,
            }
            if bot_sum > last_sum:
                self.response['response']['text'] += 'Вы проиграли'
            else:
                self.response['response']['text'] += 'Вы выйграли'
        else:
            self.response['response'] = {
                'text': f'Напишите либо ещё, либо всё',
                'end_session': False,
            }
        return self.response
