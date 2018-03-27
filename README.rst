=======
otp-gen
=======

A command line interface for generating one time passwords as per `RFC 4226`_ and `RFC 6238`_


------------
Installation
------------


---------------
Getting Started
---------------


---------------
Usage
---------------

.. otp <sub_command> 


.. Generate OTP


.. Generate OTP by URI

.. otp get --uri uri


.. Generate OTP by secret

.. otp get --secret secret


.. Create a URI by OTP parameters 

.. otp uri secret [--issuer issuer] [--user user] [--period period] [--digits digits] [--algorithm algorithm]

.. where secret is a valid base32 encoded secret


.. Create a QR-code by OTP parameters 

.. otp qrcode secret  [--issuer issuer --user user --period period --digits digits --algorithm algorithm]

.. where secret is a valid base32 encoded secret


---------------
References
---------------


---------------
License
---------------

otp-gen is under `MIT license`_

.. _`RFC 4226`: http://tools.ietf.org/html/rfc4226
.. _`RFC 6238`: http://tools.ietf.org/html/rfc6238
.. _`MIT license`: https://opensource.org/licenses/MIT
