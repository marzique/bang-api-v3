ROLES = {
    4: ['SH', 'RE', 'OL', 'OL'],
    5: ['SH', 'RE', 'OL', 'OL', 'DE'],
    6: ['SH', 'RE', 'OL', 'OL', 'OL', 'DE'],
    7: ['SH', 'RE', 'OL', 'OL', 'OL', 'DE', 'DE']     
}

actions = {
    'panic': {
        'description': 'Draw a card from a player at distance 1. This distance is not modified by weapons, but by cards such as Mustang and/or Scope.',
        'max': 4,
        'action': 'PL',
    },
    'generalstore': {
        'description': 'When played, as many cards as there are players still playing are turned face down on the table. Starting with the player that played it, proceeding clockwise, each player chooses one of the cards and adds it to their hand',
        'max': 2,
        'action': 'AL',
    },
    'missed': {
        'description': 'May be played immediately to cancel the effect of a BANG card, or any card with a BANG symbol.',
        'max': 12,
        'action': 'SE',
    },
    'wellsfargo': {
        'description': 'Draw 3 cards from the deck at time of play.',
        'max': 1,
        'action': 'SE',
    },
    'stagecoach': {
        'description': 'Draw 2 cards from the deck at time of play.',
        'max': 2,
        'action': 'SE',
    },
    'bang': {
        'description': 'Deal a BANG to target player. Target must play a MISS, otherwise the target loses one life point. Each player can only play one BANG per turn.',
        'max': 25,
        'action': 'PL',
    },
    'saloon': {
        'description': 'One life point to every player.',
        'max': 1,
        'action': 'AL',
    },
    'beer': {
        'description': 'Discard this and gain one life point.',
        'max': 6,
        'action': 'SE',
    },
    'duel': {
        'description': 'Target player must discard a BANG card, then you, etc. First player failing to discard a BANG card loses one life point. A MISS or KEG card is not accepted. This card does not use your turns BANG.',
        'max': 3,
        'action': 'PL',
    },
    'indians': {
        'description': 'All other players discard a BANG card or lose one life point. A MISS or BARREL card is not accepted.',
        'max': 2,
        'action': 'AL',
    },
    'cat': {
        'description': 'Force a player to discard a card. This card can be random from their hand, or a card they have on the table in play.',
        'max': 4,
        'action': 'PL',
    },
    'gatling': {
        'description': 'Deals a BANG card to every other player regardless of distance. This card does not use your turns BANG.',
        'max': 1,
        'action': 'AL',
    }
}

effects = {
    'mustang': {
        'description': 'When you have the mustang in play, the distance at which other players see you is increased by one. However you still see the other players at normal distance.',
        'max': 2,
        'action': 'SE',
        'checkable': False
    },
    'scope': {
        'description': 'When you have the scope in play, you see all other players at a distance decreased by one. However, other players still see you at the normal distance. ',
        'max': 1,
        'action': 'SE',
        'checkable': False
    },
    'dynamite': {
        'description': 'Before you play your turn, draw a card for the dynamite. If the card is a spades, you lose three life points, otherwise pass the dynamite to your left. The dynamite stays in play rotating around the table until it explodes on a player. Player putting the card down puts it on themself first, and draws for it on their next turn.',
        'max': 1,
        'action': 'SE',
        'checkable': True
    },
    'jail': {
        'description': 'Either draw a card and get a heart to discard the jail, or skip your turn and discard the jail. If you draw a card, and do not get a heart, the jail is still in play, and you must choose again on your next turn. If in hand, play on a player to put them in jail.',
        'max': 3,
        'action': 'PL',
        'checkable': True
    },
    'barrel': {
        'description': 'Draw a heart and it acts as a MISS card played. Keg stays in play after.',
        'max': 2,
        'action': 'SE',
        'checkable': True
    }
}

guns = {
    'remington': {
        'description': 'Shoot at distance 3.',
        'max': 1,
        'action': 'SE',
        'distance': 3,
        'unlimited': False
    },
    'rev.carabine': {
        'description': 'Shoot at distance 4.',
        'max': 1,
        'action': 'SE',
        'distance': 4,
        'unlimited': False
    },
    'schofield': {
        'description': 'Shoot at distance 2.',
        'max': 3,
        'action': 'SE',
        'distance': 2,
        'unlimited': False
    },
    'winchester': {
        'description': 'Shoot at distance 5.',
        'max': 1,
        'action': 'SE',
        'distance': 5,
        'unlimited': False
    },
    'volcanic': {
        'description': 'Shoot at distance 1 unlimited amount of times.',
        'max': 2,
        'action': 'SE',
        'distance': 1,
        'unlimited': True
    }
}

characters = {
    'vulture': {
        'description': 'Whenever a player is eliminated from play, he takes in hand all the cards of that player.',
        'health': 4,
        'fullName': 'full name...'
    },
    'suzy': {
        'description': 'As soon as she has no cards in hand, she draws a card.',
        'health': 4,
    }
}