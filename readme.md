After learning about the aztec artic circle theorem on the Mathologer YouTube channel,
I decided to write a small Python program to generate such diagrams.

There are multiple versions of the program:

- ```main.py```: runs on the command-line that outputs a text representation of the resulting diagram.
- ```main_qt.py```: runs in a Qt application to draw the diagram and gives more control on the output.
- ```main_record.py```: outputs all actions applied to the diagram, one per line.
- ```main_replay.py```: reads the actions from its standard input and re-outputs them again.
- ```main_replay_qt.py```: reads the actions from its standard input and draws the resulting diagram.

For the command-line version, all you need is a recent Python interpreter. I used Python 3.7.8, but
the most recent one, 3.9.1 should work too.

For the Qt version, you will need to install the required dependencies. Here are some instructions
explaining what and how to install what is needed:

- Python 3.7+: download and install from https://www.python.org/downloads/
- Clone the git repository: enter the command ```git clone https://github.com/pierrebai/AztecCircle.git```
- pipenv: isolate Python dependencies in a virtual environment: enter the command ```pip install pipenv```
- Qt libraries: enter the command ```pipenv install```
- Run the program: enter the command ```pipenv run python main_qt.py```

Here is how the Qt version looks:

![User Interface](https://github.com/pierrebai/AztecCircle/blob/master/Aztec-Circle-Qt.png "User Interface")

Here is how the output from the command-line version looks:

    ```
                                +-------+
                                | B   B |
                            +---+---+---+---+
                            | B   B | B   B |
                        +---+---+---+---+---+---+
                        | B   B | B   B | B   B |
                    +---+---+---+---+---+-------+---+
                    | B   B | B   B | Y | G   G | R |
                +---+-------+-------+   +-------+   +---+
                | Y | G   G | G   G | Y | B   B | R | R |
            +---+   +---+---+---+---+---+---+---+---+   +---+
            | Y | Y | Y | R | Y | G   G | R | B   B | R | R |
        +---+   +---+   |   |   +---+---+   +---+---+---+   +
        | Y | Y | Y | Y | R | Y | Y | R | R | R | Y | R | R |
        |   +---+   +---+---+---+   |   +---+   |   |   +---+
        | Y | Y | Y | Y | G   G | Y | R | R | R | Y | R | R |
        +---+   +---+   +---+---+---+---+   +---+---+---+   +
            | Y | Y | Y | Y | R | Y | R | R | G   G | R | R |
            +---+   +---+   |   |   |   +---+---+---+   +---+
                | Y | Y | Y | R | Y | R | G   G | R | R |
                +---+   +---+---+---+---+---+---+   +---+
                    | Y | Y | G   G | R | Y | R | R |
                    +---+   +---+---+   |   |   +---+
                        | Y | Y | R | R | Y | R |
                        +---+   |   +---+---+---+
                            | Y | R | G   G |
                            +---+---+---+---+
    ```