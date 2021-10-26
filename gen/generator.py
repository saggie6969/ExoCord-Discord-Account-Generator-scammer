from requests.models import Response
from email_verificator import EmailVerifier
from httpx import Client
from discord_build_info_py import *
from base64 import b64encode as b
from hcapbypass import bypass
from pfp_changer import change_pfp

import json
import urllib3
import random
import string
import time
import discum
from random import sample

def insert_dots(s, k):
    indices = sorted(sample(range(1, len(s) - 1), k))

    intervals = []

    for i, j in zip([0] + indices, indices + [len(s)]):
        intervals.append(s[i:j])

    return '.'.join(intervals)

urllib3.disable_warnings()


class TokenGenerator:
    def __init__(self, verbose, proxy, names, pfps):
        self.VerboseOutput = verbose
        self.gmail = 'bauerchaim6'
        self.UsedProxy = proxy
        self.session = Client(proxies={"https://": f"http://{self.UsedProxy}"})

        dcfduid, sdcfduid = self.GetDcfduid()
        if self.VerboseOutput:
            print("[!] Obtained __dcfduid cookie! ({})".format(dcfduid))
            print("[!] Obtained __sdcfduid cookie! ({})".format(sdcfduid))
        self.dcfduid = dcfduid
        self.sdcfduid = sdcfduid
        self.session.cookies['__dcfduid'] = dcfduid
        self.session.cookies['__sdcfduid'] = sdcfduid
        self.session.cookies['locale'] = 'it'
        self.usedmails = []

        fingerprint = self.GetFingerprint()
        if self.VerboseOutput:
            print("[!] Obtained fingerprint! ({})".format(fingerprint))
        self.fingerprint = fingerprint

        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
        build_num, build_hash, build_id = getClientData('stable')
        print(build_num)

        self.super_properties = b(json.dumps({
            "os": "Windows",
            "browser": "Firefox",
            "device": "",
            "system_locale": "us-US",
            "browser_user_agent": user_agent,
            "browser_version": "90.0",
            "os_version": "10",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": int(build_num),
            "client_event_source": None
        }, separators=(',', ':')).encode()).decode()

        self.name = random.choice(names)
        self.pfp = random.choice(pfps)
    

    def GetDcfduid(self):
        resp = self.session.get(
            'https://discord.com/register')
        return resp.cookies['__dcfduid'], resp.cookies['__sdcfduid']

    def GetFingerprint(self):
        return self.session.get("https://discordapp.com/api/v9/experiments", timeout=10).json()['fingerprint']

    def CreateAccount(self, payload, captcha=None):
        if captcha:
            payload['captcha_key'] = captcha

        headers = {
            'Accept':               '*/*',
            'Accept-Encoding':      'gzip, deflate, br',
            'Accept-Language':      'it',
            'Authorization':        'undefined',
            'Cache-Control':        'no-cache',
            'Connection':           'keep-alive',
            #'Content-Length':       str(len(str(payload).replace(' ', '').replace('None', 'null')) + 2),
            'Content-Type':         'application/json',
            'Cookie':               '__dcfduid=' + self.dcfduid + '; __sdcfduid=' + self.sdcfduid,
            'Host':                 'discord.com',
            'Origin':               'https://discord.com',
            'Pragma':               'no-cache',
            'Referer':              'https://discord.com/register',
            'Sec-Fetch-Dest':       'empty',
            'Sec-Fetch-Mode':       'cors',
            'Sec-Fetch-Site':       'same-origin',
            'TE':                   'Trailers',
            'User-Agent':           "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
            'X-Fingerprint':        self.fingerprint,
            'X-Super-Properties':   self.super_properties
        }

        return self.session.post('https://discord.com/api/v9/auth/register', headers=headers, json=payload).json()

    def GenerateToken(self):
        mail = insert_dots(self.gmail, 3) + "@gmail.com"
        if (mail in self.usedmails):
            return
        self.usedmails.append(mail)
        print(mail)
        payload = {
            'fingerprint':      self.fingerprint,
            'email':            mail,
            'username':         "ExoCord - Account Creator",
            'password':         'Aniello123',
            'invite':           None,
            'consent':          True,
            'date_of_birth':    "1999-11-01",
            'gift_code_sku_id': None,
            'captcha_key':      None
        }

        response = self.CreateAccount(payload)

        if 'captcha_key' in response:
            while 1:
                times = 0
                captcha_solved = bypass(
                    "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34", "discord.com", self.UsedProxy, True)
                if captcha_solved != False:
                    break
                times += 1
                if times >= 5: return '[!] Captcha Fail'
            response = self.CreateAccount(payload, captcha_solved)
            

        if 'retry_after' in response:
            return "[!] Rate limit! ({})".format(str(response['retry_after']))
            time.sleep((response['retry_after'] / 1000) + 5)
            response = self.CreateAccount(payload, bypass(
                "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34", "discord.com", self.UsedProxy))

        if 'token' not in response:
            return response

        token = response["token"]

       

        return response