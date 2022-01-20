# TWITER PARSER
____
## This is http parser of twits from Elon Musk twitter

This http parser repeats the user path. Parse 10 last twits and links to the first 3 commentators

For the starting work python 3 is required.

## PRE-setup
1. fill in the proxy data in **.env** file
```
    PROXY_IP= "your_proxy_ip"
    PROXY_PORT= "your_proxy_port"
    PROXY_LOGIN= "your_proxy_login"
    PROXY_PASSWORD= "your_proxy_password"
    PROXY_TYPE="http or https"
```

## Starting project
```
pip install -r requirements.txt
python twitter_parser.py
```