import os
import re
from slackclient import SlackClient
from flask import Flask, request, jsonify, abort
import game
import keys

SLACK_TOKEN = os.environ['SLACK_TOKEN']
## getting the SLACK_TOKEN from os env variable exported

active_games = {}
##THIS IS A TEST TOKEN AND NEEDS TO BE REMOVED WHEN OAUTH IS IMPLEMENTED

slack_client = SlackClient(SLACK_TOKEN)

#key for board to display for users in help
board_key =  "|  1  |  2  |  3  |\n|----+----+----|\n|  4  |  5  |  6  |\n|----+----+----|\n|  7  |  8  |  9  |"

app = Flask(__name__)

def setup():
    channels_call = slack_client.api_call("channels.list", exclude_archived=1)

    lookup_table = {}
    if channels_call.get('ok'):
        for channel in channel_call:
            lookup_table[channel['id']] = None
        return lookup_table
    return None

def validate_user():
    pass


def new_game(channel_id, player0, player1):
    #check if game exists in channel lookup
    test_game = active_games.get(channel_id, None)
    if test_game != None:
        message = {
            "response_type":"ephemeral",
            "text": "I'm sorry there is already an active game in this channel",
        }
    if (player1 == "") or (player0 == player1):
        #TODO stronger p1 validation against users list
          message = {
            "response_type":"ephemeral",
            "text": "That is not a valid opponent in this channel",
        }
    else:
        #TO DO validate both users are in channel and not deleted - (player1 not in channel_id.info.members) 
        new_game = game.Game()
        print(player0)
        print(player1)
        tempStr =player1.split("|")
        print tempStr
        player1 = tempStr[0][2:]
        print player1
        p0 = "<@"+player0+">"
       # print p1
        #set-up game Game(player1, player2)
        #return game message
        new_game.set_up(player0, player1)
        active_games[channel_id]=new_game
        message = {
            "response_type":"ephemeral",
            "text": "Please input a cell number with the command /ttt move # to make your first move\n" + board_key,
            }
    return message

def help(channel_id):
    help_str = "All possible commands for tic tac toe are below:\n /ttt help: list commands\n/ttt play @username: starts new game\n/ttt move #: adds an X or O to that space on the board\n/ttt quit: quit game\nTo make a move, select from the following space options:\n" + board_key + ""
    message = {
        "response_type": "ephemeral",
        "text": help_str,
        }
    return message

def end_game(channel_id, user_id):
    message = {
            "response_type": "ephemeral",
            "text": "Sorry that was invalid",
            }
    game_obj = active_games.get(channel_id, None)
    if game_obj == None:
        message = {
            "response_type":"ephemeral",
            "text": "Sorry there is no active game in this channel at this time."
        }
    return message
    if user_id != game_obj.player_1 or game_obj.player_0:
        message = {
            "response_type":"ephemeral",
            "text": "Don't be silly! You can't quit someone else's game"
        }
    if game_obj.end_condition == 0:
        #Call P0/Os Win Message 
        message = {
            "response_type": "in_channel",
            "text": "Hey !channel " + "we have a tic tac toe winner and it's: <@" + game_obj.player_0 + ">",
        }
    elif game_obj.end_condition == 3:
        #Call P1/Xs Win Message
        message = {
            "response_type": "in_channel",
            "text": "Hey !channel " + "we have a tic tac toe winner and it's: <@" + game_obj.player_1 + ">",
        }
    elif game_obj.end_condition == 4:
        #Call draw game
        message = {
            "response_type": "in_channel",
            "text": "Hey !channel this game is over and it ended in a draw :(",
        }
    else:
        message = {
            "response_type": "in_channel",
            "text": user_id + "Decided to quit the game :(",
        }

    active_games[channel_id]=None

    return message


def print_board(board):
    #input parameter: board list from Game class
    display_board = ""
    counter = 1
    for spot in board:
        if spot == 0:
            #append O to board spot
            display_board += "   :o:   "
        elif spot == 1:
            #aapend X to board spot
            display_board += "  :heavy_multiplication_x:  "
        elif spot == 9:
            #append blank to board spot
            display_board += "          "
        if counter in (1, 2, 4, 5, 7, 8):
            display_board += "|"
        if counter in (3, 6):
            display_board += "\n---------------------\n"
        counter +=1
    return display_board

def move(channel_id, request, player):
    game = active_games.get(channel_id, None)
    message = {
            "response_type": "ephemeral",
            "text": "Sorry that was invalid, please select a number from the following configuration",
            }
    if game == None:
        message = {
            "response_type": "ephemeral",
            "text": "Sorry there is no active game in this channel at this time.",
            }
        return message
    print "statement "+ game.player_1 + " and this is counter: " + str(game.turn_count) + " and this is p1 " + game.player_0 + " and this is player " + player
    #statement U7VQCMCKG and this is counter: 0 and this is p1 U7V2GQZ9T and this is player U7V2GQZ9T

    if (game.turn_count%2 == 0 and player != game.player_0) or (game.turn_count%2 == 1 and player != game.player_1):
        message = {
            "response_type": "ephemeral",
            "text": "Nice try! But it's not your turn",
        }
        return message
    try: 
        number = int(request)
    except:
        message = {
            "response_type": "ephemeral",
            "text": "That is not a valid move",
        }   
        return message
    if not game.is_free(number):
        message = {
            "response_type": "ephemeral",
            "text": "That is not a valid move",
        }
    #TO DO: verify player is in game and channel
    if player == game.player_0 and game.turn_count == 0:
        p0 = "<@"+player+">"
        #first move scenario
        game.turn(number)
        message = {
            "response_type":"in_channel",
            "text": "<@" + game.player_0 + "> has challenged <@" + game.player_1 + "> to a game of tic tac toe!\nCurrent board is "+print_board(game.board) + "\n<@" + game.player_1 + "> please make your move",
            }
    game.turn(number)
    message = {
        "response_type":"in_channel",
        "text": "current board status:\n" + print_board(game.board),
    }
    if game.check_win == True:
        return end_game(channel, player)
    else:
        return message

##if statement to determine responses to /ttt command 
##valid input params: command, @username, space to move
#ttt play @username - set up new game against that opponent
#ttt move # - makes a move by number space
#ttt quit - ends game in channel
#ttt help - displays all command options
@app.route('/', methods=['POST'])
def index():
    parameters = ['play','quit','move','help', 'gamestatus']
    info = request.form
    token = info.get('token', None) #VALIDATE TOKEN
    command = info.get('command', None) # do I need this?
    text = info.get('text', None)
    channel = info.get('channel_id')
    response = {
            "response_type": "ephemeral",
            "text":"I'm not sure what you are trying to say.\nPlease type /ttt help to see a list of valid commands",
            }
    ##if invalid token
    if token != SLACK_TOKEN:
        return "Invalid token for /ttt"
    if 'ttt' not in command:
        return "invalid request"

    if 'play' in text:
        p0 = info.get('user_id')
        p1 = str(text[5:])
        response = new_game(channel, p0, p1)

    if 'move' in text:
        space = str(text[5:])
        response = move(channel, space, info.get('user_id'))

    if text == 'quit':
        player = info.get('user_id')
        response = end_game(channel, player)

    if text == 'help':
        response = help(channel)

    print(response)
    return jsonify(response)


if __name__ == '__main__':
    app.debug = False
    app.run('0.0.0.0', 5000)