## First Stage:

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

## Second Stage:

Create model `Order`:
- total_price
- total_items_count
- status: CharField with choices: 'WAITING', 'SUCCESS', 'ERROR'
- items: M2M to `Item` through `OrderItem`
- metadata: JSONField

Create model `OrderItem`:
- order: ForeignKey to `Order`
- item: ForeignKey to `Item`
- quantity: IntegerField
- total_price: DoubleField

Add `quantity` field for `Item` model.

Create class-based views for:
- creating order and payment

Setup payment system Stripe.
Make sure that this is not possible to order more items that is present in Item.quantity :)
