# OmegaPricing

Docker version 1.12.6

I am a huge fan of docker/docker-compose. Hopefully you should not have any trouble running the test suite.

#### Running tests

The tests aren't comprehensive. They just test the basic desired requirements but I think they do show
some of the basic testing concepts you might be looking for (mocking requests to 3rd party APIs, etc)

`docker-compose run web python manage.py test`

#### Notes

Specific notes can be found as comments inside the code. The `requests` Library is always a huge help
when making external API calls. I am a huge fan of Django Rest Framework and the Mock libraries. For the
purposes of this demo I am just logging to the console. Normally I would log to a file or to an external tool
like loggly or something.
