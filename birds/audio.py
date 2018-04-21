from .html  import *
from .utils import *
import random
import vlc

def get_audio_urls(bird_name):
    url   = get_bird_url(bird_name) + 'sounds'
    page  = get_page(url)
    soup  = get_soup(page)
    audio = soup.findAll('div', class_='jp-jplayer player-audio')
    audio = [content['name'] for content in audio]
    return audio



def audio_quiz(birds, key='name'):
    print('''
    This quiz tests your audio identificiation skills.

    If the links have not been stored, it may take a few moments
    to retrieve them depending on your internet connection.

    To exit the quiz, enter 'Q' for the input and press return.
    To replay the sound, enter 'R' and press return
    ''')

    # =============================================
    # Use lowercase for the key
    # =============================================
    key = key.lower()
    if (key not in birds.columns) and (key != 'name'):
        print('not a valid key: {:s}'.format(key))
        return

    # =============================================
    # Iterate through each bird name and check
    # if the audio urls have been saved. If they
    # haven't then retrieve and store the links
    # =============================================
    audio = {}
    for bird in birds.index:
        print('Getting audio links: {:s}'.format(bird))
        urls = load_urls(bird, 'audio')
        if not isinstance(urls, list):
            urls = get_audio_urls(bird)
            save_urls(bird, urls, 'audio')
        audio[bird] = urls
    print('Audio loading complete\n')

    # =============================================
    # Begin the quiz
    # =============================================
    while True:

        # =============================================
        # Randomly sample a bird name
        # =============================================
        bird = random.choice(birds.index)

        # =============================================
        # Randomly select an audio url
        # =============================================
        url = random.choice(audio[bird])

        # =============================================
        # Play the audio to the user
        # =============================================
        player = vlc.MediaPlayer(url)
        player.play()

        # =============================================
        # Get the user input.
        # If the input is "r", then repeat the clip
        # =============================================
        guess = input('{:s}: '.format(key.capitalize()))
        while guess.lower() == 'r':
            player.stop()
            player.play()
            guess = input('{:s}: '.format(key.capitalize()))
        player.stop()

        # =============================================
        # In the input is "q", then quit the quiz
        # Otherwise, check if the user was right
        # =============================================
        answer = bird if key == 'name' else birds.loc[bird, key]

        if guess.lower() == 'q':
            break
        elif guess.lower() == answer:
            print('Correct!\n')
        else:
            print('Incorrect. The {:s} is {:s}\n'.format(
                key, answer)
            )
