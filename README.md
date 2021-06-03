
# Deta Echo Cache

Leverage the awesome [Deta Micros](https://docs.deta.sh/docs/micros/about) and [Deta Base](https://docs.deta.sh/docs/base/about) to cache requests and echo them as needed. Stop worrying about slow public APIs or agressive rate limits. Keep building, creating, sharing, and make the most of the many great data sources out there while taking some of the pressure of those that graciously provide them.

## Installation 

Clone the repo and deploy on a Deta Micro in just a few seconds!
```bash 
  git clone https://github.com/Gingerbreadfork/deta-echo-cache
  cd deta-echo-cache
  deta new -p
```
    
## Usage

Once you have it deployed you can send requests including a target to get or cache, whether it fetches or not will depend on if it has been requested recently and if the tolerance time has elapsed since the previous request. For example you can add to the end of your Deta Micro url:<br><br>  ```?tolerance=10&echo=https://jsonplaceholder.typicode.com/posts```<br><br> The above would then get the specified response (the echo) and tolerate data that was as old as 10 seconds (tolerance). You can freely change the echo url and tolerance time (in seconds) to whatever you like. Responses are stored in a Deta base for quick access, you will often find this can be faster than an API you are sending a request to initially.

  
## FAQ

#### How do I clear old cached data from the Deta Base?
To avoid buildup it's a great idea to set a cron using deta, this is easy to do by just running ```deta cron set "1 hours"``` in your terminal modified to suit your needs. You can set how agressive this clean up is from ```main.py``` just by modifying the ```cleanup_tolerance``` variable with how many seconds old you want to keep old responses cached. There's also a clear route, accessing ```/clear``` will perform the same job as the cron would.

#### Can I cache any kind of data?
Not yet, pretty much anything that can be serialized as JSON should be fine though!

#### Is it possible to pass parameters?
Sure, just replace any & with * when passing parameters with your URL that you are using.
  
## Like the Repo?
If you like this repo drop a star and let me know on Twitter! [@gingerbreadfork](https://twitter.com/gingerbreadfork)
