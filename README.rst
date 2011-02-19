Convore: Python API Wrapper
===========================

::

     .d8888b  .d88b.  88888b.  888  888  .d88b.  888d888  .d88b.
    d88P"    d88""88b 888 "88b 888  888 d88""88b 888P"   d8P  Y8b
    888      888  888 888  888 Y88  88P 888  888 888     88888888
    Y88b.    Y88..88P 888  888  Y8bd8P  Y88..88P 888     Y8b.
     "Y8888P  "Y88P"  888  888   Y88P    "Y88P"  888      "Y8888



Overview
--------

This is going to be awesome, and modeled after the excellent github2 module.

Usage
-----

Hmm.. ::

    >>> import convore
    >>> convore.login('username', 'password')
    
    >>> convore.account_verify()
    True

    >>> convore.groups
    [<group 'api-2'>, ...]

    >>> convore.groups['api-2']
    <group 'api-2>

    >>> convore.groups['api-2'].leave()
    True

    >>> convore.group_create(name, description=None, slug=None)
    <group 'group-name'>

    >>> convore.groups['api-2'].topics
    [<topic 'group/topic-name'>, ...]

    >>> convore.groups['api-2'].topic_create(name)
    <topic 'group/topic-name>

    >>> convore.groups['api-2'].topics[topic_id].messages
    [<message 'group/topic/'>, ...]

    >>> convore.groups['api-2'].topics[topic_id].messages.create(message)
    True
    


    convore.group_create(name, decription=None, slug=None)




Installation
------------

To install tablib, simply: ::

    $ pip install convore

Or, if you absolutely must: ::

    $ easy_install convore

But, you really shouldn't do that.

Contribute
----------

If you'd like to contribute, simply fork `the repository`_, commit your changes to the **develop** branch (or branch off of it), and send a pull request. Make sure you add yourself to AUTHORS_.


Roadmap
-------
- Documentation
- Write it!
- Test it!
- Fo shizzle

.. _`the repository`: http://github.com/kennethreitz/python-convore
.. _AUTHORS: http://github.com/kennethreitz/python-convore/blob/master/AUTHORS
