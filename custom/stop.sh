#!/bin/sh

ps -ef | grep "gaze_glass" | grep -v grep | awk '{print $2}' | xargs kill -15