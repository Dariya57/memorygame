from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

def game_view(request):
    return render(request, 'game/game.html')


# views.py (Django)
from django.http import JsonResponse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import random

# Game state
games = {}


def start(update: Update, context: CallbackContext):
    """Starts the game."""
    user_id = update.message.from_user.id
    games[user_id] = initialize_game()  # Initialize game for user
    update.message.reply_text("Welcome to the Memory Game! Press /play to start.")


def play(update: Update, context: CallbackContext):
    """Starts a new game and shows the buttons."""
    user_id = update.message.from_user.id
    game_state = games[user_id]
    markup = generate_keyboard(game_state)
    update.message.reply_text("Choose a card:", reply_markup=markup)


def generate_keyboard(game_state):
    """Generates a keyboard based on the game state."""
    buttons = []
    for row in game_state:
        button_row = [InlineKeyboardButton(text='?', callback_data='card_' + str(i)) for i in row]
        buttons.append(button_row)
    return InlineKeyboardMarkup(buttons)


def initialize_game():
    """Initialize game board with random pairs."""
    images = ["apple", "banana", "cherry", "date", "fig", "grape"] * 2  # Example pairs
    random.shuffle(images)
    return [images[i:i + 4] for i in range(0, len(images), 4)]  # 4 columns


def button_click(update: Update, context: CallbackContext):
    """Handles button clicks for card selection."""
    query = update.callback_query
    user_id = query.from_user.id
    game_state = games[user_id]

    # Logic to handle card flipping and game state updating goes here

    query.answer()


def main():
    """Starts the bot."""
    updater = Updater("YOUR_TOKEN")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("play", play))
    dp.add_handler(CallbackQueryHandler(button_click))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()