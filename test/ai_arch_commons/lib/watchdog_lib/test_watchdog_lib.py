from unittest.mock import MagicMock

from ai_arch_commons.lib.watchdog_lib.watchdog_class import WatchDogClass


def test_watchdog_lib():
    WatchDogClass.setup_scheduler = MagicMock()
    watchdog_class = WatchDogClass()

    config = {
        'delay_time_seconds': 0,
        'batch_size': 0,
        'batch_sleep_time_seconds': 0
    }

    watchdog_class.setup_service(config=config, watchdog_handler=None)
    WatchDogClass.setup_scheduler.assert_called_once()


def test_watchdog_run_job():
    WatchDogClass.watchdog_hanlder_run = MagicMock()
    WatchDogClass.set_watchdog_scheduler = MagicMock()

    watchdog_class = WatchDogClass()
    watchdog_class.run_job()

    WatchDogClass.watchdog_hanlder_run.assert_called_once()
    WatchDogClass.set_watchdog_scheduler.assert_called_once()
