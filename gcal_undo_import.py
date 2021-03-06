#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Brian Chen
#
# Open sourced under the MIT License
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys

from oauth2client import client
from googleapiclient import sample_tools


def getUserInputIndex(msg, i):
    while True:
        print(msg)
        x = input()
        if x.isdigit():
            if int(x) < i:
                break
            else:
                print('Must be less than {0}'.format(i))
        else:
            print('Type a positive integer')
    return x

def main(argv):
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)# Authenticate and construct service.
    service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar')

    try:
        page_token = None
        i = 0
        calendars = []
        events = []

        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            calendars.extend(calendar_list['items'])
            print("Loading calendars")
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

        calendars = [c for c in calendars if c['kind'] == 'calendar#calendarListEntry']

        for calendar in calendars:
            print('{0}\t{1}'.format(i, calendar['summary']))
            i += 1

        x = getUserInputIndex('\nSelect calendar by typing in the index', i)
        calendar_id = calendars[int(x)].get('id')
        print("Selected '{0}'".format(calendars[int(x)].get('summary')))
        i = 0

        while True:
            ev = service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
            events.extend(ev['items'])
            page_token = ev.get('nextPageToken')
            print("Loading entries")
            if not page_token:
                break
        
        events = [e for e in events if e['kind'] == 'calendar#event']
        for event in events:
            print(u"{0}\t{1}\t{2}".format(i, (event.get('start', {}).get('date') if event.get('start', {}).get('date') != None else event.get('start', {}).get('dateTime')), event.get('summary')))
            i += 1

        x = getUserInputIndex('\nSelect event by typing in the index', i)
        creation_date = events[int(x)].get('created')
        i = 0

        for event in events:
            if event.get('created') == creation_date:
                print(u"{0}\tDeleting {1}\t{2}".format(i, event.get('summary'), event.get('id')))
                service.events().delete(calendarId=calendar_id, eventId=event.get('id')).execute()
                i += 1

        print('Deleted {0} entries'.format(i))

    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')

if __name__ == '__main__':
    main(sys.argv)

