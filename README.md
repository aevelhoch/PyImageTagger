## Minimal image-tagging software for use with reference pictures

Attempt at making an image tagging and displaying database for use with reference pictures for drawing.

Attempts to solve the problem of organizing images by folder when there are multiple relevant categories.
For example, instead of having a hierarchy of repetitive folders:
```
USER/Reference/Buildings/60s/American/Homes
USER/Reference/Buildings/60s/American/Factories
USER/Reference/Buildings/60s/American/Stores
USER/Reference/Buildings/60s/European/Homes
USER/Reference/Buildings/60s/European/Factories
USER/Reference/Buildings/60s/European/Stores
USER/Reference/Buildings/70s/American/Homes
USER/Reference/Buildings/70s/American/Factories
...
```
A user could instead convert each folder into a tag, apply the tag to each image, and retrieve images with any given tag or combination of tags to view.
The tags are stored entirely in a database, so the image files are not altered in any way.

## Current State

Small REPL models of database functions to be integrated into final product

## Todo

Finish all necessary database functions
Integrate all database functions to final REPL
Create GUI for software and integrate with existing functions