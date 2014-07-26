T1 Client Library
=================

**WIP** Python implementation of a T1 API Library. This library consists of Python classes for working with T1 entities. This library is written for Python 2.7. I have tried to ensure compatibility with 3.x, but this is not guaranteed and should be used at your own risk.

The best way to use this package is to instantiate the `T1` class, and do everything through there. That way, the only thing you have to import is T1 (`import terminalone` or `from terminalone import T1`), then instantiate the class (`t1 = terminalone.T1(username, password, api_key, [auth_method], [environment])`).
```python
>>> from terminalone import T1
>>> t1 = T1('myusername', 'mypassword', 'my_api_key')
>>> t1.authenticate('cookie') # 'cookie' and 'basic' currently supported
```

Authenticating upon instantiation is done by using the auth_method keyword:
```python
>>> t1 = T1('myusername', 'mypassword', 'my_api_key', auth_method='basic')
```

Environment can be "production" or "sandbox", defaulting to production:
```python
>>> t1 = T1('myusername', 'mypassword', 'my_api_key', environment='sandbox')
```

Please note that until your API key is approved to be used in production, you should use environment='sandbox' when instantiating T1.

A specific entity can be retrieved by using the `get` method from `T1`:
```python
>>> my_advertiser = t1.get('advertisers', 111111)
```

You can then access that entity's properties using either instance attributes or the dict `properties`:
```python
>>> my_advertiser.id
111111
>>> my_advertiser.properties['id']
111111
```

Once you have your instance, you can modify its values, and then save it back:
```python
>>> my_advertiser.name = 'Updated name'
>>> my_advertiser.save()
ok
```

Create new entities my calling the `new` method on your T1 instance:
```python
>>> new_creative = t1.new('campaign')
>>> # OR
>>> new_creative = t1.new('campaigns')
```

Why don't we import the object classes directly? For instance, why doesn't this work?
```python
>>> from terminalone import T1Campaign
```

The answer here is that we need to keep a common session so that we can share session information across requests. This allows you to work with many objects, only passing in authentication information once.
```python
>>> t1 = T1('myusername', 'mypassword', 'my_api_key')
>>> t1.authenticate('cookie')
>>> c = t1.new('campaign')
>>> c.session is t1.session
True
```

Common use cases:


API Documentation can be found at https://kb.mediamath.com/wiki/display/APID/API+Documentation+Home.
