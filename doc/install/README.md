# Installation

## Important notes

This installation guide was created for and tested on **Debian/Ubuntu** operating systems.

This is the official installation guide to set up a production server.

The following steps have been known to work. Please **use caution when you something differently** from this guide. Make sure you don't violate any assumptions ICA makes about its environment.

## Overview

The ICA installation consists of setting up the following steps:

1. Packages / Dependencies
1. Virtual environ
1. Database
1. ICA
1. Webserver

## 1. Packages / Dependencies

`sudo` is not installed on Debian by default. Make sure your system isup-to-date and install it.

	# run as root
	aptitude update -y
	aptitude upgrade -y
	aptitude install sudo -y

**Note:** During this installation some files will need to be edited manually. If you are familiar with vim set it as default editor with the commands below. If you are not familiar with vim please skip this and keep using the default editor.

	# Install vim and set as default editor
	sudo aptitude install -y vim
	sudo update-alternatives --set editor /usr/bin/vim.basic

Install the required packages:

	sudo aptitude install python-pip python-virtualenv python-dev python-docutils build-essential curl openssh-server checkinstall logrotate make gcc git-core

## 2. Virtual environ

Create a Python virtual environment (virtualenv) to install ICA into, and activate it.
You can ignore this step.

	cd /home/
	# Prepare virtual environment to get a cleaning installation
	virtualenv env
	# Go into new virtual environment
	source env/bin/activate

## 3. Database

We recommend using a PostgreSQL database for production, plase see [postgresql.md].
Remember you can install any of the popular relational database that are in the market like: `MySQL`, `Oracle`,
`Microsoft SQL Server`, `SQLite` and others, plase see [others_rdbms.md] .

## 4. ICA

### Installation

	# We'll install into home directory
	cd /home/git

	# Clone repository
	sudo git clone https://github.com/dreiver/ica.git

	# Go to ica dir
	cd /home/ica

	# Install dependeces
	pip install -r requirements.txt