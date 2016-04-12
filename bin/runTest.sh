#!/bin/bash
#
#
unbuffer /usr/local/bin/python /home/ciPolicy/sylvia/sylvia.py 1>/var/log/sylviaTest.log 2>&1 
