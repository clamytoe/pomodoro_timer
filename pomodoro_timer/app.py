#!/usr/bin/env python3
"""
app.py

Pomodoro Timer
"""
import argparse
from collections import namedtuple
from datetime import datetime, timedelta
from os import system
from sys import platform
from time import sleep

from .config import PLAYER, SOUNDS
from .log_init import setup_logging

logger = setup_logging()
Params = namedtuple("Params", "duration breaks interval")


class Pomodoro:
    """Pomodoro Timer

    Given the amount of hours you want to spend on your task, it will prompt you to take a 5 minute break every 25
    minutes. At the end it sounds alarm to let you know that the time that you specified is up.
    """
    MODES = "idle active break".upper().split()

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
        self.break_time = None
        self.work_time = None
        self.status = self.MODES[0]
        self.rounds = 0

    def get_input(self):
        key = input("Hit any key to continue, [q]uit: ")
        if key.lower() == "q":
            self.bye_message()

    def start(self):
        """Starts the timer."""
        self.start_time = datetime.now()
        self.stop_time = self.start_time + timedelta(seconds=self.duration)
        print(f"Work session ends at: {str(self.stop_time).split('.')[0]}")
        self.start_timer()

    def start_break(self):
        """Starts the break."""
        self.break_time = None
        self.work_time = datetime.now() + timedelta(seconds=self.break_length)
        print(f"Start again at: {str(self.work_time).split('.')[0]}")
        self.status = self.MODES[2]
        self.play("break")

    def start_interval(self):
        """Starts the interval timer."""
        self.work_time = None
        self.break_time = datetime.now() + timedelta(seconds=self.interval)
        print(f"Next break: {str(self.break_time).split('.')[0]}")
        self.status = self.MODES[1]
        self.rounds += 1
        self.play("begin")

    def start_timer(self):
        try:
            while datetime.now() < self.stop_time:
                if self.rounds == 4:
                    print("Nicely done! Go take an extended break.")
                    self.play("done")
                    self.bye_message()
                else:
                    self.start_interval()
                    self.pause(self.interval)
                    self.get_input()
                    self.start_break()
                    self.pause(self.break_length)
                    self.get_input()
            print("Nicely done! You're all done!.")
            self.play("done")
            self.bye_message()
        except KeyboardInterrupt:
            print("Timer stopped by the user.")

    @staticmethod
    def bye_message():
        print("Thanks for using clamytoe's Pomodoro Timer!")
        exit()

    @staticmethod
    def play(sound):
        """
        Plays the sound file.

        :param sound: str - the path and name of the sound file to play
        :return: None
        """
        system(f"{PLAYER} {SOUNDS.get(sound, SOUNDS['warning'])}")

    @staticmethod
    def pause(length):
        sleep(length)


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
    params = Params(duration=duration, breaks=breaks, interval=interval)
    return params


def main():
    """Main entry point of the application."""
    if platform != "linux":
        print(f"Sorry, your platform {platform} is not supported!")
        exit(1)

    params = get_args()

    duration = params.duration
    breaks = params.breaks if params.breaks else 5
    interval = params.interval if params.interval else 25

    timer = Pomodoro(duration, breaks=breaks, interval=interval)
    timer.start()


if __name__ == "__main__":
    main()
