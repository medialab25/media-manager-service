# Merge Folders

## Objectives
- Inputs: One or more folders named as name-{quality}, each containing a set of data folders
- config.json has a quality_list
- Output: folder with hard links merging input folders. Only merge if a quality is better.
- In output data folder creates a .quality file to allow the quality check to take place.
- Compare quality based on postfix and use the list in config.json where lower is better.

