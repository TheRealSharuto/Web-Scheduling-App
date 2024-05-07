For my teammates.
You must do the following to run this web application:

1. Open terminal
2. copy/paste: ``pip install mysql-connector`` or ``pip install mysql-connector-python`` for windows (I am using mac so I can not confirm this).
3. have python3 installed
4. Review all imports and make sure they are installed on your computer
5. to render css everyone needs to run: 
```npx tailwindcss -i ./static/src/css/input.css -o ./static/src/css/output.css --watch```

For css to be seen, everyone needs to run

```python3 app.py```
 . Css will not render when opening a singular html page


 VERSION 2 FOR PROFESSOR INSTRUCTIONS-- CHOP THIS AND ABOVE LINES IF YOU APPROVE THESE INSTRUCTIONS

Instructions for Professor Munoz:

You must do the following to run this web application in your IDE:

1. Open terminal
2. copy/paste: ``pip install mysql-connector`` or ``pip install mysql-connector-python``
3. Ensure python3 installed
4. Review all imports pip calls out, and make sure they are installed on your computer.
5. To enable css rendering: 

In a terminal, run command ```npx tailwindcss -i ./static/src/css/input.css -o ./static/src/css/output.css --watch```

Leave this batch operation running.

In a second terminal instance, run

```python3 app.py```

ctrl-click on the localhost port 5000 link that appears.
