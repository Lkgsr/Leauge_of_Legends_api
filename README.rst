Leauge of Legends API / Database memory
=======================================

A python module for the Leauge of Legends Api which also save's the response to a Database with SQLAlchemy

Installation
------------

Using pip :

.. code:: bash

    pip install leauge_of_legends_api


or using setup.py :

.. code:: bash

    git clone https://github.com/Lkgsr/LeaugeOfLegendsApi.git
    cd LeaugeOfLegendsApi
    python setup.py install

Configure the Api Key
------------------------
To use the API from Leauge of Legends you need an APIKey. It is not that difficulty to get one.

1. You need an account for the game Leauge of Legends, which you can create here:
    (This is the url for the euw server if you want not a account for euw you have to change it on the website)

    - https://signup.euw.leagueoflegends.com/de/signup/index#/

    If you have all ready an account you just got to:

    - https://developer.riotgames.com/

    and sign in

2. If you signed in, just create yourself a Development API Key.
    confirm the Captcha and click REGENERATE API KEY

3. Now you can test you Key with the test.py file.
    Open the file in your editor of choice and replace the String "Place here your api key"
    with your actual API Key.
    *(Config file is coming soon)*

.. code:: python

    header = ["Place here your api key"]
now you ready to use the module


Usage
=====

Summoner
--------

.. code:: python

    from leauge_of_legends_api import Summoner
    Summoner.insert_to_db_by_summoner_name(header, summoner_name, update_summoner=True, just_add=False)

Inserting a summoner by his summoner name to the Database. ``header`` is a list of  Strings, which are your API Keys.
The String ``summonername`` is the summoner name which you like to save, ``update_summoner=True`` let's you control
to update or not update the summoner if he is all ready in the Database. The ``just_add=False/True`` If it's ``True``
it id added to the transaction queue (it is a mode for more performance where you have tomake the commit manually with
``Summoner.commit()``), If it's ``False`` it's added and commited at once (if you want to save many summoners it is
really slow) There are two more inserting methods, ``Summoner.insert_to_db_by_account_id`` and
``Summoner.insert_to_db_by_summoner_id`` both take the same arguments like the first one the only think which changes
is the ``summoner_name`` is now the ``account_id`` or ``summoner_id``. All three methods return a Summoner object.

There are just two more methods for the ``Summoner`` class right now:

.. code:: python

    Summoner.update_summoner_in_db(header)

This method updates all Summoners in the Database and returns every one. so you have to run it in a for loop :

.. code:: python

    for summoner in Summoner.update_all_in_db(header):
        print(summoner.name)

The last method returns a list with all your ``Summoner``'s  from you Database:

.. code:: python

    Summoner.get_all()

Test
====

Use the test.py file, add your Api key in the ``header`` variable. Now you can use the the called functions under the
``if __name__ == "__main__":``

.. code:: python

    Summoner.insert_to_db_by_summonername(header, "Place Your Summoner Name")
    update_data_base(update_leauger=True, update_masterys=True)
    Item.insert_all_to_db(header)
    Champion.insert_all_champion_to_db(header)

Where it says "Place Your Summoner Name" place the summoner name you want to save in the Database. The first method
inserts the summoner, the second one ``update_data_base()`` goes through every summoner in your Database and updates the
profile, inserts and updates the ``ChampionMastery``, the Leauge of Legend ELO with ``LeaugeOfLegendLeauger`` and the
match-history with ``Match`` and for every match it inserts the complete match history with the stats and everything
``CompleteMatch``

Coming Soon
===========

There are all ready more Classes like ``LeaugeOfLegendLeauger``, ``ChampionMastery``, ``Match``, ``Champion``,
``CompleteMatch``, ``Item`` the complete description is coming soon for all of these.