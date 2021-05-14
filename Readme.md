### **Python Rest CRUD API using Flask micro web framework**

We will build Rest Apis that can create, retrieve, update, delete and find Posts by title.

The following table shows overview of the Rest APIs that will be exported

| Methods | Urls | Actions |
|--|--|--| 
| GET | api/posts/all | Get all Posts |
| GET | api/posts/:id| Get post by `id`|
| POST |api/posts/create| Create new post |
| PUT |api/posts/update/:id| Update post by `id` |
| DELETE |api/posts/delete/:id| Delete post by `id` |
| DELETE |api/posts/deleteall| Delete all posts| . 
| GET |api/posts/published| Get all published posts| 
| GET |api/posts?title=’test’| Get all posts which titlecontains `'test'`|
| GET |api/posts/publisher?name=’christos’| Get All posts where publisher name is  `'christos'`|

Rename sample.evn to .env

**Sample .evn configuration**
__________________________________

* MYSQL_USER=user
* MYSQL_PASSWORD=pass
* MYSQL_DB=restapi
* MYSQL_HOST=127.0.0.1
* MYSQL_PORT=3306
* JWT_SECRET_KEY=Your secret key
* FLASK_APP = app.py
* FLASK_ENV = development
* FLASK_DEBUG = 1
