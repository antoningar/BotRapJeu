import logging

logging.basicConfig(filename='rap_jeu.log', format='%(asctime)s %(message)s', level=logging.WARNING)

def log_command(command, user):
    logging.warning('[COMMAND] %s BY %s (%s)' % (command, user.display_name, user.id))

def log_request(url, website, purpose):
    logging.warning('[%s] REQUEST FOR %s URL : %s' % (website, purpose, url))

def log_error(module, error):
    logging.warning('[%s] ERROR : %s' % (module, error))

def log_reaction_added(msg, user):
    logging.warning('[REACTION] ADDED ON MSG %s BY %s (%s)' % (msg, user.display_name, user.id))

def log_reaction_delete(msg, user):
    logging.warning('[REACTION] DELETED ON MSG %s BY %s (%s)' % (msg, user.display_name, user.id))