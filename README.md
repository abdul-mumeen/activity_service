# activity_service

This is a simple activity service used for saving and retrieving historical events. This service has just two endpoints `/heath` and `/events`. The schema are as below;

- `GET /heath` - This is an endpoint that can be pinged to check if the service is up or not.
  response:

  ```json
  {
    "status": "healthy"
  }
  ```

- `GET /events` - This returns a list of historical events based on the query params supplied.

  request:
  `/events/?email=ade%40gmail.com&environment=production&component=order&message=failed&from_date=04-16-2021`

  response:

  ```json
  {
    "events": [
      {
        "component": "order",
        "data": { "age": 20 },
        "email": "ade@gmail.com",
        "environment": "production",
        "message": "order failed",
        "id": "ed24df5o903-ea47ce8a-3ea7df9",
        "created_at": "12411411.23"
      }
    ]
  }
  ```

- `POST /events` - This is used to save events.

  request:

  ```json
  {
    "component": "order",
    "data": { "age": 20 },
    "email": "ade@gmail.com",
    "environment": "production",
    "message": "order failed"
  }
  ```

  response:

  ```json
  {
    "component": "order",
    "data": { "age": 20 },
    "email": "ade@gmail.com",
    "environment": "production",
    "message": "order failed",
    "id": "ed24df5o903-ea47ce8a-3ea7df9",
    "created_at": "12411411.23"
  }
  ```

## Tools Used

### Docker

For easy distribution and ease of starting up, I have dockerized the app and the postgres db used in this app.

### Flask

I used flask, flask-restplus, flask-migrate and other related flask libraries to build the app.

### Postgres

Postgres is the database used for storing events while using flask-SQLAlchemy as the ORM. Any Postgres database can be used with the app, we just need to save the credentials in the `.env` file.

## Running the app

Clone the repository using either `https` or `ssh`

### Using Docker (recommended)

- Install and launch Docker. Ensure it's running.
- Ensure no other service is running on port `5000`.
- On a terminal, `cd` into the root directory.
- Create a `.env` file and update it with the postgres and other environments' details in `.env.sample` file in the directory. For the purpose of testing, we will keep these values so that we can use the postgres db within docker. You can also replace the values in there with your choice.
- Run the command below. This should build and run the app.

  ```sh
      docker-compose up
  ```

- After the containers have been successfully built and running, we can access the endpoints at `http://localhost:5000/api/health` and `http://localhost:5000/api/events`.

### Without Docker

## App Structure

This app is structured in a MVC format such that there can be separation of responsibilities between the different layers of the app. The folder structure is displayed below. Each resource has a model, controller and corresponding view.

```files
root directory
.
+-- models
|   +-- model_a.py
|   +-- model_b.py
+-- restapi
|   +-- endpoints
|   |   +-- resource_a.py
|   |   +-- resource_b.py
+-- services
|   +-- service_a.py
|   +-- service_b.py
+-- other files
```

### Models

This is the data layer where the type of data to be stored in the database is declared. Here is where data saving and retrieving happens. Each resource will typically have a corresponding file for its model. In this app, we have only one resource which is `event`, so we have just one file in the models folder.

#### Fields of event model

- `id` - A unique hexadecimal string to identify each event data. I used a UUID4 generator to automatically generate this unique because;
  1. The UUID4 uses a random number to generate unique id such that the probability of generating two same one at different times is so low that it can be ignored.
  2. An auto-generated integer incrementing id would have guaranteed non-collision in id but that is not safe because guessing a number has a high probability that a record exists that matches it, which makes it a lot easier for an attacker to get unauthorized data.
- `component` - Required string type.
- `created_at` - A datetime field generated when the event data is saved.
- `data` - Json data type with no specific schema.
- `email` - Email address saved as string.
- `environment` - Required string type telling where the event occured.
- `message` - Required string type which describes the event in a way.

### Endpoints (views)

This is what represents the views in our MVC structure as this is where input data are collected and also responsible for formatting and sending out user's data.

### Services (Controllers)

This is an intermediary between the data layer and the presentation layer. It holds all the `business logic` which means decisions about the data regarding the business can be implemented here. Each resource will have a corresponding service module that holds business logic associated with that resource.
For business logic that cuts across multiple resources, this can be placed inside an `util` module such that it is accessible to different modules. And if in the future, the business logic becomes complex, it could be extracted into a microservice of its own.

## Testing

I would write both integration and unit tests.

### Integration tests

These are tests to confirm the end-to-end functionality of the app. This means actual data are used for testing and real results are expected. I would set up a different docker container with a test database which actual data can be written to when testing and the data and table will be removed after testing.

#### Integration tests for `events` endpoint

This will be done by calling the endpoint with different data combinations and confirming the response matches the expected output.
Different scenarios that will be tested for `POST` are;

- All request data are valid.
- All request data are empty.
- Invalid email.
- Invalid json data.
- Empty component data.
- Empty message data.
- Empty environment data.

Different scenarios that will be tested for `GET` are;

- Request with no query params.
- Request with all query params.
- Request with invalid `from_date` query param.

### Integration tests for `Event` model

This is carried out by passing both valid and invalid data to the data layer and trying to save it to confirm if the operation is successful when data is valid and error thrown when invalid.

### Unit tests

These are tests majorly written for functions executing the business logic. A set of data or events are initiated and outputs and responses are confirmed if they match the expected behaviour.
In the case of activity service, we will be passing different data values to the functions in the event service module while mocking calls to the database. The returned values are asserted and the reactions (error raised or otherwise) are confirmed to meet the expected behaviour.

## Handling 100 activity per second
