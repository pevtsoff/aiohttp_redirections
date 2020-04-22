Server:
an aiohttp HTTP server which:
1.has several managed redirect enpoints - the final enpoint will give a successful result
2.has 2 cycled redirection endpoints 
3.Gives out huge/infinite body

Client:
Test client  makes a request to a test  endpoint and sees if it has redirections.
If there are limited/managed redirectionss it will attempt to read the body of the final url.
If there is a cyclic redirection - it will stop after TooManyRedirects exception is raised

Launch:
1.python3 server.py
2.pytest -s -v (don't forget the flags, otherwize the output won't be shown)
