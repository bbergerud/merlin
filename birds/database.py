import pandas as pd
import requests
import os
from .html import *

def get_csv_name():
    dir = os.path.dirname(__file__)
    return os.path.join(dir, 'resources', 'database.csv')

def load_csv():
    csv = pd.read_csv(get_csv_name(), index_col=0)
    return csv.sort_index()

def save_csv(dataframe, index=True):
    dataframe.to_csv(get_csv_name(), index=index)

def retrieve_bird_catalog(clean_copy=False):
    """
    Scrapes the www.allaboutbirds.org website to identify
    all the birds on it, as well as their info.

    Parameters
        clean_copy      [boolean]
                        If False, attempt to load a previously saved CSV file.
                        Otherwise, begin with a blank data frame.

    Postcondition:
        The birds names, along with certain attributes, are stored in
        the csv file "database.csv" located in the "resources" directory.
    """

    # =============================================
    # Homepage for allaboutbirds
    # =============================================
    home = 'https://www.allaboutbirds.org'

    # =============================================
    # If the csv file already exists, load it.
    # If not, create a data frame to store info
    # =============================================
    try:
        if clean_copy: raise
        csv = load_csv(savefile)
    except:
        csv = pd.DataFrame(columns = [
            'name', 'group', 'order', 'family', 'species'
        ])

    # =============================================
    # Get the links on the taxonomy page
    # =============================================
    page = get_page(home + '/guide/browse/taxonomy')
    soup = get_soup(page)

    # =============================================
    # Find the links for each of the bird families
    # =============================================
    links = soup.findAll('div', class_='group-list')[0].findAll('a')
    links = [link['href'] for link in links]

    # =============================================
    # Open each link and gather the birds on page
    # Since the html text is dynamical, use request
    # =============================================
    for link in links:
        html = get_page(home + link)
        soup = get_soup(html)

        # =========================================
        # Grab the bird elements
        # =========================================
        bird_tags = soup.findAll('div', class_='family-list')[0].findAll('h3')
        for bird_tag in bird_tags:

            tag = get_soup('{}'.format(bird_tag))

            # =====================================
            # Extract the bird name
            # =====================================
            bird_name = tag.string.lower()
            print(bird_name)

            # =====================================
            # Check if the bird name is already there
            # If so, proceed to next one
            # =====================================
            if bird_name in csv['name'].values:
                continue

            # =====================================
            # Extract the url address and get the
            # page content
            # =====================================
            url  = home + tag.findAll('a')[0]['href']
            page = get_page(url)
            soup = get_soup(page)

            # =====================================
            # Extract the callout section
            # =====================================
            callout = soup.findAll('div', class_='callout')[0]

            # =====================================
            # Get the bird category
            # =====================================
            group = callout.find('div', class_='silo-group').findAll('span')[0]
            group = group.text.lower()

            # =====================================
            # Extract the order and family
            # =====================================
            info   = callout.find('ul', class_='additional-info').findAll('li')
            order  = info[0].text.split(':')[-1].strip().lower()
            family = info[1].text.split(':')[-1].strip().lower()

            # =====================================
            # Extract the species info
            # =====================================
            species = callout.find('div', class_='species-info').findAll('i')[0]
            species = species.text.lower()

            data = {
                'name'   : bird_name,
                'group'  : group,
                'order'  : order,
                'family' : family,
                'species': species
            }

            csv = csv.append(data, ignore_index=True)

        save_csv(csv, index=False)

def get_birds_by_group(*groups):
    csv = load_csv()

    df = pd.DataFrame()
    for group in groups:
        group = group.lower()
        try:
            birds = csv[csv.group == group]
            if birds.empty:
                raise
            df = df.append(birds)
        except:
            print('The group {:s} not in csv file'.format(group))
            continue
    return df.sort_index()

def get_birds_by_order(*orders):
    csv = load_csv()

    df = pd.DataFrame()
    for order in orders:
        order = order.lower()
        try:
            birds = csv[csv.order == order]
            if birds.empty:
                raise
            df = df.append(birds)
        except:
            print('The order {:s} not in csv file'.format(order))
            continue
    return df.sort_index()

def get_birds_by_family(*families):
    csv = load_csv()

    df = pd.DataFrame()
    for family in families:
        family = family.lower()
        try:
            birds = csv[csv.family == family]
            if birds.empty:
                raise
            df = df.append(birds)
        except:
            print('The family {:s} not in csv file'.format(family))
            continue
    return df.sort_index()


def get_birds_by_names(*names):
    csv = load_csv()

    df = pd.DataFrame()
    for name in names:

        # ======================================
        # Convert to lowercase
        # ======================================
        name = name.lower()

        # ======================================
        # Verify bird is in data frame and add
        # to the data frame
        # ======================================
        try:
            csv.loc[name]
            df = df.append(csv.loc[name])
        except:
            print('Bird name {:s} not in csv file'.format(name))
            continue

    return df.sort_index()
