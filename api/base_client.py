import time
import requests

REQUEST_TIMEOUT = 30
SENSITIVE_KEYS = {"password", "session"}


def _masked(payload):
    if not payload:
        return payload
    return {k: ("***" if k in SENSITIVE_KEYS else v) for k, v in payload.items()}


def post_and_log(logger, url, *, data=None, headers=None, files=None):
    """Выполняет POST-запрос с таймаутом и логирует запрос/ответ (пароль/сессия маскируются)."""
    action = (data or {}).get("action") or (data or {}).get("method") or (data or {}).get("request")
    logger.info(f"API POST {url} | action={action} | payload={_masked(data)}")

    start = time.monotonic()
    response = requests.post(url, data=data, headers=headers, files=files, timeout=REQUEST_TIMEOUT)
    elapsed = time.monotonic() - start

    logger.info(f"API ответ {response.status_code} за {elapsed:.2f}s")
    if not response.ok:
        logger.error(f"API ошибка {response.status_code} для {url}: {response.text[:2000]}")

    return response
