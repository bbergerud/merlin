import random

def taxonomy_quiz(birds, key='order'):
    print('''
    This quiz tests your knowledge of bird orders, family,
    and species name.

    To exit the quiz, enter 'Q' for the input and press return.
    ''')

    # =============================================
    # Use lowercase for the key
    # =============================================
    key = key.lower()
    if key not in birds.columns:
        print('not a valid key: {:s}'.format(key))
        return

    # =============================================
    # Begin the quiz
    # =============================================
    while True:

        # =============================================
        # Randomly sample a bird name
        # =============================================
        bird = random.choice(birds.index)

        # =============================================
        # Get the user's guess
        # =============================================
        guess = input('Bird Name = {:s}, {:s} = '.format(
            bird.title(), key.capitalize()
        )).lower()

        # =============================================
        # In the input is "q", then quit the quiz
        # Otherwise, check if the user was right
        # =============================================
        answer = birds.loc[bird, key]

        if guess == 'q':
            break
        elif guess == answer:
            print('Correct!\n')
        else:
            print('Incorrect. The {:s} is {:s}\n'.format(
                key, answer)
            )
