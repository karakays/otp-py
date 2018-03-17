import hashlib, hmac, time, base64, functools
from enum import Enum

def create_otp(secret, counter):
    token = Token('I2TE4DXFFG4QQKBS', 30, 'SHA1', 6)
    return token.generateCode()
 

class TokenCode:
    def __init__(self, code, start, end):
        self.start = start
        self.end = end
        self.code = code

    @property
    def block(self):
        return self.end - self.start

    @property
    def progress(self):
        current = time.time()

        if current >= self.end:
            return 0

        p = (current - self.start)
        return (p / self.block)

    @property
    def remaining(self):
        current = time.time()
        rem = self.end - current
        return 0 if rem <=0 else int(rem)
        

class TokenType(Enum):
        HOTP, TOTP = range(2)

        @staticmethod
        def fromValue(value):
            if value == 'hotp':
                return TokenType.HOTP
            elif value == 'totp':
                return TokenType.TOTP
            else:
                return None


class Token:
    def __init__(self, secret, period, algorithm, digits):
        self.secret = secret
        self.period = period
        self.algorithm = algorithm
        self.digits = digits

    def toUri(self):
        pass


    def generateCode(self):
        start = time.time()
        counter = int(start / self.period)
        secret_bytes = base64.b32decode(self.secret)

        mac = hmac.new(secret_bytes, counter.to_bytes(8, 'big'), hashlib.sha1)
        digest = mac.digest()
        offset = digest[len(digest) - 1] & 0x0f
        buf = [digest[i + offset] << (8 * (3 - i)) for i in range(4)]
        res = functools.reduce((lambda x, y: x | y), buf)
        code = res % (10 ** self.digits)
        code = str(code)

        while len(code) < self.digits:
            code = '0' + code

        return TokenCode(code, (counter + 0) * self.period, (counter + 1) * self.period)


    @classmethod
    def fromUri(cls, uri):
        from urllib.parse import parse_qs

        token_type = TokenType.fromValue(uri.netloc)
        if not token_type:
            raise InvalidTokenUriError()

        params = parse_qs(uri.query)

        secret = params.get('secret')
        secret = None if not secret else secret[0]
        if not secret:
            raise InvalidTokenUriError()

        period = params.get('period')
        try:
            period = 30 if not period else int(period[0])
        except ValueError:
            raise InvalidTokenUriError()
        
        digits = params.get('digits')
        try:
            digits = 6 if not digits else int(digits[0])
        except ValueError:
            raise InvalidTokenUriError()

        algorithm = params.get('algorithm')
        algorithm = 'SHA1' if not algorithm else algorithm[0]

        return Token(secret, period, algorithm, digits)


    @classmethod
    def fromString(cls, string):
        from urllib.parse import urlparse
        return Token.fromUri(urlparse(string))


class InvalidTokenUriError(Exception):
    pass

