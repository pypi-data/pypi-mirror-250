import logging
import sys
from typing import List, Optional, Union

from apipulse_python.core.model.sdk_options import SdkOptions

from .auto_configuration import ApiPulseAutoConfiguration

options: Optional[SdkOptions] = None
initialized = False
auto_configuration: Optional[ApiPulseAutoConfiguration] = None



def init(
    url: str = "",
    application_name: str = "",
    environment: str = "",
    auth_key: str = None,
    logging_enabled: bool = False,
    log_level: Union[str, int] = logging.FATAL,
    mask_headers: Optional[List[str]] = None,
    capture: str = None,
    # extra 
    partner_id: str = None,
    team_name: str = None,
     
):
    """
    Initialize Apipulse SDK. It automatically samples traffic and syncs with Apipulse servers.


    :param str url: The Apipulse url for your org, provided by Apipulse team.
        Ex: https://example.apipulse.dev

    :param str application_name: Project or Application name. Ex: Demo-Service

    :param str auth_key: Apipulse auth key, provided by Apipulse team.

    :param str environment: Your application environment. Ex: stage, prod, alpha, etc.

    :param bool logging_enabled: Enable Apipulse SDK logging

    :param str log_level: Apipulse SDK logging level. Logging depends on `logging_enabled ` argument.

    :param list(int) mask_headers: Headers names (case in-sensitive) that will be masked at the SDK level itself.
        Masking will happen locally before data is sent to Apipulse servers. Ex: ["cookie", "x-auth"]

    :param str capture: TEST MODE
    """
    global options, initialized, auto_configuration

    # sdk fails in django-admin commands. we only allow sdk to run if runserver django admin command was used
    if len(sys.argv) >= 2 and sys.argv[0].endswith("manage.py") and sys.argv[1] != "runserver":
        return

    if not initialized:
        initialized = True

        opts: SdkOptions = SdkOptions(
            url, application_name, auth_key, environment, logging_enabled, log_level, mask_headers, capture, partner_id, team_name
        )
        opts.sanitize()
        is_options_valid = opts.validate()

        if not is_options_valid:
            return

        options = opts

        auto_configuration = ApiPulseAutoConfiguration(opts=opts)
        auto_configuration.init()

        print("Apipulse Initialized !")
