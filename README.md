# This application is a Flask API end-point meant to allow searching and querying on the data.json file located in the source folder.

# Future instructions will be provided in order to run the application, including better usage if pipenv and/or a requirements.txt file, but here are the current requirements:
- Install Python (though this was built with 3.11, >3.7 should do fine)
- Install Flask (though this was built with 2.2.3, anything greater than 2 should be fine, and even older versions may work)

# Running the application
- Within this directory, run sh bootstrap.sh, which will start the Flask server
- Navigate to the /providers endpoint (i.e. http://127.0.0.1:5000/providers) which will return all providers
- Use query strings to filter the data. All top-level attributes for a provider that are primitive types are filterable. The "filter_" prefix should be used to specify the desired field filters, and multiple query strings can be specified to filter of.

For example, the below query will return all active providers that are in Ukraine.
http://127.0.0.1:5000/providers?filter_country=Ukraine&filter_active=true

No filters are automatically applied; in order to always receive active providers, specify it in the query:
http://127.0.0.1:5000/providers?filter_active=true

- Use query strings to order/sort the data. All top-level attributes for a provider that are primitive types are filterable. The "order_" prefix should be used to specify the desired ordering attribute. Ordering and filtering can be combined, but only one ordering attribute can be specified. 0 specifies that the order should happen in ascending/non-reverse order, and 1 specified that the order should happen in descending/reverse order.

No ordering is automatically applied. If an order is not specified, the default order of them in the list will be done.

For example, the below query will return all active providers ordered by rating descending.
http://127.0.0.1:5000/providers?filter_active=true&order_rating=1