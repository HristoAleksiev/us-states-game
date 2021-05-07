from turtle import Turtle, Screen
import pandas

NUMBER_OF_STATES = 50
scr = Screen()
scr.title("U.S States")
image = "blank_states_img.gif"
scr.addshape(image)
scr.tracer(0)

tur = Turtle()
tur.shape(image)

writer = Turtle()
writer.hideturtle()
writer.penup()

is_game_over = False
player_score = 0
correct_guesses = []
missed_states = []

db_states = pandas.read_csv("50_states.csv")
state_from_db = db_states.state.to_list()


def check_answer(user_guess):
    """
    Checks if the guessed state exists in the database and if it has been guessed already.
    Returns all information about the state for further operations in the program.
    """

    if user_guess in state_from_db:
        if user_guess not in correct_guesses:
            correct_guesses.append(user_guess)
            return db_states[db_states.state == user_guess].values.tolist()
    else:
        return False


def export_missed_states():
    """
    At the end of the game, exports all the states that have not been guessed to a file named "missed_states.csv"
    in the same directory as the project.
    """
    global missed_states
    for state in state_from_db:
        if state not in correct_guesses:
            missed_states.append(state)

    csv_data = pandas.DataFrame(missed_states)
    csv_data.columns = ["State"]
    csv_data.to_csv("missed_states.csv")


while not is_game_over:
    scr.update()

    user_input = scr.textinput(title=f"{player_score}/{NUMBER_OF_STATES} States Found",
                               prompt="Guess the name of a State")
    if user_input is None:
        is_game_over = True
        export_missed_states()
        break
    else:
        state_data = check_answer(user_input.title())
        if state_data:
            writer.goto(x=state_data[0][1], y=state_data[0][2])
            writer.write(arg=state_data[0][0])
            player_score += 1

        # If the player guesses all the states correctly, nothing happens. :D
        if player_score == NUMBER_OF_STATES:
            is_game_over = True
