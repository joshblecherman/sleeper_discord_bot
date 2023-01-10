# sleeper_discord_bot

## Project tree
.
 * [sleeper_api_utils](./sleeper_api_utils)
   * [sleeper_api_utils.py](./sleeper_api_utils/sleeper_api_utils.py)
   * [\_\_init\_\_.py](./sleeper_api_utils/__init__.py)
 * [db_handler](./db_handler)
   * [db_handler.py](./db_handler/db_handler.py)
   * [\_\_init\_\_.py](./db_handler/__init__.py)
 * [thicc_utils](./thicc_utils)
   * [\_\_init\_\_.py](./thicc_utils/__init__.py)
   * [thicc_utils.py](./thicc_utils/thicc_utils.py) 
 * [main.py](./main.py)
 * [state.db](./state.db)
 * [README.md](./README.md)

## Descriptions 

__sleeper_api_utils__: module responsible for communicating to the sleeper api 

__thicc_utils__: module responsible for calculating who has the largest fantasy football team, by weight 

__db_handler__: module responsible for creating and updating `state.db`. Data recieved from the sleeper API is stored in `state.db` 

__main.py__: Running process that manages the connection to the discord server  
   
