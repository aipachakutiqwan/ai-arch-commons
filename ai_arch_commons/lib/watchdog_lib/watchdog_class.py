import logging
import sched
import time


class WatchDogClass:
    def __init__(self):
        self.delay_time_seconds = None
        self.watchdog_schedular = None
        self.watchdog_handler = None
        self.batch_size = None
        self.batch_sleep_time = None

    def setup_service(self, config, watchdog_handler):

        self.delay_time_seconds = config['delay_time_seconds']
        self.batch_size = config['batch_size']
        self.batch_sleep_time = config['batch_sleep_time_seconds']

        self.watchdog_schedular = self.setup_scheduler()
        self.watchdog_handler = watchdog_handler

    def setup_scheduler(self):
        return sched.scheduler(time.time, time.sleep)

    def run_service(self):
        self.schedule_job()

    def run_job(self, message='default'):
        """
        Run the scheduled job
        Args:
            :param message: message received
        Returns:
            response:
        """
        try:
            logging.info(message)
            self.watchdog_hanlder_run(message)
        except Exception as e:
            logging.error(f"GENERIC_EXCEPTION_POLLER: error={e}")

        self.set_watchdog_scheduler()

    def watchdog_hanlder_run(self, message):
        self.watchdog_handler.run(message)

    def set_watchdog_scheduler(self):
        self.watchdog_schedular.enter(self.delay_time_seconds, 1,
                                      self.run_job,
                                      argument=('processing scheduled job',))

    def schedule_job(self):
        """
        Schedule the job
        Args:
            :param
        Returns:
            response:
        """
        self.set_watchdog_scheduler()
        self.watchdog_run()

    def watchdog_run(self):
        self.watchdog_schedular.run()
