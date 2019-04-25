## BUGS
* in case of missing configuration, stacktrace is dumped
* sha-256 specified in config but sha-1 is in code


## IMPROVE
* versioning
* remove QR code functionality
* improve docs (with zero dependency)


## FEATURE
* better user experience
    - otp add --secret -- issuer --user --digits --algo --period
    - remove get and `otp` to get code
* profiles
    - starred reference
    - otp {id} # id optional
    - otp ls
    - otp add ...
    - otp rm <id>
* hotp support


## TODO
* release 0.2.0!
