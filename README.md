# Bird Identification

This is a basic interface to the audio and image files at [The Cornell Lab of Ornithology](https://www.allaboutbirds.org).

## Code

The file "base.py" is basic script for starting things up in a python terminal. Python3 is recommended.

The functions for testing your knowledge are as follows:

```
    audio_quiz(birds, key='name')
    image_quiz(birds, key='name', figsize=(7,7))
    video_quiz(birds, key='name')
    taxonomy_quiz(birds, key='order')
```

Each function requires a pandas dataframe as an input (*birds*), with an optional parameter called *key*. For the audio, image, and video quizzes, this key can be from ['name', 'order', 'family', 'species'], while for the taxonomy quiz if must be from ['order', 'family', 'species']. The *figsize* parameter allows you to change the image size.

The video links have a limited duration of about ~1 hour. If the links stop working, simply exit the quiz (type "q" and hit return) and call the function again.

Functions that can be used to create dataframes are the following:

```
    get_birds_by_family(*families)
    get_birds_by_group(*groups)
    get_birds_by_order(*orders)
    get_birds_by_name(*names)
```

Each function can take a series of strings referring to birds of the designated type. Thus a few usages are the following

```
    waterfowl = get_birds_by_group('geese', 'swans', 'ducks')
    waterfowl = get_birds_by_order('anseriformes')
    waterfowl = get_birds_by_family('anatidae')
```

If you want to quiz yourself by looking at various images of waterfowl, and increase the figure size, this can be done as follows in a python terminal:

```
    from base import *
    waterfowl = get_birds_by_family('anatidae')
    image_quiz(waterfowl, figsize=(9,9))
```

If you are using an ipython terminal, then ```run base``` can be used in place of ```from base import *```

To run an *audio_quiz* on the birds defined in the dataframe *custom_list*, and require that the answer refer to the *order* of the species, we can do the following

```
    audio_quiz(custom_list, key='order')
```

Similarly, to run a *video_quiz* on the birds that we've seen and test on the family of the bird we can call

```
    video_quiz(class_birds, key='family')
```

To exit a quiz, simply type "q" and press return. The audio can be repeated by entering "r" and pressing return; the same works with the video quiz.

If wanting to go the Cornell website for a particular bird, simply pass the name of the bird as a string into the function *open_browser*. If there is an apostrophe in the name, precede with a backspace.

```
    >> open_brower('bald eagle')
    >> open_browser('ross\'s goose')
```

## Library Dependencies

Some python library dependencies:

```
    BeautifulSoup
    skimage
    pandas
    vimeo_dl
    vlc                  [also need VLC media player]
    webbrowser
```

## Downloading

If git is installed, you can download the content into a directory using
```
    git clone https://github.com/bbergerud/merlin.git
```
If any changes are made to the content on github, you can update your files by running
```
    git pull
```
in the terminal. Otherwise, click the "Clone or download" button at the top.
