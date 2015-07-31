A simple demonstration of how to use Redis lists for interprocess communication. In this example the producer and consumer processes are spun up from the same script using Python's multiprocessing module, however processes written in a different language or run in a different manner would work in exactly the same way.

# Installation

 1. Get and compile redis
 
 ```
 wget http://download.redis.io/redis-stable.tar.gz
 tar xvzf redis-stable.tar.gz
 cd redis-stable
 make
 ```

 2. (Optional) run tests
 
 ```
 make test
 ```

 3. (Optional) install - binaries are in `src` if you don't want to do this
 
 ```
 make install
 ```
 

 4. Install python's Redis bindings
 
 ```
 sudo pip install redis
 ```
