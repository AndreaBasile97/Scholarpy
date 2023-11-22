# Scholarpy
Author: Andrea Basile
A wrapper for Semantic Scholar APIs. This tool was made to make easier scholar reasearch.

## Guide

### Snowballing

Snowballing is a technique that consists in getting all the references from a specific paper (backward) or
all the citations of that very same paper.

Thanks to Scholarpy you can do it easly having a csv file as result containing all the main informations about the references 
such as:

- title
- bibTex
- DOI
- link
- year
- Authors

Quick start:

1. using

        python gui.py

2. using args

        python -m snowballer [add args here that you can find in snowballer.py file]