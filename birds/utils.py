import os

def clean_bird_name(bird):
    bird = bird.replace(' ', '_')
    bird = bird.replace('\'', '')
    return bird

def get_base_dir(key):
    dir = os.path.dirname(__file__)
    dir = os.path.join(dir, 'resources', key)
    if not os.path.exists(dir):
        os.mkdir(dir)
    return dir

def get_filename(bird, key):
    bird = clean_bird_name(bird)
    return os.path.join(get_base_dir(key), bird)

def load_urls(bird, key):
    try:
        filename = get_filename(bird=bird, key=key)
        with open(filename + '.txt', 'r') as f:
            urls = f.readlines()
        return [url.strip() for url in urls]
    except:
        return None


def save_urls(bird, urls, key):
    try:
        filename = get_filename(bird=bird, key=key)
        with open(filename + '.txt', 'w') as f:
            for url in urls:
                f.write(url + '\n')
    except:
        print('Failed to save {:s} url'.format(key))
