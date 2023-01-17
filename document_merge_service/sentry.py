import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration


def sentry_init(dsn, env, traces_sample_rate, send_default_pii):
    sentry_sdk.init(
        dsn=dsn,
        environment=env,
        send_default_pii=send_default_pii,
        traces_sample_rate=traces_sample_rate,
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
            # the `level` kwarg defaults to INFO and instructs sentry to include log messages of that level or higher in
            # the message sent to sentry when triggered by an event of level specified in event_level kwarg as
            # breadcrumbs.
        ],
    )
