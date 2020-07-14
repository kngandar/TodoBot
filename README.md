# TodoBot
Custom todo discord bot written in python.

It will keep track of todos which will award exp to users when completed.

Users can be assigned prizes that will be awarded when they reach a certain amount of exp.

Users can also use emotes to mark a todo as done, mark a prize as done or delete either a todo or prize from their respective list.




### Commands
- !add-todos: Adds todo to user's list
</br>&nbsp;&nbsp;&nbsp;e.g: !add-todos "Laundry (2), Cook dinner (4)"
- !add-prizes: Adds prizes to user's list
</br>&nbsp;&nbsp;&nbsp;e.g: !add-prizes "Order sushi (10), A steam game in your wishlist (20)"
  
- !stats: Checks exp of user

- !8ball: For fun 8-ball command

### Emotes
- tododone: Moves todo from todo channel to done-todo
- prizedone: Moves prizes from prize-list channel to done-prize-list
- deleteitem: Deletes todo from todo channel / Deletes prizes from prize-list channel




## Setup
1. Ensure you have the python libraries in app.py

2. Put own server token in TOKEN variable in app.py

2. Add custom emotes with the following names:
  tododone, prizedone, deleteitem
  
3. Add text channels with the following names:
  todo, done-todo, prize-list, done-prize-list
  
4. Run program, and the bot will go online
