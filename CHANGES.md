Changelog
=========
1.0.23 (2016-12-28)
-------------------
-Added digits to first level domain regex

1.0.23 (2016-12-28)
-------------------
-Invalid / non matching RFC domain was just saying "invalid levels"
-Sauced up README.md

1.0.22 (2016-12-28)
-------------------
-Removed "all" function
-Added ability to load Alexa DB into memory or not
-Added ability to specify how much of the Alexa DB to load into memory
-Added OpenDNS top million
-Added ability to load OpenDNS into memory or not
-Added ability to specify how much of the OpenDNS DB to load into memory

1.0.21 (2016-07-06)
-------------------
-Removed logging every none domain

1.0.20 (2016-07-06)
-------------------
-Fix alexa issue since using iter value if called twice it would not call the DB

1.0.19 (2016-07-06)
-------------------
-Returning str and not int for alexa rank

1.0.18 (2016-07-06)
-------------------
-Don't load Alexa DB into memory and instead use iter

1.0.17 (2016-03-22)
-------------------
-Log fix

1.0.16 (2016-03-22)
-------------------
-Added EoL to domain

1.0.15 (2016-03-22)
-------------------
-Changed naming of level domain length

1.0.14 (2016-03-14)
-------------------
-Cleanup

1.0.13 (2016-03-10)
-------------------
-Adding logging and removed some prints

1.0.12 (2016-02-29)
-------------------
-Alexa rank was not being parsed to lowest common denominator and was returning right away if it did not have a rank.

1.0.11 (2016-02-29)
-------------------
-Fixed 1.0.10

1.0.10 (2016-02-29)
-------------------
-Download error checking and switched to requests

1.0.9 (2016-02-26)
-------------------
-Decreased download rate of Alexa DB
-Code cleanup

1.0.8 (2016-02-17)
-------------------
-Fixed valid domain regex...

1.0.7 (2016-02-05)
-------------------
-Changed stuff probably for no reason

1.0.6 (2016-01-21)
-------------------
-Fixed home directory for windows or linux

1.0.5 (2016-01-21)
-------------------
-Added pprint to examples

1.0.4 (2016-01-21)
-------------------
-Return unique any level domain and any_length domain

1.0.3 (2016-01-21)
-------------------
-Added total levels of domain

1.0.2 (2016-01-21)
-------------------
-GD unicode returns from MongoDB

1.0.1 (2016-01-20)
-------------------
-raise error if not domain is string

1.0.0 (2016-01-18)
-------------------
-initial commit