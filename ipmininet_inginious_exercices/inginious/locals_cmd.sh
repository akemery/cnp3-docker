#!/bin/bash
xgettext -d base -o locales/base.pot grader.py
cd locales/fr/LC_MESSAGES
msgfmt -o base.mo base
