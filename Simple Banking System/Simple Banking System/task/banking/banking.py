import secrets
import sqlite3


class Card:

    def __init__(self, card_number, pin=None, balance=0):
        # if pin == None:
        #    self.set_pin()

        self.card_number = card_number
        self.pin = pin
        self.balance = balance

    def get_number(self):
        return self.card_number

    def get_balance(self):
        return self.balance

    def update_balance(self, balance):
        self.balance = balance

    def set_pin(self, pin=None):
        if pin is None:
            pin = []
            for i in range(4):
                pin.append(str(secrets.randbelow(10)))
            pin = ''.join(pin)

        self.pin = pin
        return pin

    def auth(self, pin):
        return self.pin == pin


# storage for cards, lol
class CardStorage:

    def __init__(self, iin):
        self.iin = iin
        self.table_name = 'card'
        self.connection = sqlite3.connect('card.s3db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS ' + self.table_name + ' ('
                            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                            'number TEXT NOT NULL,'
                            'pin TEXT NOT NULL,'
                            'balance INTEGER DEFAULT 0'
                            ');')
        self.connection.commit()

    def add(self, card_obj, pin):
        if not isinstance(card_obj, Card) or self.find(card_obj.get_number()) is not None:
            return

        self.cursor.execute('INSERT INTO ' + self.table_name + ' (number, pin)'
                            'VALUES (?,?);', (card_obj.get_number(), pin))
        self.connection.commit()

    def remove_card(self, card_number):
        # TODO
        pass

    def find(self, card_number):
        self.cursor.execute('SELECT number, pin, balance FROM ' + self.table_name + ' WHERE number = ?', (card_number,))
        result = self.cursor.fetchone()
        if result is None:
            return None
        return Card(result[0], result[1], result[2])

    def generate_num(self):
        while True:
            card_number = [ch for ch in self.iin]
            for i in range(9):
                card_number.append(str(secrets.randbelow(10)))

            card_number.append(self.count_lunh(card_number))

            card_number = ''.join(card_number)
            if self.find(card_number) is None:
                return card_number

    def create_card(self):
        card_number = self.generate_num()
        card_obj = Card(card_number)
        pin = card_obj.set_pin()
        self.add(card_obj, pin)
        return {'card_obj': card_obj, 'pin': pin}

    def sync(self, card_obj, diff=None):
        self.cursor.execute('SELECT FROM ' + self.table_name +
                            'balance'
                            'WHERE'
                            'number = ' + card_obj.get_number() + ';')
        result = self.cursor.fetchone()
        if result is not None:
            card_obj.update_balance(result[0])

    @staticmethod
    def count_lunh(self, card_number):
        card_number = [int(i) for i in card_number]
        for i in range(len(card_number)):
            if i % 2 == 0:
                card_number[i] *= 2
            if card_number[i] > 9:
                card_number[i] -= 9
        luhn_sum = 10 - (sum(card_number) % 10)
        if luhn_sum == 10:
            luhn_sum = 0
        return str(luhn_sum)


storage = CardStorage('400000')
stage = []
current_card = None

while True:
    if len(stage) == 0:
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        action = input().strip()
        if action == '1':
            stage.append('create')
        elif action == '2':
            stage.append('login')
        elif action == '0':
            stage.append('exit')

    elif stage[0] == 'create':
        print("Your card has been created")
        response = storage.create_card()

        print("Your card number:")
        print(response['card_obj'].get_number())

        print("Your card PIN:")
        print(response['pin'])

        stage.pop()

    elif stage[0] == 'login':
        print("Enter your card number:")
        card_number = input().strip()
        print("Enter your PIN:")
        pin = input().strip()

        card_obj = storage.find(card_number)

        if card_obj is not None and card_obj.auth(pin):
            print("You have successfully logged in!")
            current_card = card_obj
            stage.pop()
            stage.append('panel')
        else:
            print("Wrong card number or PIN!")
            stage.pop()
            continue
    elif stage[0] == 'panel':
        if len(stage) == 1:
            print("1. Balance")
            print("2. Add income")
            print("3. Do transfer")
            print("4. Close account")
            print("5. Log out")
            print("0. Exit")
            action = input().strip()
            if action == '1':
                storage.sync(current_card)
                print("Balance: " + str(current_card.get_balance()))
            elif action == '2':
                stage.append('add')
            elif action == '3':
                stage.append('transfer')
            elif action == '4':
                stage.append('close')
            elif action == '5':
                print("You have successfully logged out!")
                current_card = None
                stage.pop()
            elif action == '0':
                stage.pop()
                stage.append('exit')
        else:
            if stage[1] == 'add':
                pass
            elif stage[1] == 'transfer':
                print('Transfer')
                print('Enter card number:')
                card_number = input()
                recipient = storage.find(card_number)
                if recipient is None:
                    print('Such a card does not exist.')
                else:
                    
                stage.pop()
            elif stage[1] == 'close':
                pass

    elif stage[0] == 'exit':
        print("Bye!")
        break
