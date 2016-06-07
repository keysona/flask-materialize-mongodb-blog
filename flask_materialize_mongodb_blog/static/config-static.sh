#!/bin/bash

# materialize
sass --style compressed lib/materialize-src/sass/materialize.scss static/css/materialize.min.css

# my css
sass --style compressed lib/keysona/keysona.scss static/css/keysona.min.css
