# Python Module for accessing Shield Cloud API

__version__="0.2.9"


import json

# special import so that we can hack the connection method to bootstrap it
from urllib3.util import connection

_orig_create_connection = connection.create_connection

# main requests library that will call urllib3
import requests

# dns libraries could be imported conditionally during init
import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query
import dns.resolver

import os
import copy

import socket

# used in the registry/auth response
import jwt

# regex used to prototype whitelisting - there are probably much faster ways to right-match a string
import re
# sys is used to output to stderr
import sys

# the following commented out code belongs in the shieldmethod class

# methods that are called before DNS resolution (effectively replacing it) are in this list:
# PRE_RESOLVE_METHODS = [SHIELD_CLOUD_API_V1, SHIELD_DNS_API_JSON, GOOGLE_DOH]

# methods that are called after DNS resolution are in this list:
# POST_RESOLVE_METHODS = [
#    SHIELD_RECURSOR_DNS,
#    GOOGLE_DNS,
# ]

# methods that are not in either list will fail
# methods that are in both lists will probably only work at the PRE_RESOLVE stage

# bootstrap hostnames to allow query of HTTPS endpoints to provide DNS information (when DNS is obviously not available)
# please use the bootstrap_host_add funcion to add new entries during initialisation of your script
bootstrap_fqdn = {
    "developer.intrusion.com": "34.98.66.35",  # Shield Cloud API endpoint
    "dns.google": "8.8.8.8",  # Google DNS
    "zegicnvgd2.execute-api.us-west-2.amazonaws.com": "52.32.153.91",  # Shield DNS API endpoint (alpha)
}

#initialise global variables for bootstrap dns
bootstrap_dns = ''
bootstrap_dns_suppress = False

# constant for INTZ proprietary EDNS option
EDNS_OPT_INTZ_AUTHZ = 64053

# debuging disabled by default, integer 0-5
debug = 0 

# Shield methods to be implemented as an enum here:
from enum import Enum



class shieldmethod(Enum):
    SHIELD_CLOUD_API_V1 = 1  # Apigee Interface with V1 URLs
    SHIELD_DNS_API = 20  # DOH with dns-message method, via AWS API with an API key
    SHIELD_DNS_API_JSON = (
        21  # DOH using dns-query method, use this to get extended information easily
    )
    SHIELD_RECURSOR_DNS = 53            # query with UDP, fallback to UDP
    SHIELD_RECURSOR_DNS_AUTH = 63       # send an auth product using a proprietary method
    SHIELD_RECURSOR_DNS_REGISTER = 73   # (placeholder) register with Shield API endpoint and receive an auth product

    CLOUDFLARE_DNS = 1111  # testing
    GOOGLE_DNS = 8888  # testing mode using 8.8.8.8 DNS
    GOOGLE_DOH = 8889  # testing mode using JSON GET to 8.8.8.8

    # default function
    @classmethod
    def default(cls):
        return cls.SHIELD_CLOUD_API_V1


def bootstrap_host_add(hostname, address):
    # simply adds an entry to the global bootstrap_fqdn structure
    # done as a separate function because we might want to add extra logic or validation here
    
    #global bootstrap_fqdn

    #only store and compare owercase hostnames
    hostname = hostname.lower()

    bootstrap_fqdn["hostname"] = address


def bootstrap_lookup(hostname):
    # lookup a hostname before system DNS is available
    # priority:
    #   bootstrap_fqdn structure
    #   boostrap_dns server lookup for A record
    #
    # returns:
    #   address, can be either IPv4 or IPv6, not validated
    #   false if no answer available

    #global bootstrap_fqdn
    global bootstrap_dns
    #global bootstrap_dns_suppress

    if not bootstrap_dns:
        bootstrap_dns = '8.8.8.8'

    bootstrap_dns_timeout = 3

    # mediate hostname
    lookup_hostname = hostname
    # remove whitespace
    lookup_hostname = lookup_hostname.strip()
    # only check lowercase hostnames
    lookup_hostname = hostname.lower()
    if lookup_hostname[-1] == '.':
        lookup_hostname = lookup_hostname[0:-1]

    if lookup_hostname in bootstrap_fqdn:
        return bootstrap_fqdn[lookup_hostname]

    # got to here? try a DNS lookup unless someone has set the suppress feature
    
    if bootstrap_dns_suppress:
        # we are not supposed to try and look this up somewhere else
        return False

    if not bootstrap_dns:
        # there is no way to lookup additional information
        return False



    # consider using the resolve mode rather than query here


    bootstrap_resolver = dns.resolver.Resolver()
    # note that an array is required here but we provide one with just a single element because we are simps
    bootstrap_resolver.nameservers = [bootstrap_dns]

    answer = bootstrap_resolver.query(hostname,"A")

    print(answer)

    # check the answer for A records

    if answer[0]:
        return answer[0].address
    

    # do something with CNAME?

    # check additional for A records    

    return False    
    

def bootstrap_create_connection(address, *args, **kwargs):
    # this function provides a connection to developer.intrusion.com, the IP address cannot be resolved at boot time because we are the DNS
    # ideally, we might give a global variable here that is bootstrap resolved during init
    # but for now just use a hard coded IP

    # if you try to use the "connection" function elsewhere in your own program, it may instead use this one which will create problems

    # one day this will be replaced by a DNS Adapter function so that

    # print("DEBUG: using bootstrap_create_connection")

    host, port = address
    #hostip = "34.98.66.35"
    hostip = bootstrap_lookup(host)
    return _orig_create_connection((hostip, port), *args, **kwargs)


# default debug error printing
def error_print(text):
    sys.stderr.write("stderr {}".format(text))

# put a default def here to make it global
debug_print = error_print

# debug message takes two parameters - a message and a debug level
# level 1 = critical
# level 5 = annoying
def debug_message(text,level):
    if debug >= level:
        debug_print(text)

# function to redefine debugging ahead of any other definition
def setup_debug(session):
    
    global debug
    global debug_print

    print("Enter setup_debug {}".format(debug))
    if "callback_log" in session:
        if callable(session["callback_log"]):
            debug_print = session["callback_log"]
            debug_print("Callback logging enabled")

    if "debug" in session:
        if (session["debug"]):
            debug = 5
            debug_print("shieldpythonapi Debugging has been enabled")

    print("Exit setup_debug {}".format(debug))


def create_uuid(uniqueid):
    # this is a placeholder - we will leave it to external app to handle uuid
    # create a uuid from the last 12 bytes of a unique string
    pass

def shieldcloud_registry_register(session,devicetype,uuid,apiurl="https://ind0ryey38.execute-api.us-east-1.amazonaws.com/beta",apikey=None,apikeyheader='x-api-key'):
    # calls the register function
        # documented internally here: https://intrusion.atlassian.net/wiki/spaces/ADT/pages/399704065/Registry+-+API+Specification


    debug_message("function: shieldcloud_registry_register",4)

        # need to use the bootstrap functions here
    url = apiurl + '/register'
    payload = {
        "deviceType":   devicetype,
        "uuid":     uuid
    }
    header = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    if apikeyheader:
        header[apikeyheader] = apikey

    # we might want to try: this in a loop to handle a timeout

    response = requests.post(url, headers=header, json = payload)

    debug_message(url,4)
    debug_message(payload,5)
    debug_message(header,5)

    debug_message(response,5)

    # ###
    #
    # THE MOST LIKELY REASON FOR A FAILURE HERE IS BECAUSE THE REGISTRY RETURNS 400 IF THE UUID is NOT VALID
    #
    # ###

    if response.status_code != 200:
        # raise an error here or log something
        debug_print("Registration failed with status code {}".format(response.status_code))
        return False

    #print(response.text)   
    

    jr = json.loads(response.text)
    
    # setup a structure in the session so that we know registration has occurred
    session["registry"] = {'registered': True}

    # check / validate?

    #print("DEBUG")
    #print(jr)

    # if dns is not already configured in session, configure it from response
    if "dnshost" not in session:
        session["dnshost"] = []
        if "dnsService" in jr:
            # note that the example JSON shows uppercase IP but in production returns lower case "ip"
            if "ip" in jr["dnsService"]:
                session["dnshost"].append({"address": jr["dnsService"]["ip"]})
            else:
                # iterate over array of DNS in future version of registry
                # as of August 2023 it only supports the single entry
                pass

    #print(session)

    return session

def shieldcloud_registry_auth(session,uuid,apiurl="https://ind0ryey38.execute-api.us-east-1.amazonaws.com/beta",apikey=None,apikeyheader='x-api-key'):
    # calls the auth function
    # returns a jwt that needs to be decoded

    # hard coded signature - could add this to config
    jwtsignature = "CnORn72bitiSBqIXST6LjCRVdvlVMGyy"

    if not uuid:
        return False

    url = apiurl + '/auth?uuid=' + uuid
    headers = { 'Accept': 'application/json' }
    if apikeyheader:
                headers[apikeyheader] = apikey

    response = requests.get(url,headers=headers)
        
    # test for 200 OK

    if response.status_code != 200:
        return False

    jr = json.loads(response.text)

    #decode jwt?    

    # note that leeway is only necessary because sometimes the iat value of the token occurs before the local system time, which causes an error
    jwtjson = jwt.decode(jr["jwt"],jwtsignature,algorithms=["HS256"],leeway=10)

    print(jwtjson)

    # product key learned from jwt is authoritative
    session["authproductint"] = int(jwtjson["product"],16)

    # put the expiry in the session so something has a chance to re-auth
    session["registry"]["authexpiry"] = jr["expiry"]

    return session


# global function to replace connection routine used by "requests" with our bootstrapped routine
connection.create_connection = bootstrap_create_connection


# helper function to load an API key from a local file if it is not available as part of init
# helpful because the developer (me) can re-use their key instead of accidently importing it to github
def apikeyfile(hintname="", hintpath=""):

    filenames = ["shield_apikey","apikey", "apikey.txt"]
    if hintname:
        filenames.insert(0, hintname)

    paths = [os.getcwd(), os.path.expanduser("~")]
    if hintpath:
        paths.insert(0, hintpath)

    # nested loops to look for candidates
    for f in filenames:
        for p in paths:
            file = "{}/{}".format(p, f)

            #debug info
            if debug > 3:
              print("Looking for apikey in: {}".format(file))

            if os.path.exists(file):
                # read until we get a line that is not:
                #   whitespace
                #   beginning with #
                #   shorter than 32 characters (the API key length is 49)
                # revise to 19 chars to allow authproduct to use the same file

                h = open(file, "r")
                lines = h.readlines()
                for line in lines:
                    line = line.strip()
                    #print("len debug: {}".format(len(line)))
                    if line and not line.startswith("#") and len(line) > 17:
                        #print("debug: " + line)
                        return line

    # if we get to here then there is no apikey
    return False

# delete this func
#def shieldcloud_register(session,apiurl="https://ind0ryey38.execute-api.us-east-1.amazonaws.com/beta"):
#   # calls the register function
#   # documented internally here: https://intrusion.atlassian.net/wiki/spaces/ADT/pages/399704065/Registry+-+API+Specification
#
#   # need to use the bootstrap functions here
#
#   return true 

def validate_SHIELD_RECURSOR_DNS_AUTH(config):
    
    if not config["productkey"]:
        raise Exception("Cannot authenticate DNS without a product key or registration")
        return false

    # default dns
    if not config["dnshost"] or not config["dnshost"][0]["address"]:
        config["dnshost"] = []
        config["dnshost"].append({"address": '198.58.73.13'})

    # maybe pass the config to a vanilla dns validation routine to check parameters

    # transform the productkey into authproductint
    if isinstance(config["productkey"],str):
        config["authproductint"] = int(config["productkey"],16)
    elif isinstance(config["productkey"],int):
        config["authproductint"] = config["productkey"] 

    return config


def validate_SHIELD_RECURSOR_DNS_REGISTER(config):
    
    # validate register specific information

    if "devicetype" in config:
        # convert to integer
        devicetype = config["devicetype"]
    else:
        # 10 is the default for shieldcloudapi
        devicetype = 1

    if "uniqueid" in config:
        uuid = config["uniqueid"]
    else:
        # do we fail here, leave it blank or generate a uuid?
        uuid = ''

    # allow config of apiurl
        
    apiurl = "https://ind0ryey38.execute-api.us-east-1.amazonaws.com/beta"
    apikey = config["registrykey"]

    # allow config of apikeyheader

    # register with API

    register_config = shieldcloud_registry_register(config,devicetype,uuid,apiurl,apikey,'x-api-key')
    if register_config:
        # get parameters from register_config       
        pass

    else:
        # we can still run without registration if we already have a product key
        if "productkey" not in config:
            return False
        else:
            return config

    # auth with api and get productkey

    auth_config = shieldcloud_registry_auth(register_config,uuid,apiurl,apikey,'x-api-key')
    
    if not auth_config:
        return config

    # validate dns_auth information
    
    # validate dns information

    # return valid config

    config = auth_config
    
    return config

def validate_method(config):
    # does specific validation and/or sets defaults for particular methods


    # set the default method if none, this should probably call the default/_missing_ function in the shieldmethod class
    if not config["method"]:
        config["method"] = shieldmethod.SHIELD_RECURSOR_DNS_AUTH

    # shortcut variable
    m = config["method"]

    # direct to the apropriate function
    # there is probably a more graceful way to do this, but this way I get to nest functions inside each other where functionality overlaps
    if  m == shieldmethod.SHIELD_RECURSOR_DNS_AUTH:
        return validate_SHIELD_RECURSOR_DNS_AUTH(config)

    elif    m == shieldmethod.SHIELD_RECURSOR_DNS_REGISTER:
        return validate_SHIELD_RECURSOR_DNS_REGISTER(config)

    # etc etc

    else:
        return config



def validate_config(config):
    # this takes a config, which preumably comes from a YAML file, and stripts out undefined directives, which builds a new validated_config structure
    # it may also expand some shorthand or aliased configuration

    valid_config = {}

    for pos,t in enumerate(config):
        # convert config directive to lowercase and strip whitespace
        t = t.lower().strip()

        if  t == 'method':
            valid_config[t] = shieldmethod[config[t]]

        elif    t == 'registrykey':
            # check the registrykey
            valid_config[t] = config[t].strip()

        elif    t == 'apikey':
            # if registry key and product key do not exist, this is productkey

            apikey = config[t]
            if isinstance(apikey,int):
                valid_config["productkey"] = apikey
            else:
            
                apikey = config[t].strip()
                if len(apikey) == 18 and apikey[0:2] == '0x':
                    # assume hex string of 16 chars after 0x
                    if "registrykey" not in config and "productkey" not in config:
                        valid_config["productkey"] = apikey
                
                elif "registrykey" not in config:
                    valid_config["registrykey"] = apikey
                

        elif    t == 'productkey':

            productkey = config[t]
            if isinstance(productkey,int):
                valid_config[t] = productkey
            else:

                productkey = config[t].strip()
                # check for valid hex string
                if len(productkey) == 18 and productkey[0:2] == '0x':
                    valid_config[t] = productkey            

        elif    t == 'bootstraphost':
            # test for valid IP address
            valid_config[t] = config[t]

        elif    t == 'uniqueid':
            # test for length or entropy?
            valid_config[t] = config[t]
    
        elif    t == 'dnshost':
            if isinstance(config[t],str):
                # test for valid IP

                # setup dnshost structure (leave blank if no option matches)
                valid_config["dnshost"] = []

                valid_config["dnshost"].append({'address': config[t]})

            elif isinstance(config[t],list):
                # its a list of addresses or dicts
                dnshost = config[t]
                # create the empty list
                valid_config["dnshost"] = []
                for i in dnshost:
                    if isinstance(i,str):
                        # assume it's an address
                        valid_config["dnshost"].append({'address': i})
                    elif isinstance(i,dict):
                        # assume it is a valid structure
                        # come back and flesh out this validation because it will be complicated
                        valid_config["dnshost"].append(i)
        elif    t == "whitelist":
            #whitelist requires a method, config, action
            # NOT VALIDATED while developing
            if isinstance(config[t],dict):
                # validate config
                if "whitelist_config" in config[t]:
                    pass

                elif 'whitelist_file' in config[t]:
                    config[t]["whitelist_config"] = config[t]["whitelist_file"]
                
                # validate action
                if "whitelist_action" in config[t]:
                    config[t]["whitelist_action"] = config[t]["whitelist_action"].strip().lower() 
                    if config[t]["whitelist_action"] in {"ignore","split_horizon"}:
                        pass
                    else:
                        config[t]["whitelist_action"] = 'edns'
                else:
                    config[t]["whitelist_action"] = 'edns'
                        

                # validate method
                if 'whitelist_method' in config[t]:
                    config[t]["whitelist_method"] = config[t]["whitelist_method"].strip().lower()
                    if config[t]["whitelist_method"] in {"cdb","dbm","textreverse"}:
                        pass
                    else:
                        config[t]["whitelist_method"] = 'text'

                    valid_config[t] = config[t]

        elif    t == "callback_log":
            # this is a special case that cannot be configured from a file, it must be inserted into the config by the calling program
            if callable(config[t]):
                valid_config[t] = config[t]

    # here we should probably do some checks that the minimum config is available

    # load in some defaults if items are missing?

    
    
    # perhaps set a timestamp
    valid_config["validated"] = True

    # return the valid data we got here
    return valid_config             


def init_config(config):

    # setup debugging before validation so errors can be logged
    setup_debug(config)

    # only use a validated config from here
    valid_config    = validate_config(config)

    # error if there is no valid_config

    # validate the specific config for the configured method

    session     = validate_method(valid_config)
        
    return session

# init function to load authentication credentials
# also determines the method used to retreive information (Shield Cloud API, Shield DNS API, Shield Recursor DNS)
# returns some kind of session, allowing multiple API hosts (ie: prod, stage) to be used simultaneously
#
# NOTE TO DEVELOPERS - documentation is at developers.intrusion.com, API calls go to developer.intrusion.com. subtle.


def init(
    apikey,
    method=shieldmethod.SHIELD_CLOUD_API_V1,
    apihost="developer.intrusion.com",
    timeout=5,
    loadbalance="none",
    debug=0,
):

    # api key
    # method
    # apihost
    # timeout - seconds, under normal conditions we might set this to 30, but in a firewall application we need a quick response!
    # loadbalance - placeholder to decide how we multiple api hosts are handled
    # debug - return a debugging response that includes full HTTP headers of request/response

    session = {}

    # print("SC Variable type")
    # print(type(method))

    # allow the session to be setup using different variables for "method"
    # if type(method) is enum:
    #   session["method"] = method
    #
    if type(method) is str:
        # test to see if str is actually an integer

        session["method"] = shieldmethod[method]
        # test for valid method, otherwise warn
        #print("Method str")


    elif type(method) is int:
        session["method"] = shieldmethod(method)
        #print("Method int")

    elif isinstance(method,shieldmethod):
        #uses the method class
        session["method"] = method

    else:
        session["method"] = shieldmethod.default()
        #print("Method default")

    #print("SC method configured: {}".format(shieldmethod(session["method"])))

    # this is a catch all, if a valid method is not set, set it to default
    if type(session["method"]) == "NoneType" or not isinstance(
        session["method"], shieldmethod
    ):
        # print("DEFAULT method")
        session["method"] = shieldmethod.default()

    # replace the incoming "method" with whatever got configured
    method = session["method"]

    # debug throwaway
    # print(type(session["method"]))
    # print("session method:")
    # print(session["method"])
    # print("requested method:")
    # print(method)
    # print("apikey:")
    # print(apikey)
    # print()

    session[
        "loadbalance"
    ] = loadbalance  # validation of this parameter can be done below

    if method == shieldmethod.SHIELD_CLOUD_API_V1:
        # validate api key, maybe some kind of regex is appropriate

        # try and find it in a local file
        if not apikey:
            apikey = apikeyfile()

        if not apikey:
            raise ValueError("init: invalid apikey")

        # validate apihost - in a future version intrusion might introduce load balancing functionality here
        if not apihost:
            raise ValueError("init: empty api host, cannot proceed")

        session["apihost"] = apihost
        session["apikey"] = apikey
        session["urlprefix"] = "https://" + apihost
        session["headers"] = {"Content-type": "application/json", "x-apikey": apikey}

        # might need to bump up the default timeout for APIGEE

        return session

    elif method == shieldmethod.SHIELD_RECURSOR_DNS:

        dns_hosts = []  # list of IPv4 and IPv6 addresses
        #dns_default = ["198.58.73.13"]
        dns_default = ["131.186.6.89"]

        # add default IP if blank
        if 1:
            dns_hosts = dns_default
        # change default "developer.intrusion.com" to default IP

        # bootstrap resolve hostname, ie: bind-dev.rr.shield-cloud.com

        # setup a scoreboard to test that DNS is working before we try and use it

        session["dnshosts"] = dns_hosts
        session["dnshost"] = []
        for i in dns_hosts:
            session["dnshost"].append({"address": i})

        return session

    elif method == shieldmethod.SHIELD_RECURSOR_DNS_AUTH:

        dns_hosts = []
        #dns_default = ["198.58.73.39"]
        dns_default = ["131.186.6.89"]

        if not dns_hosts:
            dns_hosts = dns_default

        session["dnshosts"] = dns_hosts
        session["dnshost"] = []
        for i in dns_hosts:
            session["dnshost"].append({"address": i})

        # these things should come from config hash
        session["timeout"] = 3
        session["maxretries"] = 3   # maximum number of retries across all hosts


        # use apikey as a substitute for the auth product
        if not apikey:
            apikey = apikeyfile()

        if not apikey:
            raise ValueError("init: invalid auth product")

        # validate auth product
        # - it should be a 64-bit integer
        # - it should start with 0x

        session["authproduct"] = apikey
        if isinstance(apikey,int):
            session["authproductint"] = apikey
        else:
            session["authproductint"] = int(apikey,16)

        return session

    elif (
        method == shieldmethod.SHIELD_DNS_API_JSON or method == shieldmethod.GOOGLE_DOH
    ):
        # only validate API key for SHIELD_DNS_API_JSON
        if method == shieldmethod.SHIELD_DNS_API_JSON:
            # IP address is ok
            if not apihost:
                raise ValueError("DNS JSON - apihost not configured")

            # https://zegicnvgd2.execute-api.us-west-2.amazonaws.com/dns-query

            session["apihost"] = apihost
            session["apikey"] = apikey
            session["urlprefix"] = "https://" + apihost
            session["headers"] = {
                "Content-type": "application/json",
                "x-apikey": apikey,
            }

            # no-op for formatting
            pass
            # expand hostname to IP addresses
            session["url"] = "https://"
            # ipv6 address we should check

        elif method == shieldmethod.GOOGLE_DOH:
            dns_hosts = ["8.8.8.8"]

        else:
            raise ValueError("Unsupported Method for DoH query:", method)

        session["dnshosts"] = dns_hosts
        return session


# doh_simple functions from https://github.com/rthalley/dnspython/blob/master/examples/doh-json.py
def make_rr(simple, rdata):
    csimple = copy.copy(simple)
    csimple["data"] = rdata.to_text()
    return csimple


def flatten_rrset(rrs):
    simple = {
        "name": str(rrs.name),
        "type": rrs.rdtype,
        "typetext": dns.rdatatype.to_text(rrs.rdtype)
    }
    if len(rrs) > 0:
        simple["TTL"] = rrs.ttl
        return [make_rr(simple, rdata) for rdata in rrs]
    else:
        return [simple]


def to_doh_simple(message):
    simple = {"Status": message.rcode()}
    for f in dns.flags.Flag:
        if f != dns.flags.Flag.AA and f != dns.flags.Flag.QR:
            # DoH JSON doesn't need AA and omits it.  DoH JSON is only
            # used in replies so the QR flag is implied.
            simple[f.name] = (message.flags & f) != 0
    for i, s in enumerate(message.sections):
        k = dns.message.MessageSection.to_text(i).title()
        simple[k] = []
        for rrs in s:
            simple[k].extend(flatten_rrset(rrs))
    # we don't encode the ecs_client_subnet field

    # johns EDNS options code - non standard
    # Google says EDNS is not supported
    # https://developers.google.com/speed/public-dns/docs/doh/json
    # IETF document does not mention it
    # https://datatracker.ietf.org/doc/html/draft-bortzmeyer-dns-json

    # hack to define here, re-do as class
    edecodes = {}
    edecodes[15] = "Blocked"
    edecodes[17] = "Filtered"


    modifiedresponse = False
    if message.options:
        edns = []

        for o in message.options:
            infocode = int(o.otype)
            edecode = edecodes[infocode] if edecodes[infocode] else "unknown"
            edns.append(
                {
                    # INFO-CODE and EXTRA-TEXT are defined in RFC 8914
                    "infocode": infocode,
                    "edecode:": edecodes[infocode],
                    "extratext": o.text,
                }
            )
            if infocode > 0:
                modifiedresponse = True

        simple["EDNS"] = edns
        if modifiedresponse:
            simple["ModifiedDNSResponse"] = True

    return simple

def reverse_domain(domain):
    d = domain.split('.')
    ret = '';
    for i in range(d.len(),0):
        if d[i]:
            ret = ret + d[i]
            if i:
                ret = ret + '.'

    return ret


# whitelist lookup test reversed
# reverse list can be sorted by string length for faster lookup
# return true if in the whitelist, false otherwise
# simple version opens the file each time, later version may hold a file open
def whitelist_lookup_reverse_text_simple(session,domain):
    whitelist_file = session["whitelist"]["whitelist_file"]
    rdomain = reverse_domain(domain)
    
    f = open(whitelist_file,'r')
    for x in f:
        if re.match('^'+rdomain):
            return reverse_domain(rdomain)

# forward text whitelist match, simple right-match with regex
def whitelist_lookup_text_simple(session,domain):
    whitelist_file = session["whitelist"]["whitelist_file"]

    debug_print("=== open whitelist_file: {}".format(whitelist_file))
    f = open(whitelist_file,'r')
    for x in f:
        # remove trailing whitespace
        x = x.strip()
        pattern = x + '\.?$'   # optionally match a trailing . character at the end of the domain
        if debug > 4:
          debug_print ("wl entry: {}".format(x))
          debug_print ("pattern: {}".format(pattern))

        # right-match the whitelist domain to the domain query
        if re.search(pattern,domain):
            if debug > 3:
              debug_print("Whitelist Match! {} {}".format(pattern, domain))
            return x

    if debug>3:
        debug_print("No Whitelist match for {}".format(domain))
    return False

#whitelist lookup advises whether a domain is whitelisted or not
# it DOES NOT resolve the domain
# returns false if not whitelisted
# returns the matching domain string if the domain is whitelisted
def whitelist_lookup(session, domain):
    #check for valid session (already checked at query_dns function)
    #if "whitelist" not in session:
    #    return False

    debug_print("Whitelist debug level {}".format(debug))

    if debug>4:
        debug_print("Whitelist Lookup")

    if not isinstance(session["whitelist"],dict):
        #session does not have a valid whitelist structure
        return False

    # choose whitelist type

    # just use the simple text one anyway for now
    if "whitelist_file" in session["whitelist"]:
        if debug>4:
            debug_print("whitelist file")
        return whitelist_lookup_text_simple(session,domain)



# apigee raw API call to resolve domain
def domainresolution_v1(session, domain, querytype):
    # validate session or fail

    # this function will only work for method SHIELD_API_V1

    jdict = {"domain": domain, "querytype": querytype}
    url = session["urlprefix"] + "/domainresolution/v1/"
    #print("URL: " + url)
    #print(session["headers"])
    # response = requests.post(url, json=jdict, headers=session["headers"])
    response = requests.get(url, params=jdict, headers=session["headers"])

    # if debug, grab the headers and request/response here
    # print(response)

    # assume response is json, should probably test for that first
    data = json.loads(response.text)

    # collect some infomation from the requests object and return it as data for better error handling
    data["api"] = {
        "status_code": response.status_code,
        "elapsed": response.elapsed.total_seconds(),
    }

    return data


# call domainresolution_v1 above, and mediate the result into a "standard" JSON DNS response
def domainresolution_v1_mediated(session, domain, querytype):
    result = domainresolution_v1(session, domain, querytype)
    r = {}
    # 0 is an affirmative response, there are other codees for errors
    r["Status"] = 0

    # type should be the numeric code
    r["Question"] = {   "name": domain,
                        "type": dns.rdatatype.from_text(querytype),
                        "typetext": querytype
                        }
    r["Answer"] = result["response"]["answer"]
    r["Authority"] = []
    r["Additional"] = {}

    return r


def domainenrich_v1(session, domain, querytype):
    # validate session or fail

    jdict = {"domain": domain, "querytype": querytype}
    url = session["urlprefix"] + "/domainenrich/v1/"
    #print("URL: " + url)
    #print(session["headers"])
    response = requests.post(url, json=jdict, headers=session["headers"])
    # if debug, grab the headers and request/response here
    # print(response)

    # assume response is json, should probably test for that first
    data = response.text

    return data


def doh_json(session, domain, querytype):
    # validate session of fail

    # session method should be SHIELD_DNS_API_JSON or GOOGLE_DOH
    url = session["url"]

    return false


def query_recursor(session, domain, querytype="A"):
    # this is the standard DNS query

    # validate session

    # just take the first DNS host, add in load balancing code later
    #dns_server = session["dnshosts"][0]
    dns_server = session["dnshost"][0]["address"]

    # add the edns tag here, so that Shield Recursor DNS gives an extended response
    q = dns.message.make_query(domain, querytype, use_edns=0)

    # create an empty list ot hold edns options
    ednsopt = []

    # check if we need to set an edns option 0 to a positive integer for bypass of filtering policy
    if "whitelist" in session and "edns" in session["whitelist"]:
        # technically this is not checking for the case where "edns" is empty
        # b'\x01' is a representation of integer '1' in bytes
        ednsopt.append( dns.edns.GenericOption(0,b'\x01') )
        

    # proprietary intrusion DNS auth method
    if "authproductint" in session:
        ednsopt.append( dns.edns.GenericOption(EDNS_OPT_INTZ_AUTHZ,session["authproductint"].to_bytes(8,'big')) )
        
    # if the list is not empty, use it
    if ednsopt:
        q.use_edns(True, options = ednsopt )

    # validate that it made a query?
    # print("DEBUG 1")
    # print(q.to_text())

    # print("DNS: " + dns_server)

    maxretries = 3 # change to session variable
    retries = 0
    answer = False
    timeout = 3 # change to session variable



    while retries < maxretries and not answer:
        retries = retries + 1
        # run the query
        # implement timeout here later

        # change the server according to the load balance algo before each run

        # set a timer here
        try:
            (r, tcp) = dns.query.udp_with_fallback(
                    q, 
                    dns_server,
                    timeout
                    )
            if not r.answer:
                print("No answer from {} to attempt {}".format(dns_server,retries))
                print("Query: {}".format(q))

                print("Session: {}".format(session))
            else:
                answer = True


        except dns.exception.Timeout:
            print("DNS Timeout")
        except Exception as e:
            print("DNS Exception: {}".format(e))

    if not answer:
        return False

    # use doh_simple code from lambda to turn the wirecode response into a python object
    # print("DEBUG 2")
    # print(r.to_text())

    p = to_doh_simple(r)

    if session["method"] == shieldmethod.SHIELD_RECURSOR_DNS:
        # check for extra guff here to add into the response
        pass
    else:
        # its vanilla DNS
        pass

    # ultimately, lambda_handler.py will probably load this module, wouldn't that be cool
    # that way, customers can run their own lambda handler that points at our infrasructure recursively

    return p


# top function for querying of all methods with a mediated result
def query_dns(session, domain, querytype="A"):

    # if there is no session, raise an error

    # first thing to do is check if the domain is whitelisted
    if "whitelist" in session:
        whitelist_domain = whitelist_lookup(session,domain)
        if whitelist_domain:
            # handle via a whitelist query instead of DNS
            print("=== Whitelist domain for {} ===".format(domain))
            if "whitelist_action" in session["whitelist"] and session["whitelist"]["whitelist_action"] == 'edns':
                session["whitelist"]["whitelist_domain"] = whitelist_domain
                session["whitelist"]["edns"] = 'bypass'

    # shield API does not handle types other than A or AAAA, so we probably need to handle that

    # debug line
    debug_print("query_dns with debug level {}".format(debug))

    if debug > 4:
      debug_print("=== query_dns ===")
      debug_print(session)
    

    if session["method"] == shieldmethod.SHIELD_CLOUD_API_V1:
        # result = domainresolution_v1(session, domain, querytype)
        result = domainresolution_v1_mediated(session, domain, querytype)

    elif session["method"] in [shieldmethod.SHIELD_RECURSOR_DNS, shieldmethod.SHIELD_RECURSOR_DNS_AUTH, shieldmethod.SHIELD_RECURSOR_DNS_REGISTER] :
        result = query_recursor(session, domain, querytype)

    # need to test for failure here in case session["method"] is not valid

    if debug > 4:
      debug_print("=== end query_dns ===")
    return result


def valid_ip(ipaddr):
    try:
        socket.inet_aton(ipaddr)
        return 4
    except socket.error:
        return False

def query_ip(session,ipaddr,verbose=False):
    block = False
    allow = False

    #check if it is a valid ipv4 or ipv6 address

    ipversion = valid_ip(ipaddr)
    if not ipversion:
        return False
    elif ipversion == 4:
        fqdn = "{}.ip.shield-cloud.com".format(ipaddr)
        result = query_dns(session,fqdn)

        if "Answer" in result and "data" in result["Answer"][0]:
            #print(result["Answer"][0]["data"])
            if result["Answer"][0]["data"].startswith("127"):
                block = True
                allow = False
            else:
                block = False
                allow = True

            if verbose:
                # use element 0 in case we one day want to return multiple answers
                result["Answer"][0]["Block"] = block
                result["Answer"][0]["Allow"] = allow
                return result

            elif block:
                return "BLOCK"
            elif allow:
                return "ALLOW"
            else:
                return False
        
        # provide data if it didn't come back with an answer
        if verbose:
            return result
        else:
            return False

    print("ipversion was {}".format(ipversion))

# this function returns 2 items if successful
#   a netmask in CIDR format
#   an action (ie: block or deny)
def query_netmask(session,ipaddr):

    ret = {}

    result = query_ip(session,ipaddr,True)
    if not result:
        print("NOT RESULT")
        return False
   

    print("Block: {}".format(result["Answer"][0]["Block"]))

    if result["Answer"][0]["Block"] == True:
        ret["Action"] = "BLOCK"
        if "Additional" in result:
            # process reply to add whole netmask
            #ret["Netmask"] = "not done yet"

            ret["NetMask"] = "{}/32".format(ipaddr)

        else:
            ret["NetMask"] = "{}/32".format(ipaddr)

    elif result["Answer"][0]["Allow"] == True:
        ret["Action"] = "ALLOW"
        ret["NetMask"] = "{}/32".format(ipaddr)
    else:
        print("ELSE")
        return result


    return ret


def query(session, domain, querytype="ANY"):
    # basic host request
    # return block or allow
    # return list of blocked IP addresses
    # return list of allowed IP addresses

    return false
