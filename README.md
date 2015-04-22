TerminalOne-Python
==================

**WIP** Python library for MediaMath's APIs. This library consists of classes for working with T1 APIs and managing entities. It is written for Python 2.7 and >=3.3. Compatibility with Python 3 is made possible by bundling the module [six](https://pypi.python.org/pypi/six).

API Documentation is availble at [https://developer.mediamath.com/docs/TerminalOne_API_Overview](https://developer.mediamath.com/docs/TerminalOne_API_Overview).

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
	- [Service Object](#service-object)
	- [Fetching Entities and Collections](#fetching-entities-and-collections)
		- [Collections](#collections)
		- [Entities](#entities)
		- [Searching for entities](#searching-for-entities)
		- [Appendix](#appendix)
- [Contact](#contact)
- [Copyright](#copyright)


## Installation

Installation is simple with pip in a virtual environment:

```bash
$ pip install --extra-index-url=https://code.mediamath.com/pypi/simple/ TerminalOne
```

The `--extra-index-url` flag specifies a package index URL; this is where the code is hosted. Alternatively, download the latest tag of the repository as a tarball or zip file and run:

```bash
$ python setup.py install
```

## Usage

### Service Object

*class* `terminalone.T1`(*username*=`None`, *password*=`None`, *api_key*=`None`, *auth_method*=`None`, *session_id*=`None`, *environment*=`"production"`, *api_base*=`None`)

The `T1` class is the starting point for this package. This is where authentication and session, entity retrieval, creation, etc. are handled.

- *username* and *password* correspond to credentials for a T1 user.
- *api_key* is an approved API key generated at [MediaMath's Developer Portal](https://developer.mediamath.com).
- *session_id* is for applications receiving a session ID instead of user credentials, such as an app. In this case *api_key* should still be provided.
- *auth_method* is a string corresponding to which method of authentication the session to use. Currently only "cookie" has full support, while "basic" is supported with Execution and Management API.
- Either *environment* or *api_base* should be provided to specify where the request goes.

```python
>>> import terminalone
>>> t1 = terminalone.T1("myusername", "mypassword", "my_api_key", auth_method="cookie")
```

Using `auth_method` authenticates upon instantiation. Authentication can also be done separately by calling the `authenticate` method with the same acceptable arguments as the keyword:

```python
>>> t1 = terminalone.T1("myusername", "mypassword", "my_api_key")
>>> t1.authenticate("cookie")
```

Environment can be "production" or "qa", defaulting to production:

```python
>>> t1 = terminalone.T1("myusername", "mypassword", "my_api_key", auth_method="cookie", environment="qa")
```

If you have a specific API base (for instance, if you are testing against a local deployment) you can use the `api_base` keyword:

```python
>>> t1 = terminalone.T1("myusername", "mypassword", "my_api_key", api_base="https://myqaserver.domain.com/api/v2.0", auth_method="cookie")
```

If you are receiving a (cloned) session ID, for instance the norm for apps, you will not have user credentials to log in with. Instead, provide the session ID and API key:

```python
>>> t1 = terminalone.T1(session_id="13ea5a26e77b64e7361c7ef84910c18a8d952cf0", api_key="my_api_key")
```

### Fetching Entities and Collections

Use `get` for entity and collection retrieval:

`T1.get`(*collection*, *entity*=`None`, *child*=`None`, *limit*=`None`, *include*=`None`, *full*=`None`, *page_limit*=`100`, *page_offset*=`0`, *sort_by*=`"id"`, *get_all*=`False`, *query*=`None`, *count*=`False`)

- *collection*: T1 collection, e.g. `"advertisers"`
- *entity*: Integer ID of entity being retrieved from T1
- *child*: Child object of a particular entity, e.g. `"dma"`, `"acl"`
- *limit*: dict to query for relation entity, e.g. `{"advertiser": 123456}`
- *include*: str/list of relations to include, e.g. `"advertiser"`, `["campaign", "advertiser"]`
- *full*: When retrieving multiple entities, specifies which types to return the full record for. e.g.
	- `"campaign"` (full record for campaign entities returned)
	- `True` (full record of all entities returned),
	- `["campaign", "advertiser"]` (full record for campaigns and advertisers returned)
- *page_limit* and *page_offset* handle pagination. *page_limit* specifies how many entities to return at a time, default and max of 100. *page_offset* specifies which entity to start at for that page.
- *sort_by*: sort order. Default `"id"`. e.g. `"-id"`, `"name"`
- *get_all*: Whether to retrieve all results for a query or just a single page. Mutually exclusive with *page_limit*/*page_offset*
- *query*: Search parameters. *Note*: it's much simpler to use `find` instead of `get`, allowing `find` to construct the query.
- *count*: bool return the number of entities as a second parameter
- *raise* `terminalone.errors.ClientError` if *page_limit* > 100, `terminalone.errors.APIError` on >399 HTTP status code
- *return*: If single entity is specified, returns a single entity object. If multiple entities, generator yielding each entity.

#### Collections

```python
>>> advertisers = t1.get("advertisers")
>>> for advertiser in advertisers:
...     print(advertiser)
...
Advertiser(id=1, name="My Brand Advertiser", _type="advertiser")
...
```

Returns generator over the first 100 advertisers (or fewer if the user only has access to fewer), ordered ascending by ID. Each entity is the limited object, containing just `id`, `name`, and `_type` (`_type` just signifies the type returned by the API, in this case, "advertiser").

```python
>>> ag_advertisers = t1.get("advertisers",
...                         limit={"agency": 123456},
...                         include="agency",
...                         full="advertiser")
>>> for advertiser in ag_advertisers:
...     print(advertiser)
...
Advertiser(id=1, name="My Brand Advertiser", agency=Agency(id=123456, name="Operating Agency", _type="agency"), agency_id=123456, status=True, ...)
...
```

Generator over up to 100 advertisers within agency ID 123456. Each advertiser includes its parent agency object as an attribute. The advertiser objects are the full entities, so all fields are returned. Agency objects are limited and have the same fields as advertisers in the previous example.

```python
>>> campaigns, count = t1.get("campaigns",
...                           get_all=True,
...                           full=True,
...                           sort_by="-updated_on")
>>> print(count)
539
>>> for campaign in campaigns:
...     print(campaign)
Campaign(id=123, name="Summer Acquisition", updated_on=datetime.datetime(2015, 4, 4, 0, 15, 0, 0), ...)
Campaign(id=456, name="Spring Acquisition", updated_on=datetime.datetime(2015, 4, 4, 0, 10, 0, 0), ...)
...
```

Generator over every campaign accessible by the user, sorted in descending order of last update. Second argument is integer number of campaigns retrieved, as returned by the API. `get_all=True` removes the need to worry about pagination — it is handled by the SDK internally.

```python
>>> _, count = t1.get("advertisers",
...                   page_limit=1,
...                   count=True)
>>> print(count)
23
```

Sole purpose is to get the count of advertisers accessible by the user. Use `page_limit=1` to minimize unnecessary resources, and assign to `_` to throw away the single entity retrieved.

#### Entities

A specific entity can be retrieved by using `get` with an entity ID as the second argument, or using the `entity` keyword. You can then access that entity's properties using instance attributes:

```python
>>> my_advertiser = t1.get("advertisers", 111111)
>>> my_advertiser.id
111111
```

If for some reason you need to access the object like a dictionary (for instance, if you need to iterate over fields or dump to a CSV), the dict `properties` is available. However, you shouldn't modify `properties` directly, as it bypasses validation.

Once you have your instance, you can modify its values, and then save it back. A return value of `None` indicates success. Otherwise, an error is raised.

```python
>>> my_advertiser.name = "Updated name"
>>> my_advertiser.save()
>>>
```

Create new entities my calling `T1.new` on your instance:

```python
>>> new_properties = {
...     "name": "Spring Green",
...     "status": True,
... }
>>> new_concept = t1.new("concept", properties=new_properties)
>>> new_concept.advertiser_id = 123456
>>> new_concept.save()
>>>
```

#### Searching for entities

Limiting entities by relation ID is one way to limit entities, but we can also search with more intricate queries using `find`:

`T1.find`(*collection*, *variable*, *operator*, *candidates*, ***kwargs*)

- *collection*: T1 collection, same use as with `get`
- *variable*: Field to query for, e.g. `name`
- *operator*: Arithmetic operator, e.g. `"<"`
- *candidates*: Query value, e.g. `"jonsmith*"`
- *kwargs*: Additional keyword arguments to pass onto `get`. All keyword arguments applicable for `get` are applicable here as well.

*class* `terminalone.filters`

- `IN`
- `NULL`
- `NOT_NULL`
- `EQUALS`
- `NOT_EQUALS`
- `GREATER`
- `GREATER_OR_EQUAL`
- `LESS`
- `LESS_OR_EQUAL`
- `CASE_INS_STRING`

```python
>>> greens = t1.find("atomic_creatives",
...                  "name",
...                  terminalone.filters.CASE_INS_STRING,
...                  "*Green*",
...                  include="concept",
...                  get_all=True)
```

Generator over all creatives with "Green" in the name. Include concept.

```python
>>> my_campaigns = t1.find("campaigns",
...                       "id",
...                       terminalone.filers.IN,
...                       [123, 234, 345],
...                       full=True)
```

Generator over campaign IDs 123, 234, and 345. Note that when using `terminalone.filers.IN`, *variable* is automatically ID, so that argument is effectively ignored. Further, *candidates* must be a list of integer IDs.

```python
>>> pixels = t1.find("pixel_bundles",
...                  "keywords",
...                  terminalone.filters.NOT_NULL,
...                  None)
```

Generator over first 100 pixels with non-null keywords field.

```python
>>> strats = t1.find("strategies",
...                  "status",
...                  terminalone.filters.EQUALS,
...                  True,
...                  limit={"campaign": 123456})
```

Active campaigns within campaign ID 123456.

### Fetching Reports

*class* `terminalone.Report`

`Report.metadata`

To use MediaMath's [Reports API](https://developer.mediamath.com/docs/read/reports_api), instantiate an instance with `T1.new`:

```python
>>> rpts = t1.new("report")
```

This is a metadata object, and can be used to retrieve information about which reports are available.

```python
>>> pprint.pprint(rpts.metadata)
{'reports': {...
             'geo': {'Description': 'Standard Geo Report',
                     'Name': 'Geo Report',
                     'URI_Data': 'https://api.mediamath.com/reporting/v1/std/geo',
                     'URI_Meta': 'https://api.mediamath.com/reporting/v1/std/geo/meta'},
...}
>>> pprint.pprint(rpts.metadata, depth=2)
{'reports': {'audience_index': {...},
             'audience_index_pixel': {...},
             'day_part': {...},
             'device_technology': {...},
             'geo': {...},
             'performance': {...},
             'pulse': {...},
             'reach_frequency': {...},
             'site_transparency': {...},
             'technology': {...},
             'video': {...},
             'watermark': {...}}}
```

You can retrieve the URI stub of any report by calling `Report.report_uri`:

```python
>>> print(rpts.get_uri("geo"))
'geo'
```

(Which is just a short-cut to getting the final part of the path of `Report.metadata[report]['URI_Data']`. Getting the URI from the specification is preferred to assuming that the name is the same as the stub. This is more directly applicable by instantiating the object for it:

```python
>>> report = t1.new("report", rpts.report_uri("performance"))
```

You can access metadata about this report from the `Report.metadata` property as well. To get data, first set properties about the query with `Report.set`, and use the `Report.get` method, which returns a tuple `(headers, data)`.:

```python
>>> report.set({
...     'dimensions': ['campaign_id', 'strategy_name'],
...     'filter': {'campaign_id': 126173},
...     'metrics': ['impressions', 'total_spend'],
...     'time_rollup': 'by_day',
...     'start_date': '2013-01-01',
...     'end_date': '2013-12-31',
...     'order': ['date'],
... })
>>> headers, data = report.get()
>>> print(headers)
['start_date', 'end_date', 'campaign_id', 'strategy_name', 'impressions']
>>> for line in data:
...     # do work on line
...     print(line)
...
['2013-06-27', '2013-06-27', '126173', 'PS', '231']
...
```

`headers` is a list of headers, while `data` is a csv.reader object. Type casting is not present in the current version, but is tentatively planned for a future date.

More information about these parameters can be found [here](https://developer.mediamath.com/docs/read/reports_api/Data_Retrieval).



#### Appendix
Why don't we import the object classes directly? For instance, why doesn't this work?

```python
>>> from terminalone import Campaign
```

The answer here is that we need to keep a common session so that we can share session information across requests. This allows you to work with many objects, only passing in authentication information once.

```python
>>> t1 = T1("myusername", "mypassword", "my_api_key")
>>> t1.authenticate("cookie")
>>> c = t1.new("campaign")
>>> c.session is t1.session
True
```

## Contact

For questions about either API workflow or this library, email [developers@mediamath.com](mailto:developers@mediamath.com).

## Copyright

Copyright MediaMath 2015. All rights reserved.
