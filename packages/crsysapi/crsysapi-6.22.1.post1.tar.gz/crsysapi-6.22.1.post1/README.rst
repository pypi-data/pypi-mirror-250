Python for CryptoSys API
===================================

This is a Python interface to the **CryptoSys API** library <https://www.cryptosys.net/api.html>. 

CryptoSys API is a library to carry out "symmetrical" encryption using block ciphers like AES and Triple DES; 
stream ciphers ArcFour, Salsa and ChaCha20; Authenticated Encryption with Additional Data (AEAD);
message authentication algorithms HMAC, CMAC and KMAC; 
hash functions SHA-1, SHA-2 and SHA-3; the PBKDF2 and SCRYPT key derivation functions; and more. 

Requires: Python 3.
CryptoSys API v6.22.1 or above must be installed on your system.
This is available from

    https://www.cryptosys.net/api.html.


To use in Python's REPL
-----------------------

Using wild import for simplicity.

.. code-block:: python

    >>> from crsysapi import *  # @UnusedWildImport
    >>> Gen.version() # "hello world!" for CryptoSys API
    62201
    >>> Hash.hex_from_data(b'abc') # compute SHA-1 hash in hex of 'abc' as bytes
    'a9993e364706816aba3e25717850c26c9cd0d89d'
    >>> Hash.hex_from_string('abc', Hash.Alg.SHA256)   # same but over a string and using SHA-256
    'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
    >>> h = Hash.data(b'abc')   # h is a byte array (bytes->bytes)
    >>> print(Cnv.tohex(h))     # display the byte array in hex
    A9993E364706816ABA3E25717850C26C9CD0D89D

The stricter way using the ``crsysapi`` prefix.

.. code-block:: python

    >>> import crsysapi
    >>> crsysapi.Gen.version() # Underlying core CryptoSys API dll
    62201
    >>> crsysapi.__version__  # crsysapi.py module version
    6.22.1.0000
    >>> crsysapi.Hash.hex_from_data(b'abc') # compute SHA-1 hash in hex of 'abc' as bytes
    'a9993e364706816aba3e25717850c26c9cd0d89d'
    >>> crsysapi.Hash.hex_from_string('abc', crsysapi.Hash.Alg.SHA256)   # same but over a string and using SHA-256
    'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
    >>> h = crsysapi.Hash.data(b'abc')   # h is a byte array (bytes->bytes)
    >>> print(crsysapi.Cnv.tohex(h))     # display the byte array in hex
    A9993E364706816ABA3E25717850C26C9CD0D89D

Note that ``crsysapi.Gen.version()`` gives the version number of the underlying core (native) CryptoSys API DLL, 
and ``crsysapi.__version__`` gives the version of the Python crsysapi module. 

Examples
--------

There is a series of tests in ``test_crsysapi.py`` (`source <https://www.cryptosys.net/test_crsysapi.py.html>`_). 
This creates any required test files automatically.
You should find an example there of what you want to do.


post1 Update
------------

2023-01-08: Updated distribution to use pyproject.toml and build instead of setup.py, and removed troublesome and unnecessary requirements file
(which messed up pytest).


Contact
-------

For more information or to make suggestions, please contact us at
https://www.cryptosys.net/contact/

| David Ireland
| DI Management Services Pty Ltd
| Australia
| <https://www.di-mgt.com.au> <https://www.cryptosys.net>
| 8 January 2024
