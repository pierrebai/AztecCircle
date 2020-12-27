After listening to the artic circle theorem on the Mathologer you-tube channel, I decided to write
a small Python program to generate such diagrams.

This first crude version only outputs a text representation of the resulting diagram. I may
improve it in the future to add a Qt front-end to have animated drawings instead.

For now, here how it looks:

   ```
                                        +-------+
                                        | B   B |
                                    +---------------+
                                    | B   B | B   B |
                                +-----------------------+
                                | B   B | B   B | B   B |
                            +-------------------------------+
                            | B   B | B   B | B   B | B   B |
                        +---------------------------+-------+---+
                        | B   B | B   B | B   B | Y | G   G | R |
                    +-------------------+-------|   |-------|   |---+
                    | B   B | B   B | Y | R | Y | Y | B   B | R | R |
                +---+-------+-------|   |   |   |---------------|   |---+
                | Y | G   G | G   G | Y | R | Y | B   B | B   B | R | R |
            +---|   |-------+-------+---+-------+---------------+---|   |---+
            | Y | Y | B   B | B   B | Y | G   G | R | B   B | Y | R | R | R |
        +---|   |---+-------+-------|   |-------|   |-------|   |   |---|   |---+
        | Y | Y | Y | G   G | G   G | Y | B   B | R | G   G | Y | R | R | R | R |
    +---|   |---|   |-------------------+-------+-----------+---+---|   |---|   |---+
    | Y | Y | Y | Y | Y | G   G | G   G | G   G | G   G | R | Y | R | R | R | R | R |
    |   |---|   |---|   |-------+-----------------------|   |   |   |---|   |---|   |
    | Y | Y | Y | Y | Y | Y | R | Y | G   G | G   G | R | R | Y | R | R | R | R | R |
    +---|   |---|   |---|   |   |   |-------+-------|   |---+-------|   |---|   |---+
        | Y | Y | Y | Y | Y | R | Y | B   B | B   B | R | R | B   B | R | R | R |    
        +---|   |---|   |---+---+---+-------+-----------|   |-------+---|   |---+
            | Y | Y | Y | Y | R | Y | G   G | R | B   B | R | G   G | R | R |
            +---|   |---|   |   |   |-------|   |-------+-----------|   |---+
                | Y | Y | Y | R | Y | B   B | R | G   G | G   G | R | R |
                +---|   |---+-------+-------+-------------------|   |---+
                    | Y | Y | G   G | G   G | G   G | G   G | R | R |
                    +---|   |-------+-------+---------------|   |---+
                        | Y | Y | R | B   B | Y | G   G | R | R |
                        +---|   |   |-------|   |-------|   |---+
                            | Y | R | G   G | Y | Y | R | R |
                            +---+---------------|   |   |---+
                                | G   G | G   G | Y | R |
                                +-------------------+---+
                                    | G   G | G   G |
                                    +---------------+
                                        | G   G |
                                        +-------+
   ```