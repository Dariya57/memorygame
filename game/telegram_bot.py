import os
import django
from memory_game.views import main

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'memory_game.settings')
django.setup()

if __name__ == '__main__':
    main()