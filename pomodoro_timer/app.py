#!/usr/bin/env python3
"""
app.py

Pomodoro Timer
"""
import argparse

from datetime import datetime, timedelta
from os import system
from time import sleep
from sys import platform

from .config import PLAYER, SOUNDS
from .log_init import setup_logging

logger = setup_logging()


class Pomodoro:
    """Pomodoro Timer

    Given the amount of hours you want to spend on your task, it will prompt you to take a 5 minute break every 25
    minutes. At the end it sounds alarm to let you know that the time that you specified is up.
    """

    def __init__(self, duration, breaks=5, interval=25):
        """
        Initializes the timer.

        :param duration: int - specifies how long the timer should run for, in hours.
        :param breaks:  int - specifies how long the breaks should be, in minutes.
        :param interval: int - specifies how long to work before taking a break, in minutes.
        """
        self.second = 1
        self.minute = self.second * 60
        self.hour = self.minute * 60
        self.duration = duration * self.hour
        self.interval = interval * self.minute
        self.break_length = breaks * self.minute
        self.start_time = None
        self.stop_time = None

    def start(self):
        """Starts the timer."""
        self.start_time = datetime.now()
        print(f"duration: {self.duration}")
        self.stop_time = self.start_time + timedelta(seconds=self.duration)
        print(f"Work session ends at: {str(self.stop_time).split('.')[0]}")
        try:
            while datetime.now() < self.stop_time:
                self.start_interval()
                self.start_break()
            print("Nicely done! Go take an extended break.")
            self.play("done")
        except KeyboardInterrupt:
            print("Timer stopped by the user.")

    def start_break(self):
        """Starts the break."""
        start_work = datetime.now() + timedelta(seconds=self.break_length)
        print(f"Start again at: {str(start_work).split('.')[0]}")
        self.play("break")
        sleep(self.break_length)

    def start_interval(self):
        """Starts the interval timer."""
        break_time = datetime.now() + timedelta(seconds=self.interval)
        print(f"Next break: {str(break_time).split('.')[0]}")
        self.play("begin")
        sleep(self.interval)

    @staticmethod
    def play(sound):
        """
        Plays the sound file.

        :param sound: str - the name of the sound file to play
        :return: None
        """
        system(f"{PLAYER} {SOUNDS.get(sound, SOUNDS['warning'])}")


def get_args():
    """Argument parser."""
    parser = argparse.ArgumentParser(description="Pomodoro Productivity Timer")
    parser.add_argument("duration", type=int, help="How long you going to work for, in hours")
    parser.add_argument("-b", "--breaks", type=int, help="How long the breaks should be", required=False)
    parser.add_argument("-i", "--interval", type=int, help="Minutes to work before taking a break", required=False)
    args = parser.parse_args()
    duration = args.duration
    breaks = args.breaks
    interval = args.interval
    return duration, breaks, interval


def main():
    """Main entry point of the application."""
    if platform != "linux":
        print(f"Sorry, your platform {platform} is not supported!")
        exit(1)

    params = get_args()

    duration = params[0]
    breaks = params[1] if params[1] else 5
    interval = params[2] if params[2] else 25

    timer = Pomodoro(duration, breaks=breaks, interval=interval)
    timer.start()


if __name__ == "__main__":
    main()
