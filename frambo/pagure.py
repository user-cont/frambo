from frambo.config import get_from_frambo_config

PAGURE_HOST = get_from_frambo_config("pagure", "host")
PAGURE_PORT = get_from_frambo_config("pagure", "port", raises=False)

PAGURE_URL = f"https://{PAGURE_HOST}/"


def cfg_url(repo, branch, file="bot-cfg.yml"):
    return f"{PAGURE_URL}{repo}/raw/{branch}/f/{file}"
