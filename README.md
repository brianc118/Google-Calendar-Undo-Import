Google Calendar Undo Import

Accidently imported an .ics into the wrong calendar? Unfortunately, Google hasn't provided 
a solution to undoing calendar imports. If you've imported the .ics into a primary calendar
you will not be able to fix the issue even by reuploading the same .ics with every entry
labelled as CANCELLED (i.e. STATUS:CANCELLED).

This tool allows you to choose any calendar and remove all entries specified created
at a specified time. Firstly you will be asked to chose a calendar. Then you will be asked
to choose an entry from the calendar that reflects the time. For example, if you chose the
entry "MATH2001" which was created on Jan 1 2015 5:31pm, then all entries in that calendar
created at exactly Jan 1 2015 5:31pm will be deleted.

Getting Started
- To run the script you  must first install the Google Client Library
Follow the steps here https://developers.google.com/google-apps/calendar/quickstart/python
*Remember to download client_secret.json from Google and place it in the same directory as
the script*
