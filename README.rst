.. image:: https://badge.fury.io/py/otp-py.svg
    :target: https://badge.fury.io/py/otp-py

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
The way to install otp-gen is to use `pip`_

.. code:: bash

    $ pip3 install otp-gen

---------------
Getting Started
---------------

You need to provision the secret key, issuer and rest of the details with the ``config`` command. Default values are shown if any.

.. image:: img/demo-provisioning.gif
    :align: center

---------------
Usage
---------------

You can request a new OTP with the ``get`` command. A progress bar appears next to the code to indicate expiry period of it. ``get`` continuously provides valid codes until killed.

Current configuration can be embedded in a QR code by using ``qrcode`` command.

.. image:: img/demo.gif
    :align: center

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

