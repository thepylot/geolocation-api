[![Build Status](https://travis-ci.com/raszidzie/geolocation-api.svg?branch=main)](https://travis-ci.com/raszidzie/geolocation-api)

# Geolocation API
Endpoints for geolocation data based on IP or URL

## Getting Started
This project works on **Python 3+** and Django 2+.

1. Create free API KEY from https://ipstack.com and update ```ACCESS_KEY``` field in ```.env.dev``` file with your key.

2. Build the project by following command:

```
docker-compose build
````

and run the containers:

```
docker-compose up
```

3. Create a new user by navigating to http://localhost:8000/api/user/create.

4. Once a new user created generate JWT token by navigating to http://localhost:8000/api/user/token

5. Copy the ```access``` and put it to your headers like below:

``` Bearer <YOUR_ACCESS_KEY> ```

We recommend to use ModHeader extension to manage headers in Chrome

6. Finally, navigate to http://localhost:8000/api to access endpoints

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
