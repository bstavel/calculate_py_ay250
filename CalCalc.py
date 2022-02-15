#!/usr/bin/env python

import argparse
import numexpr as ne
import numpy as np
import requests
import os
import urllib.parse
import re


def ask_wolfram(str_exp):

    app_id = 'LA2L7A-2JGQA2LXP6'
    query = urllib.parse.quote_plus(str_exp)
    query_url = f"http://api.wolframalpha.com/v2/query?" \
                 f"appid={app_id}" \
                 f"&input={query}" \
                 f"&format=plaintext" \
                 f"&includepodid=Result" \
                 f"&output=json"

    r = requests.get(query_url).json()

    data = r["queryresult"]["pods"][0]["subpods"][0]
    plaintext = data["plaintext"]

    # clean up result by removing letters and replacing wolfram alpha specific x with *, etc
    plaintext = plaintext.replace('×','*').replace('^','**')
    plaintext = re.sub('[^\d\.\*]', '', plaintext)

    result = ne.evaluate(plaintext)
    return(result.tolist())

def calculate(str_exp):
    try: 
        result = ne.evaluate(str_exp)
        return(result.tolist())
    except:
        try:
            result = ask_wolfram(str_exp)
            return(result)
        except (ValueError, SyntaxError):
            print("Wolfram alpha could not solve the issue")
        


if __name__ == '__main__':
    # parse command line arguements 
    parser = argparse.ArgumentParser(description='evaluate expression')
    parser.add_argument('-s', action='store', dest='str_exp',
                    help='String to parse')
    results = parser.parse_args()
    
    print(calculate(results.str_exp))
    
