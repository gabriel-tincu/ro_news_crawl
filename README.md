## Use this to crawl romanian news sites and store content to either mongo or ES

### install
  get [python 3](https://www.python.org/) and [virtualenv](https://pypi.python.org/pypi/virtualenv)
  ```bash
   virtualenv venv --no-site-packages --python python3
   source vev/bin/activate
   pip install -r requirements.txt
   python main.py
   ```
     
### docker launch
   [install docker](https://www.docker.com/)
   ```bash 
   docker stack deploy -c docker/stack.yml crawl
   ```
   
### TODO
   [ ] use `scrapyd` to deploy
   [ ] have a look at deduplication and what it entices in case of service failure
   [ ] figure out why ES doesn't play nicely inside docker