[![Build Status](https://travis-ci.com/raszidzie/geolocation-api.svg?branch=main)](https://travis-ci.com/raszidzie/geolocation-api)

# Geolocation API
Endpoints for geolocation data based on IP or URL

## Getting Started
This project works on **Python 3+** and Django 2+.

Create free API KEY from https://ipstack.com and update ```ACCESS_KEY``` field in ```.env.dev``` file with your key.

Build the project by following command:

```
docker-compose build
````

and run the containers:

```
docker-compose up
```

Navigate to http://localhost:8000/api/user/create to create a new user.

Once a new user created generate JWT token by navigating to http://localhost:8000/api/user/token

Copy the ```access``` and put it to your headers like below:

``` Bearer <YOUR_ACCESS_KEY> ```

We recommend to use ModHeader extension to manage headers in Chrome

Finally, navigate to http://localhost:8000/api

## Endpoints
The endpoints are:
* ```/api/locations```
Retrieves the list of created geolocations and allows to add a new geolocation if the IP address and all required response data exists.
* ```/api/locations/<id>```
Retrieves a particular geolocation object and allows PUT, PATCH and DELETE requests.

## Testing
You can run all tests by following command:

```docker-compose run app sh -c "python manage.py test"```

## Live Preview on Heroku
You can visit the link below too see it in production:
