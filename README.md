# YouCrawler - Tags Edition

Hi! This is YouCrawler, my first real Python project for release under open source licenses.

This command line tool allows you to scrape YouTube of "hidden" tags (they are availble via the [YouTube API](https://developers.google.com/youtube/v3)). This application takes various inputs based on your selected method of counting, finds all video links in the "recommended videos" section and adds them to a list for futher iterations. Following scanning the page of URL's the script will then pull the tags for every video in the list and save them.

***Some "cool" tidbits of info***

 - YouCrawler remembers URL's that it visits so as to not create duplicate tags or URL's or wasted bandwidth
 - Data is exported to JSON at the end of iterations
 - Previously exported iterations can be easily imported


## Inspiration?

Scanning Reddit recently I stumbled upon [this post](https://www.reddit.com/search/?q=YouTube%20tags) , I credit my initial inspiration and utilizing [ishanfx's](https://www.reddit.com/user/ishanfx/) codeblock in my worker thread to execute the tag scraping.

## Possible use cases?
These are entirely speculative (obviously)

 - Training a neural net on tags
 - Compiling statistics on most used words content creators use in their videos.

## Roadmap
In no particular order, #5 is next on the workload

 1. Add command line arguments for headless operation
 2. Add multiple export languages (more than JSON)
 3. Add concurrent threads and multitasking
 4. Clean up code/efficiency/utilizing styleguide
 5. "[setup.py](https://docs.python.org/3/installing/index.html#installing-index)"
 6. PyPi

## Considerations
 1. This is my first ***real*** project with Python
 2. I am educating myself on [PEP 8](https://www.python.org/dev/peps/pep-0008/)
 3. Please branch and submit suggestions to my project, I welcome this very much.
 4. Expect this project to change in the future as I work out more efficient processes to conduct this
 5. Expect dependencies to change, hopefully less than they currently are.


## Dependencies

 - os
 - collections
 - httplib2
 - bs4 (beautifulsoup)
 - requests
 - time
 - sys
 - json
 - random
 - string
 - re
