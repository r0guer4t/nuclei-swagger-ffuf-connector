# nuclei-swagger-ffuf-connector 

## This is a series of helper scripts to take swagger pages detected in vulnerability scanners and plug them into the ffuf fuzzer developed by tomnomnom [ffuf](https://github.com/ffuf/ffuf)

## Usage

#### Installation

Install ffuf

```bash
go install github.com/ffuf/ffuf/v2@latest
```

Install python dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```


#### Swagger URLS

First thing is to parse output from your scanner. 

This bash liner is good for nuclei but you can alter the field and delimiter to fit other scanners.

```bash

cat [nucleiScanFile.txt] | grep '[Ss]wagger' | cut -d']' -f4- > swaggerVuln.txt
```

#### Docs Parsing

Next step is to crawl these domains for swagger.json files that are parsed into endpoint lists for the fuzzer. This script utilizes multiple user agents in a loop in the event there are different endpoints for different devices or firewall rules. 

```bash
python3 enumSwagger.py
```

This will create an output directory called swagger-jsons where the resulting jsons are stored.

#### Endpoint list creation

Following accumulating the swagger.jsons of the domains now its time to put the domain before the endpoint in a list with the kinds of requests that are accepted by the endpoint (graciously provided by again the swagger.json). 

```bash
python3 processSwagger.py
```

#### ffuf automation

After this neatly created list has been generated now its time to plug it into ffuf. 

#### A word on wordlists

In ffufSwagger.sh at the top of the script is where you will configure your wordlists. WORDLIST1 is path parameters and WORDLIST2 is body data.

```bash
sudo chmod +770 ffufSwagger.sh
./ffufSwagger.sh
```
