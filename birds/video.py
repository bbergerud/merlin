from .html  import *
from .utils import *
import vimeo_dl as vimeo
import random
import vlc
#import time

def store_vimeo_urls(birds):
    for bird in birds.index:
        print('Getting vimeo links: {:s}'.format(bird))
        filename = get_filename(bird, 'video') + '.txt'
        if os.path.exists(filename):
            continue
        vimeo = get_vimeo_urls(bird)
        if isinstance(vimeo, list):
            save_urls(bird, vimeo, 'video')

def get_vimeo_urls(bird):
    url  = get_bird_url(bird) + 'id/'
    page = get_page(url)
    soup = get_soup(page)

    # =========================================
    # Find a link to the media-browser page
    # =========================================
    stop_bool = True
    links = soup.findAll('a')
    for link in links:
        try:
            href = link['href']
            media = 'media-browser' in href
            guide = href[:7] == '/guide/'
            if media and guide:
                ending = href.split('/')[-1]
                if len(ending) == 6:
                    url = href
                    stop_bool = False
                    break
        except:
            continue

    # =========================================
    # Boolean check if there were any videos
    # =========================================
    if stop_bool:
        print('No videos for {:s}'.format(bird))
        return

    # =========================================
    # Get the content on the media-browser page
    # and find the <iframe> elements.
    # =========================================
    page = get_page('https://www.allaboutbirds.org' + url)
    soup = get_soup(page)

    videos = soup.findAll('iframe')
    videos = [
        video['src'].replace('player.', '').replace('video/', '')
        for video in videos
    ]

    return videos

def get_video_urls(vimeo_urls):
    urls = []
    for url in vimeo_urls:
        video = vimeo.new(url)
        best = video.getbest()
        urls.append(best.url)
    return urls


def video_quiz(birds, key='name'):
    print('''
    This quiz tests your visual/ audio identificiation skills
    by showing video clips.

    The url addresses have a ~1 hour self life, so if they stop
    working exit the quiz and start again.

    To exit the quiz, enter 'Q' for the input and press return.
    To replay the video, enter 'R' and press return
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
    # if the vimeo urls have been saved. If they
    # haven't then retrieve and store the links
    # =============================================
    #start_time = time.time()

    video = {}
    for bird in birds.index:
        print('Getting video links: {:s}'.format(bird))
        vimeo = load_urls(bird, 'video')
        if not isinstance(vimeo, list):
            print('Failed to load links: {:s}'.format(bird))
            continue
            #vimeo = get_vimeo_urls(bird)
            #if not isinstance(vimeo, list):
            #    print('Failed to load links: {:s}'.format(bird))
            #    continue
            #save_urls(bird, vimeo, 'video')
        urls = get_video_urls(vimeo)
        video[bird] = urls
    print('Video loading complete\n')

    # =============================================
    # Begin the quiz
    # =============================================
    while True:

        # =============================================
        # Randomly sample a bird name
        # =============================================
        bird = random.choice(birds.index)

        # =============================================
        # Randomly select a video url for the bird.
        # Since not all birds have an associated video,
        # there needs to be a check to make sure there
        # is a valid url
        # =============================================
        try:
            url = random.choice(video[bird])
        except:
            continue

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

        """
        if (time.time() - start_time) / 60 > timer:
            start_time = time.time()
            for bird in birds.index:
                print('Getting video links: {:s}'.format(bird))
                vimeo = load_urls(bird, 'video')
                urls = get_video_urls(vimeo)
                video[bird] = urls
        """
