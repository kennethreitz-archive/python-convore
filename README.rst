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

        >>> from convore.client import ConvoreClient
	>>> convore = ConvoreClient('username', 'password')
	
	>>> groups = convore.groups()
        >>> groups
	[<ConvoreGroup ...]
	
	>>> topics = groups[0].topics()
	>>> topics
	[<ConvoreTopic ...]
	>>> len(topics)
	14

	>>> messages = topics[0].messages()
	>>> messages
	[<ConvoreMessage ...]


	>>> new_topic = groups[0].topics.create(name="New Topic")
	>>> new_topic
	<ConvoreTopic New Topic, ...

	>>> new_topic.messages.create(message="The first message")
	>>> new_topic.messages.create(message="The 2nd one")
	>>> len(new_topic.messages())
	2

	>>> convore.groups['292']
        <ConvoreGroup 674,Python,...
	
	>>> convore.groups.create(name, decription=None, slug=None)
	(group creation doesn't work at this moment..)
	


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
