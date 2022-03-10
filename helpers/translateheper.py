import settings
if settings.TRANSLATE_LANG == 'FR':
    import translate.fr as translate

def get_cards(key, val=None):
    return translate.cards[key] if val is None else translate.cards[key] % val

def get_roland(key, val=None):
    return translate.roland[key] if val is None else translate.roland[key] % val

def get_guidelines(key, val=None):
    return translate.guidelines[key] if val is None else translate.guidelines[key] % val

def get_team(key, val=None):
    return translate.team[key] if val is None else translate.team[key] % val

def get_lead(username, score):
    return translate.lead['score'] % (username, score)

def get_lead_intro():
    return translate.lead['intro_leaderboard']

def get_lead_user(position, username, score):
    return translate.lead['user_leaderboard'] % (position, username, score)

def get_test(key, points=None):
    return translate.test[key] if points is None else translate.test[key] % points