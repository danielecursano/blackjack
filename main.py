from fastapi import FastAPI, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from blackjack import BlackJack, Player
from typing import Optional
import random
from web3 import Web3
from api_utils import pay, verify_transaction
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
url = config['cheapeth']['url']
w3 = Web3(Web3.HTTPProvider(url))

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')
games = {}

@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    id = random.randint(9999, 9999999)
    return templates.TemplateResponse('index.html', {'request': request, 'step': 1, 'id': id})

@app.post('/play/{id}', response_class=HTMLResponse)
async def home2(request: Request, id: int, step: Optional[int] = Form(None), move: Optional[str] = Form(None), addr: Optional[str] = Form(None), txHash: Optional[str] = Form(None)):
    #redirect to homepage once the game is finished  
    if id == 0:
        return RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)
    #var error = None changes to string in case of error and returned in the html page
    error = None
    if step == 1:
        if not Web3.isAddress(addr):
            return templates.TemplateResponse('index.html', {'request': request, 'error': 'Address not valid!', 'step': 1, 'id': random.randint(9999, 9999999)})
        if id in games:
            game = games[id]
            first_move = game.dealer.cards, game.players.cards
        else:
            games[id] = BlackJack(addr=addr, txHash=txHash)
            game = games[id]
            first_move = game.start_game()
        if verify_transaction(game.txHash, game.address):
            return templates.TemplateResponse('index.html', {'request': request, 'dealer': [first_move[0][0], '*'], 'player': first_move[1], 'step': 2, 'id': id, 'sumP': game.players.value})

        del games[id]
        return templates.TemplateResponse('index.html', {'request': request, 'error': 'invalid transaction', 'step': 1, 'id': random.randint(9999, 999999999)})
    else:
        try:
            game = games[id]
        except:
            return RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)
        if move == 'pass':
            result, dealer, player = game.verify(finish=1)
            if result == 'WIN':
                if pay(game.address, game.txHash):
                    print('{} got payed for the win'.format(game.address))
                else:
                    error = "Invalid Transaction"

            del games[id]
            return templates.TemplateResponse('index.html', {'request': request, 'error': error, 'dealer': dealer, 'player': player, 'step': 1, 'res': result, 'id': 0, 'sumP': game.players.value, 'sumD': game.dealer.value})
        if move == 'card':
            game.players.cards.append(game.extract())
            response, dealer, player = game.verify()
            if not response:
                del games[id]
                result = 'LOSE'
                return templates.TemplateResponse('index.html', {'request': request, 'dealer': dealer, 'player': player, 'step': 1, 'res': result, 'id': 0, 'sumP': game.players.value, 'sumD': game.dealer.value})
            if sum(player) == 21:
                result, dealer, player = game.verify(finish=1)
                if result == 'WIN':
                    if pay(game.address, game.txHash):
                        print('{} got payed for the win'.format(game.address))
                    else:
                        error = "Invalid Transaction"

                del games[id]
                return templates.TemplateResponse('index.html', {'request': request, 'error': error, 'dealer': dealer, 'player': player, 'step': 1, 'res': result, 'id': 0, 'sumP': game.players.value, 'sumD': game.dealer.value})
            else:
                if response == 'WIN':
                    if pay(game.address, game.txHash):
                        print('{} got payed for the win'.format(game.address))
                    else:
                        error = "Invalid Transaction"
                return templates.TemplateResponse('index.html', {'request': request, 'error': error, 'dealer': [dealer[0], '*'], 'player': player, 'step': 2, 'id': id, 'sumP': game.players.value})
        else:
            return templates.TemplateResponse('index.html', {'request': request, 'dealer': [game.dealer.cards[0], '*'], 'player': game.players.cards, 'step': 2, 'id': id, 'error': 'Command not valid!', 'sumP': game.players.value})



