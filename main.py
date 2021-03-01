from fastapi import FastAPI, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from blackjack import BlackJack, Player
from typing import Optional
import random
from web3 import Web3
from pay_winner import pay

w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/4ef94712ce884095ad5a2404003f36e5'))
app = FastAPI()
templates = Jinja2Templates(directory='templates')
games = {}

#TODO check if address sent money on backend

@app.get('/test', response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse('test.html', {'request': request})

@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    id = random.randint(9999, 9999999)
    return templates.TemplateResponse('index.html', {'request': request, 'step': 1, 'id': id})

@app.post('/play/{id}', response_class=HTMLResponse)
async def home2(request: Request, id: int, step: Optional[int] = Form(None), move: Optional[str] = Form(None), addr: Optional[str] = Form(None)):

    #once the game is finished the new link is play/0 which redirects to the first page
    if id == 0:
        return RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)

    #try-except to check if there is already a game linked to the id sent
    try:
        game = games[id]
    except:
        pass
    if step == 1:
        if not Web3.isAddress(addr):
            return templates.TemplateResponse('index.html', {'request': request, 'error': 'Address not valid!', 'step': 1, 'id': random.randint(9999, 9999999)})

        games[id] = BlackJack(addr)
        game = games[id]
        first_move = game.start_game()
        return templates.TemplateResponse('index.html', {'request': request, 'dealer': [first_move[0][0], '*'], 'player': first_move[1], 'step': 2, 'id': id, 'sumP': game.players.value})
    else:
        if move == 'pass':
            result, dealer, player = game.verify(finish=1)
            if result == 'WIN':
                pay(game.address)
                print('{} got payed for the win'.format(game.address))

            del games[id]
            return templates.TemplateResponse('index.html', {'request': request, 'dealer': dealer, 'player': player, 'step': 1, 'res': result, 'id': 0, 'sumP': game.players.value, 'sumD': game.dealer.value})
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
                    pay(game.address)
                    print('{} got payed for the win'.format(game.address))

                del games[id]
                return templates.TemplateResponse('index.html', {'request': request, 'dealer': dealer, 'player': player, 'step': 1, 'res': result, 'id': 0, 'sumP': game.players.value, 'sumD': game.dealer.value})
            else:
                if response == 'WIN':
                    pay(game.address)
                    print('{} got payed for the win'.format(game.address))
                return templates.TemplateResponse('index.html', {'request': request, 'dealer': [dealer[0], '*'], 'player': player, 'step': 2, 'id': id, 'sumP': game.players.value})
        else:
            return templates.TemplateResponse('index.html', {'request': request, 'dealer': [game.dealer.cards[0], '*'], 'player': game.players.cards, 'step': 2, 'id': id, 'error': 'Command not valid!', 'sumP': game.players.value})


