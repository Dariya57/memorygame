from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import random

# Initialize the game state
game_state = {
    'board': [],
    'flipped': [],
    'moves': 0,
    'matches': 0
}

# Initialize the board with pairs of emojis
def initialize_board():
    emojis = ['🍎', '🍌', '🍒', '🍇', '🍉', '🍓', '🍍', '🥝']
    board = emojis * 2
    random.shuffle(board)
    return board

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    game_state['board'] = initialize_board()
    game_state['flipped'] = []
    game_state['moves'] = 0
    game_state['matches'] = 0
    update.message.reply_text('Memory Game started! Use /flip <position> to flip a card.')

# Flip command handler
def flip(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1 or not context.args[0].isdigit():
        update.message.reply_text('Usage: /flip <position> (0-15)')
        return

    position = int(context.args[0])
    if position < 0 or position >= 16:
        update.message.reply_text('Position must be between 0 and 15.')
        return

    if position in game_state['flipped']:
        update.message.reply_text('Card already flipped.')
        return

    game_state['flipped'].append(position)
    game_state['moves'] += 1

    if len(game_state['flipped']) == 2:
        check_match(update)

    update.message.reply_text(display_board())

# Check for a match
def check_match(update: Update) -> None:
    pos1, pos2 = game_state['flipped']
    if game_state['board'][pos1] == game_state['board'][pos2]:
        game_state['matches'] += 1
        update.message.reply_text('Match found!')
    else:
        update.message.reply_text('No match. Try again.')
        game_state['flipped'] = []

# Display the board
def display_board() -> str:
    board_display = ''
    for i in range(16):
        if i in game_state['flipped']:
            board_display += f'{game_state["board"][i]} '
        else:
            board_display += '❓ '
        if (i + 1) % 4 == 0:
            board_display += '\n'
    return board_display

def main() -> None:
    updater = Updater("7792728038:AAH_1QdHeRR7Ld_GLQsoONyOh9viyaIdFvs")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("flip", flip))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
