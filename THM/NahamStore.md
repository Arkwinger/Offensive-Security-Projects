# Naham Store Walkthrough

___________________________



```
root@ip-10-201-21-194:~# ffuf -u http://nahamstore.thm -c -w /usr/share/wordlists/SecLists/Discovery/Web-Content/raft-medium-words-lowercase.txt -H 'Host: FUZZ.nahamstore.thm' -fw 125

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.3.1
________________________________________________

 :: Method           : GET
 :: URL              : http://nahamstore.thm
 :: Wordlist         : FUZZ: /usr/share/wordlists/SecLists/Discovery/Web-Content/raft-medium-words-lowercase.txt
 :: Header           : Host: FUZZ.nahamstore.thm
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
 :: Filter           : Response words: 125
________________________________________________

shop                    [Status: 301, Size: 194, Words: 7, Lines: 8]
www                     [Status: 301, Size: 194, Words: 7, Lines: 8]
marketing               [Status: 200, Size: 2025, Words: 692, Lines: 42]
stock                   [Status: 200, Size: 67, Words: 1, Lines: 1]
:: Progress: [56293/56293] :: Job [1/1] :: 6887 req/sec :: Duration: [0:00:10] :: Errors: 0 ::
```
