## First stage:

Create abstract base model that will be base for all another models:
- create_date
- update_date

Create model `Product`:
- name
- description
- active
- image


Create model `Item`:
- name
- active
- price
- metadata: JSONField


Implement cart functionality - use one of the libraries (https://github.com/lazybird/django-carton) or (https://github.com/bmentges/django-cart)

Implement wishlist  functionality - use one of library above (if it supports it) or implement your own solution.

Create class-based views for:
- list all products
- product detail page
- adding/removing/list item to/from/in cart
- adding/removing/list item to/from/in wishlist

