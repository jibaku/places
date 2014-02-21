Managers
========

.. method:: PlaceManager.for_site()
	
	Return the places related to the current site or the site whom ID is passed
	as the site_id parameter.

.. method:: PlaceManager.public()

	Return the public places (by default for the current website, or for the
	site whose ID is passed as *site_id* parameter)

.. method:: PlaceManager.for_user()

	Return the places for the user passed as parameter. It's the public places
	and the user private places.
