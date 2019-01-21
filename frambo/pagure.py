from os import getenv

DEPLOYMENT = getenv('DEPLOYMENT')

if not DEPLOYMENT:
    raise AttributeError("Please provide environment as DEPLOYMENT variable."
                         "One of ['stage', 'prod', 'dev', 'test']")
if DEPLOYMENT == 'prod':
    PAGURE_HOST = 'pagure.io'
elif DEPLOYMENT in ('stage', 'dev', 'test'):
    PAGURE_HOST = 'stg.pagure.io'
else:
    raise AttributeError(f"Unsupported environment {DEPLOYMENT}")

# Fedora Pagure.io does not need port for clonning.
PAGURE_PORT = ''
PAGURE_URL = f'https://{PAGURE_HOST}'


def cfg_url(repo, branch, file='bot-cfg.yml'):
    return f"{PAGURE_URL}{repo}/raw/{branch}/f/{file}"
