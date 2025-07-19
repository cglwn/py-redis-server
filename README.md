`py-redis-server` is a native Python implementation of the Redis server.
It was developed with the test suite from CodeCrafter's [Build your own Redis](https://app.codecrafters.io/courses/redis).

# Usage
Run the server
```sh
pipenv run python3 -m app.main
```

It runs on port `6379` and communicates with `redis-cli`
```
$ redis-cli PING
PONG
```