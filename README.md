Server:
an aiohttp HTTP server which:
1.has several managed redirect enpoints - the final enpoint will give a successful result
2.has 2 cycled redirection endpoints 
3.Gives out huge/infinite body

Client:
Test client  makes a request to a test  endpoint and sees if it has redirections.
If there are limited/managed redirectionss it will attempt to read the body of the final url.
If there is a cyclic redirection - it will stop after TooManyRedirects exception is raised

Note: Default limit for body is 10000 bytes
