# Overview

...TODO...


# One-time Setup

Clone the repo in some personal location, preferably on network storage, e.g. somewhere in your home directory:

	$ git clone git@github.com:/fasrc/fasrcsw.git ~/fasrcsw

Give all shells an environment variable named `FASRCSW` which points to this location, e.g. with something like the following:

	$ echo 'export FASRCSW=$HOME/fasrcsw' >> ~/.bashrc

Source ~/.bashrc if you'll continue to work in the same shell.
This variable is only used to make the instructions below portable; it's not part of the fasrcsw framework per se.


# Workflow

## Prep

* make sure you're logged into the build host
* make sure you're logged into your normal user account, *not* root
