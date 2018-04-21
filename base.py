from birds.database import get_birds_by_group, get_birds_by_name, load_csv
from birds.database import get_birds_by_order, get_birds_by_family
from birds.html     import open_browser
from birds.audio    import audio_quiz
from birds.image    import image_quiz
from birds.video    import video_quiz
from birds.taxonomy import taxonomy_quiz

# =====================================
# Issue with VLC Media Player (?Linux?)
# =====================================
import ctypes
try:
    x11 = ctypes.cdll.LoadLibrary('libX11.so')
    x11.XInitThreads()
except:
    print("Warning: failed to XInitThreads()")

# =====================================
# Some examples of creating bird lists
# =====================================
birds     = load_csv()
waterfowl = get_birds_by_family('anatidae')
raptors   = get_birds_by_group(
    'accipiters',
    'eagles',
    'falcons',
    'harriers',
    'hawks',
    'osprey',
    'owls',
    'vultures'
)

# =====================================
# A custom list along with the birds
# that have been seen in class.
# =====================================
custom_list = [
    'american robin',
    'blue jay',
    'european starling',
    'northern flicker',
    'song sparrow',
]

class_birds = [
    'american coot',
    'american crow',
    'american robin',
    'american white pelican',
    'american woodcock',
    'bald eagle',
    'barn swallow',
    'blue jay',
    'blue-winged teal',
    'bufflehead',
    'canada goose',
    'canvasback',
    'common loon',
    'cooper\'s hawk',
    'dark-eyed junco',
    'double-crested cormorant',
    'eastern phoebe',
    'european starling',
    'gadwall',
    'great blue heron',
    'greater prairie-chicken',
    'greater white-fronted goose',
    'green-winged teal',
    'killdeer',
    'lesser scaup',
    'mallard',
    'mourning dove',
    'northern cardinal',
    'northern flicker',
    'northern harrier',
    'northern shoveler',
    'pectoral sandpiper',
    'pied-billed grebe',
    'red-tailed hawk',
    'red-winged blackbird',
    'ring-billed gull',
    'ring-necked duck',
    'rock pigeon',
    'ruddy duck',
    'sandhill crane',
    'song sparrow',
    'tree swallow',
    'trumpeter swan',
    'turkey vulture',
]

custom_list = get_birds_by_name(*custom_list)
class_birds = get_birds_by_name(*class_birds)
