# proj2-flask

_Kory Schneider_

_CIS 322, Fall 2016_

## What is this?
This is a simple Flask server that displays a term schedule.

## Installation
Clone the repository:

    $ cd where/you/want/it
    $ git clone https://github.com/koryschneider/proj2-flask
    $ cd proj2-flask

Then set it up and run it:

    $ bash ./configure && make service

## Usage
`$ make run` will launch the debugging server built into Flask.  It
provides the best support for tracking down bugs, but is not suitable
for high traffic or running the server over a long period of time.

`$ make service` starts a Green Unicorn (gunicorn) server. Green Unicorn
is more suitable for servers that will run for a long period of time.

## Credit
Forked from Michal Young at https://github.com/UO-CIS-322/proj2-flask for
CIS 322: Intro to Software Engineering.
