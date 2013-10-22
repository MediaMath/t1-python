T1ClientLibrary-Python
================

**WIP** Python implementation of a T1 API Library. This library consists of Python classes for working with T1 entities. This library is written for Python 2.7. I have tried to ensure compatibility with 3.x, but this is not guaranteed and should be used at your own risk.

The best way to use this class is to initiate the `T1Service` class, and do everything through there. That way, the only thing you have to import is T1Service (`from t1apicore import t1service` or `from t1apicore.t1service import T1Service`), then instantiate the class (`t1 = t1service.T1Service(username, password, apikey, environment)` or `t1 = T1Service(username, password, apikey, environment)`, respectively).

A specific entity can be retrieved by using the `get` method from `T1Service`:
```python
>>> from t1apicore.t1service import T1Service
>>> t1 = T1Service(username, password, apikey, environment)
>>> my_advertiser = t1.get('advertisers', 111111)
```
You can then access that entity's properties using either instance attributes, the dict `properties`, or even accessing it like a dict itself:
```python
>>> my_advertiser.id
111111
>>> my_advertiser.properties['id']
111111
>>> my_advertiser['id']
111111
>>>
```

Once you have your instance, you can modify its values, and then save it back:
```python
>>> my_advertiser.name = 'Updated name'
>>> my_advertiser.save()
ok
>>>
```

Create new entities my calling the `new` method on your T1Service instance:
```python
>>> # Proper
>>> new_creative = t1.new('atomic_creatives')
>>> # OR
>>> new_creative = t1.new('atomic_creative')
>>> # OR
>>> new_creative = t1.new_atomic_creative()
>>>
```

API Documentation can be found at https://kb.mediamath.com/wiki/display/APID/API+Documentation+Home.
