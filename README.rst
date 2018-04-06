=======
otp-gen
=======

A command line interface for generating one time passwords as per `RFC 4226`_ and `RFC 6238`_

------------
Requirements
------------
* Python version 3.6.x and greater

------------
Installation
------------
The way to install aws-cli is to use `pip`_

.. code:: bash

    $ pip install otp-gen

---------------
Getting Started
---------------

You need to provision secret key, issuer, user, period, digits, secure hash algorithm with *config* command. Default values are shown inside
parantheses. 

.. code:: bash

    $ otp config
    Secret key: JBSWY3DPEHPK3PXP
    Issuer: Foo
    User: Bar
    Period (30 seconds):
    Digits (6):
    Algorithm (SHA-256):

---------------
Usage
---------------

You can request a new OTP by using *get* command. A progress bar showing expiry period of the current valid code is provided along. get command continuously updates new codes.


.. code:: bash

    $ otp get
    Code = 004790, progress [*****************-----------------------]

Current configuration can be embedded in a QR code by using *qrcode* command.


.. code:: bash

    $ otp qrcode

---------------
References
---------------

* https://github.com/google/google-authenticator/wiki/Key-Uri-Format
* https://github.com/freeotp

---------------
License
---------------

otp-gen is under `MIT license`_

.. _pip: http://www.pip-installer.org/en/latest/
.. _`RFC 4226`: http://tools.ietf.org/html/rfc4226
.. _`RFC 6238`: http://tools.ietf.org/html/rfc6238
.. _`MIT license`: https://opensource.org/licenses/MIT
