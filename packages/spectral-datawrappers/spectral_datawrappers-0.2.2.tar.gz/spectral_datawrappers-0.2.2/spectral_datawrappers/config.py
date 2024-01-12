
import os
from dynaconf import Dynaconf

path = os.path.dirname(os.path.realpath(__file__))
settings = Dynaconf(
    env_switcher='ENV',
    envvar_prefix="DATA_WRAPPERS",
    settings_files=['spectral_datawrappers/config/settings.toml', 'spectral_datawrappers/config/.secrets.toml'],
    environments=True,
    load_dotenv=True,
    includes=[path + '/config/*.toml'],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
