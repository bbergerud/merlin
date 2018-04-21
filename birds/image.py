from .html  import *
from .utils import *
from skimage.io import imread
import matplotlib.pyplot as plt
import re, random

def get_image_urls(bird):
    url     = get_bird_url(bird) + 'id/'
    page    = get_page(url)
    soup    = get_soup(page)

    image  = soup.findAll('section', 'carousel wide id-carousel')[0]
    image  = image.findAll('img')
    image  = [img['data-interchange'].split('[')[-1].split(',')[0]
                for img in image]


    caption = soup.findAll('div', class_='annotation-txt')

    header = []
    for text in caption:
        content = re.search('<h5>(.*)</h5>', str(text))
        if isinstance(content, type(None)):
            header.append('')
        else:
            header.append(content.group(1))

    paragraph = []
    for text in caption:
        content = re.search('<p>(.*)</p>', str(text))
        if isinstance(content, type(None)):
            paragraph.append('')
        else:
            paragraph.append(content.group(1))

    caption = []
    for h, p in zip(header, paragraph):
        if h != '':
            caption.append('{:s}. {:s}'.format(h, p))
        else:
            caption.append('{:s}'.format(p))

    return image, caption


def image_quiz(birds, key='name', figsize=(7,7)):
    print('''
    This quiz tests your visual identificiation skills.

    If the links have not been stored, it may take a few moments
    to retrieve them depending on your internet connection.

    To exit the quiz, enter 'Q' for the input and press return.
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
    # if the image urls have been saved. If they
    # haven't then retrieve and store the links
    # =============================================
    image   = {}
    caption = {}
    for bird in birds.index:
        print('Getting image urls: {:s}'.format(bird))
        urls = load_urls(bird, 'image')
        text = load_urls(bird, 'caption')
        if not isinstance(urls, list):
            urls, text = get_image_urls(bird)
            save_urls(bird, urls, 'image')
            save_urls(bird, text, 'caption')
        image[bird]   = urls
        caption[bird] = text
    print('Image loading complete\n')

    # =============================================
    # Create a plot for displaying the images
    # =============================================
    fig, ax = plt.subplots(figsize=figsize)

    # =============================================
    # Begin the quiz
    # =============================================
    while True:

        # =============================================
        # Randomly sample a bird name
        # =============================================
        bird = random.choice(birds.index)

        # =============================================
        # Randomly select an image url and its caption
        # =============================================
        elem = random.randint(0, len(image[bird])-1)
        url  = image[bird][elem]
        text = caption[bird][elem]

        # =============================================
        # Display the image
        # =============================================
        ax.imshow(imread(url))
        fig.show()

        # =============================================
        # Get the user input
        # =============================================
        guess = input('{:s}: '.format(key.capitalize()))

        # =============================================
        # In the input is "q", then quit the quiz
        # Otherwise, check if the user was right
        # =============================================
        answer = bird if key == 'name' else birds.loc[bird, key]

        if guess.lower() == 'q':
            plt.close()
            break
        elif guess.lower() == answer:
            print('Correct!')
        else:
            print('Incorrect. The {:s} is {:s}'.format(
                key, answer)
            )
        print(caption[bird][elem])

        # =============================================
        # Wait for the user to indicate to move on
        # =============================================
        temp = input('Return to continue; Q to exit: ')
        if temp.lower() == 'q':
            plt.close()
            break
        print('\n')
