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
    MODES = "idle active respite".upper().split()

    def __init__(self, duration, breaks=5, interval=25):
        """Initializes the timer.

        :param duration: int - specifies how long the timer should run for, in hours.
        :param breaks:  int - specifies how long the breaks should be, in minutes.
        :param interval: int - specifies how long to work before taking a break, in minutes.
        """
        self.second = 1
        self.minute = self.second * 60
        self.hour = self.minute * 60
        self.duration = duration
        self.breaks = breaks
        self.interval = interval
        self.p_duration = self.duration * self.hour
        self.p_interval = self.interval * self.minute
        self.p_breaks = self.breaks * self.minute
        self.session_start = datetime.now()
        self.status = self.MODES[0]
        self.stop_time = None
        self.rounds = 0

    def __repr__(self):
        """Representation of the object."""
        class_name = str(self.__class__).split(".")[-1].replace(">", "").replace("'", "")
        return f"{class_name}(duration:{self.duration} breaks={self.breaks} interval={self.interval})"

    def bye_message(self):
        """Exit message."""
        logger.info(f"{self.status}, session: end")
        print("Thanks for using clamytoe's Pomodoro Timer!")
        exit()

    def get_input(self):
        """Used to continue the program or quit it."""
        self.play("warning")
        key = input("Hit any key to continue, [q]uit: ")
        try:
            if key.lower() == "q":
                self.bye_message()
        except AttributeError:
            pass

        self.play("break") if self.status == "ACTIVE" else self.play("begin")

    def pause(self, length):
        """Pauses the program execution for the desired length of time."""
        sleep(length)
        print("Time for a break!") if self.status == "ACTIVE" else print("Time to get back to work!")
        self.get_input()

    def start(self):
        """Starts the timer."""
        start_time = datetime.now()
        self.stop_time = start_time + timedelta(seconds=self.p_duration)
        logger.info(f"{self.status}, session: start, projected: {self.stop_time}")
        print(f"Session ends at: {str(self.stop_time).split('.')[0]}")
        self.start_timer()

    def start_break(self):
        """Starts the break."""
        work_time = datetime.now() + timedelta(seconds=self.p_breaks)
        print(f"Start again at: {str(work_time).split('.')[0]}")
        self.status = self.MODES[2]
        logger.info(f"{self.status}, break_until: {work_time}")

    def start_interval(self):
        """Starts the interval timer."""
        break_time = datetime.now() + timedelta(seconds=self.p_interval)
        print(f"Next break at: {str(break_time).split('.')[0]}")
        self.rounds += 1
        if self.status == "IDLE":
            self.play("begin")
        self.status = self.MODES[1]
        logger.info(f"{self.status}, interval: {self.rounds}")

    def start_timer(self):
        """Initiates the timing cycle."""
        try:
            while datetime.now() < self.stop_time:
                if self.rounds == 4:
                    print("Nicely done! Go chillax for a bit.")
                    self.play("done")
                    self.rounds = 0
                    self.status = self.MODES[0]
                    logger.info(f"{self.status}, intervals: completed")
                    self.get_input()
                else:
                    self.start_interval()
                    self.pause(self.p_interval)
                    self.start_break()
                    self.pause(self.p_breaks)
            print("Nicely done! You're all done!.")
            self.play("done")
            self.bye_message()
        except KeyboardInterrupt:
            logger.info("User terminated session.")
            print("Timer stopped by the user.")

    @staticmethod
    def play(sound):
        """Plays the sound file.

        :param sound: str - the path and name of the sound file to play
        :return: None
        """
        logger.info(f"sound: {PLAYER} {SOUNDS[sound]}")
        system(f"{PLAYER} {SOUNDS.get(sound, SOUNDS['warning'])}")


def get_args():
    """Argument parser."""
    parser = argparse.ArgumentParser(description="Pomodoro Productivity Timer")
    parser.add_argument("-d", "--duration", type=int, help="How long you going to work for, in hours", required=False)
    parser.add_argument("-b", "--breaks", type=int, help="How long the breaks should be", required=False)
    parser.add_argument("-i", "--interval", type=int, help="Minutes to work before taking a break", required=False)
    args = parser.parse_args()
    duration = args.duration
    breaks = args.breaks
    interval = args.interval
    params = Params(duration=duration, breaks=breaks, interval=interval)
    logger.info(f"Parsed parameters: {params}")
    return params


def main():
    """Main entry point of the application."""
    if platform != "linux":
        logger.warning(f"Attempted to run on unsupported {platform} platform.")
        print(f"Sorry, your platform {platform} is not supported!")
        exit(1)

    params = get_args()

    duration = params.duration if params.duration else 2
    breaks = params.breaks if params.breaks else 5
    interval = params.interval if params.interval else 25

    timer = Pomodoro(duration, breaks=breaks, interval=interval)
    logger.info(f"Initialize Session: {repr(timer)}")
    timer.start()


if __name__ == "__main__":
    main()
