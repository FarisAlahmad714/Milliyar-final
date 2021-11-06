#!/bin/bash

sudo service nginx reload
sudo service nginx start



    ApplicationStart:
    - location: scripts/start_server
      timeout: 6000
      runas: ubuntu