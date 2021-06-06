# [cl-flags] prints all accounts
$ otp
github (user) 123456 12
udemy (user) 123456 29
binance (user) 123456 3

# [cl-flags] prints default profile with progress
$ otp -p
123456

# [cl-flags] copies into clipboard 
$ otp -c
123456

# [cl-flags] list accounts
$ otp ls
1. (*) issuer-1 for user
2. issuer-2 for user
3. issuer-3 for user

# [multiple-accounts] support multiple accounts

# [token-for-account] prints token for account with id 2
$ otp -a 2

# [auto-complete] select account with auto-complete
$ otp -a git<Tab>
github ...
$ otp -a <Tab>
github
udemy
binance

# [timer-progress-bar] count down with ansi escape color codes
$ otp
issuer user <red>{code}</red>

# [decode-qr-image]
* decode qr code
  https://betterprogramming.pub/how-to-generate-and-decode-qr-codes-in-python-a933bce56fd0
* remove qr code export
  
# [sha-1 and sha-3 support]
* SHA-1 SHA-3 support

# [hotp-support]
* hotp support