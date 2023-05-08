import sentry_sdk


def test_sentry(sentry_mock):
    assert len(sentry_mock.method_calls) == 0
    sentry_sdk.capture_exception(Exception("test_sentry_exc"))
    assert len(sentry_mock.method_calls) == 1
    sentry_mock.record_lost_event.assert_not_called()
    assert (
        sentry_mock.method_calls[0]
        .args[0]
        .items[0]
        .get_event()["exception"]["values"][0]["value"]
        == "test_sentry_exc"
    )
