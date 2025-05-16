
# BookReader

## components

### Base-Logic

- epub-parser
- word instance extractor
- api handler

### backend

- routes for uploading
- routes for getting book
- routes to get meaning of word

### frontend

- epub parser
- epub prettifier using dom manupilation of epub(html)

## Current-to-do

- take chapter,sentence,"selection",type
    1. if type is `lookup`
      - divide the book by sentence
      - find all sentence with the given word on both section
      - query api with word and 1st sect(non spoiler) 2nd sect(spoiler)
      - return the response
    2. if type is `explanation`
      - send the selection with context
      - format it well
      - return it
