import pickle
#Pickle helps is a Python module that allows you to save (serialize) Python objects to a file and load (deserialize) them back into a program later

# Initializing the chessboard variable
# The unicodes translate to chess piece visuals when run
chess_board = [["\u265C","\u265E","\u265D","\u265A","\u265B", "\u265D","\u265E", "\u265C"],
    ["\u265F","\u265F","\u265F","\u265F","\u265F","\u265F","\u265F","\u265F" ],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    ["\u2659","\u2659","\u2659","\u2659","\u2659","\u2659","\u2659","\u2659"],
    ["\u2656","\u2658","\u2657","\u2655","\u2654", "\u2657","\u2658", "\u2656"]]

eliminated_pieces = []
white_pieces = ["\u2656","\u2658","\u2657","\u2655","\u2654", "\u2657","\u2658", "\u2656", "\u2659"]
black_pieces = ["\u265C","\u265E","\u265D","\u265A","\u265B", "\u265D","\u265E", "\u265C", "\u265F"]

num_rows = num_cols = 8

# Function to save the game state
def save_game(filename):
    game_state = {
        'chess_board': chess_board,
        'eliminated_pieces': eliminated_pieces,
        'player_turn': player_turn
    }
    with open(filename, 'wb') as file:
        pickle.dump(game_state, file) # Pickle was used to save the objects into the file
    print("Game saved successfully.")

# Function to load the game state
def load_game(filename):
    global chess_board, eliminated_pieces, player_turn
    with open(filename, 'rb') as file:
        game_state = pickle.load(file) #Pickle was used to load the objects rom the file
    chess_board = game_state['chess_board']
    eliminated_pieces = game_state['eliminated_pieces']
    player_turn = game_state['player_turn']
    print("Game loaded successfully.")

# This defines the chessboard
def print_game_board():
    for row in range(num_rows):
        # This creates the top border of the chessboard
        print(f"\n+---+---+---+---+---+---+---+---+")
        # This places | as a barrier in between each row
        print("|", end="")
        for col in range(num_cols):
            # This places | as a barrier in between each column
            print("", chess_board[row][col], end=(" |"))
            # This creates the bottom border of the chessboard
    print("\n+---+---+---+---+---+---+---+---+")


def get_input():
    # This gets the user's move in the format e2 e4 and then removes the whitespace 
    
    move = input("Enter your move.  (Enter 'save' to save the game, 'load' to load the game): ")
    if move.lower() == 'save':
        save_game('chess_game_save.pkl')
        return None, None
    elif move.lower() == 'load':
        load_game('chess_game_save.pkl')
        return None, None
    
    if len(move) == 5 and move[2] == " ":
        move = move.strip()
        # Then splits the input into two with the beginning part being the "start" and the second part being the "end"
        start, end = move.split()

        if start[0] in "abcdefgh" and start[1] in "12345678" and end[0] in "abcdefgh" and end[1] in "12345678":
            # This serves as a key to make it easier to interpret the alphabets from the input into its row and column-wise location
            chessmap = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

            # This defines the initial position and the final position

            # For the initial position, the total number of rows is 8 so the, the initial row is the (8 - second part of the text saved as "start") and the initial row is the first part of the "start"
            # For the final position, the total number of rows is 8 so the, the final row is the (8 - second part of the text saved as "end") and the final column is the first part of the "end"
            # This is because the rows are labelled with numbers which constitute the second part of the "start" and the columns are labelled with alphabets which constitute the first part of the "start"
            
            int_position = ((8 - int(start[1])), chessmap[start[0]])
            fin_position = ((8 - int(end[1])), chessmap[end[0]])
            return int_position, fin_position
            
    else:
        while True:
            print("Invalid input. Try again.\nHint: Follow the labels. Valid format: [e2 e4]")
            move = input("Enter your move (or 'save' to save the game, 'load' to load the game): ")
            if move.lower() == 'save':
                save_game('chess_game_save.pkl')
                return None, None
            elif move.lower() == 'load':
                load_game('chess_game_save.pkl')
                return None, None
            
            if len(move) == 5 and move[2] == " ":
                move = move.strip()
                start, end = move.split()
                if start[0] in "abcdefgh" and start[1] in "12345678" and end[0] in "abcdefgh" and end[1] in "12345678":
                    chessmap = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
                    int_position = ((8 - int(start[1])), chessmap[start[0]])
                    fin_position = ((8 - int(end[1])), chessmap[end[0]])
                    return int_position, fin_position
    

    
    return None, None

def player_move(int_position, fin_position):
    if validate_move(int_position, fin_position):
        int_row, int_column = int_position
        fin_row, fin_column = fin_position
        piece = chess_board[int_row][int_column]

        # Checks if destination has a piece already filling the space which is not the same color as the moving piece and if so, allows that piece to be captured by the new piece
        if chess_board[fin_row][fin_column] != " " and mistaken_elimination(int_position, fin_position) == True:
            # The following then adds the captured piece to a list called "Eliminated_pieces"
            eliminated_pieces.append(chess_board[fin_row][fin_column])
        
        if mistaken_elimination(int_position, fin_position) == True:
            #this checks if it's a players turn to play and restricts movement of pieces of a different colour. If it's white's turn, black pieces won't move
            if player_turn == 0:
                if piece in black_pieces:
                    print("It is white's move. Move a white piece.")
                    return False
                else:
                    #if piece is not a different colour from the player's turn, then it moves the piece to the inputted destination
                    chess_board[int_row][int_column] = " "
                    chess_board[fin_row][fin_column] = piece
                    return True
            elif player_turn == 1:
                if piece in white_pieces:
                    print("It is black's move. Move a black piece")
                    return False       
                else:
                    chess_board[int_row][int_column] = " "
                    chess_board[fin_row][fin_column] = piece 
                    return True
        return False

# Checks if there is a same color piece in the destination of a piece and if so, prevents capturing or movement
def mistaken_elimination(int_position, fin_position):
    int_row, int_column = int_position
    fin_row, fin_column = fin_position
    piece = chess_board[int_row][int_column]

    if piece in white_pieces and chess_board[fin_row][fin_column] in white_pieces:
        return False
    elif piece in black_pieces and chess_board[fin_row][fin_column] in black_pieces:
        return False
    else:
        return True

# This code checks if the move of a pawn piece is valid or not
def allow_pawn(int_position, fin_position):
    int_row, int_column = int_position
    fin_row, fin_column = fin_position
    piece = chess_board[int_row][int_column]

    # If piece is the white pawn
    if piece == "\u2659":
        # If piece is in the 6th row, travelling to the 4th row, travelling along the same column, no piece between its initial position and final position, no piece in final position 
        if int_row == 6 and fin_row == 4 and int_column == fin_column and chess_board[5][int_column] == " " and chess_board[4][int_column] == " ":
            return True 
        # If destination is in a row 1 above its current row, piece is travelling along the same column and the final position holds no piece already
        elif fin_row == int_row - 1 and int_column == fin_column and chess_board[fin_row][fin_column] == " ":
            return True
        # If destination is in a row 1 above the piece's current row, destination column is to the right of the initial column and there is a piece in the final destination
        elif fin_row == int_row - 1 and fin_column - int_column == -1 and chess_board[fin_row][fin_column] != white_pieces:
            return True
        # If destination is in a row 1 above the piece's current row, destination column is to the left of the initial column and there is a piece in the final destination
        elif fin_row == int_row - 1 and fin_column - int_column == 1 and chess_board[fin_row][fin_column] != white_pieces:
            return True
    # If piece is the black pawn
    if piece == "\u265F":
        # If piece is in the 7th row, travelling to the 5th row, travelling along the same column, no piece between its initial position and final position, no piece in final position
        if int_row == 1 and fin_row == 3 and int_column == fin_column and chess_board[2][int_column] == " " and chess_board[3][int_column] == " ":
            return True
        # If piece is in a row 1 less than its current row, the piece is travelling along the same column and the final position holds no piece already
        elif fin_row == int_row + 1 and int_column == fin_column and chess_board[fin_row][fin_column] == " ":
            return True
        # If destination is in a row 1 less than piece's current row, destination column is to the right of the initial column and there is a piece in the final destination
        elif fin_row == int_row + 1 and fin_column - int_column == -1 and chess_board[fin_row][fin_column] != black_pieces:
            return True
        # If destination is in a row 1 less than piece's current row, destination column is to the left of the initial column and there is a piece in the final destination
        elif fin_row == int_row + 1 and fin_column - int_column == 1 and chess_board[fin_row][fin_column] != black_pieces:
            return True      
    
        return False

    # Checks if destination does not have one of the player's own pieces to prevent player from capturing himself
    mistaken_elimination(int_position, fin_position)
        
    
# This code checks if the move of a knight is valid or not
def allow_knight(int_position, fin_position):
    int_row, int_column = int_position
    fin_row, fin_column = fin_position
    piece = chess_board[int_row][int_column]

    # If piece is white knight
    if piece == "\u2658":
        # If destination is 2 rows below current row and to the right
        if fin_row == int_row - 2 and fin_column - int_column == -1 and chess_board[fin_row][fin_column] != white_pieces:
            return True
        # If destination is 2 rows below current row and to the left
        elif fin_row == int_row - 2 and fin_column - int_column == 1 and chess_board[fin_row][fin_column] != white_pieces:
            return True
        # If destination is 2 rows above current row and to the right
        elif fin_row == int_row + 2 and fin_column - int_column == -1 and chess_board[fin_row][fin_column] != white_pieces:
            return True
        # If destination is 2 rows above current row and to the left
        elif fin_row == int_row + 2 and fin_column - int_column == 1 and chess_board[fin_row][fin_column] != white_pieces:
            return True
        # If destination is 2 columns to the left and one row below
        elif fin_row == int_row - 1 and fin_column == int_column - 2 and chess_board[fin_row][fin_column] != white_pieces:
            return True
        # If destination is 2 columns to the right and one row below
        elif fin_row == int_row - 1 and fin_column == int_column + 2 and chess_board[fin_row][fin_column] != white_pieces:
            return True
        # If destination is 2 columns to the right and one row above
        elif fin_row == int_row + 1 and fin_column == int_column - 2 and chess_board[fin_row][fin_column] != white_pieces:
            return True
        # If destination is 2 columns to the left and one row above
        elif fin_row == int_row + 1 and fin_column == int_column + 2 and chess_board[fin_row][fin_column] != white_pieces:
            return True
        
    # If piece is black knight
    if piece == "\u265E":
        # If piece is 2 rows below current row and to the right
        if fin_row == int_row - 2 and fin_column - int_column == -1 and chess_board[fin_row][fin_column] != black_pieces:
            return True
        # If piece is 2 rows below current row and to the left
        elif fin_row == int_row - 2 and fin_column - int_column == 1 and chess_board[fin_row][fin_column] != black_pieces:
            return True
        # If piece is 2 rows above current row and to the right
        elif fin_row == int_row + 2 and fin_column - int_column == -1 and chess_board[fin_row][fin_column] != black_pieces:
            return True
        # If piece is 2 rows above current row and to the left
        elif fin_row == int_row + 2 and fin_column - int_column == 1 and chess_board[fin_row][fin_column] != black_pieces:
            return True    
        # If destination is 2 columns to the left and one row below
        elif fin_row == int_row - 1 and fin_column == int_column - 2 and chess_board[fin_row][fin_column] != black_pieces:
            return True
        # If destination is 2 columns to the right and one row below
        elif fin_row == int_row - 1 and fin_column == int_column + 2 and chess_board[fin_row][fin_column] != black_pieces:
            return True
        # If destination is 2 columns to the right and one row above
        elif fin_row == int_row + 1 and fin_column == int_column - 2 and chess_board[fin_row][fin_column] != black_pieces:
            return True
        # If destination is 2 columns to the left and one row above
        elif fin_row == int_row + 1 and fin_column == int_column + 2 and chess_board[fin_row][fin_column] != black_pieces:
            return True

        return False

    # Checks if destination does not have one of the player's own pieces to prevent player from capturing himself
    mistaken_elimination(int_position, fin_position)

# This code checks if the move of a rook is correct or not
def allow_rook(int_position, fin_position):
    int_row, int_column = int_position
    fin_row, fin_column = fin_position
    piece = chess_board[int_row][int_column]

    # This checks if the piece being moved is indeed a rook
    if piece == "\u2656" or "\u265C":
        # Checks if the rook is moving along the same row it is in already (if it is moving horizontally)
        if int_row == fin_row:
            # Checks if the rook is moving to the right
            if int_column < fin_column:
                # Checks if the path is clear by checking if the column right after the current column up to the last column moving forward is empty for movement
                for columns in range(int_column + 1, fin_column + 1, 1):
                    if chess_board[int_row][columns] != " ":
                        return False
            
            # Checks if the rook is moving to the left
            elif int_column > fin_column:
                # Checks if the path is clear by checking if the column right after the current column up to the last column moving backward is empty for movement
                for columns in range(int_column - 1, fin_column, -1):
                    if chess_board[fin_row][columns] != " ":
                        return False

        # This checks if the rook is moving along the same column (if it is moving vertically)
        elif int_column == fin_column:
            # Checks if the rook is moving up
            if int_row < fin_row:
                # Checks if the path is clear by checking if the row after the current row up to the final row moving up is empty for movement
                for rows in range(int_row + 1, fin_row, 1 ):
                    if chess_board[rows][int_column] != " ":
                        return False
            # Checks if the rook is moving down
            elif int_row > fin_row:
                # Checks if the path is clear by checking if the row after the current row up to the final row moving down is empty for movement
                for rows in range(int_row - 1, fin_row , -1):
                    if chess_board[rows][fin_column] != " ":
                        return False
        return True
    
    # Checks if destination does not have one of the player's own pieces to prevent player from capturing himself
    mistaken_elimination(int_position, fin_position)

# This checks if the move of a bishop is valid or not
def allow_bishop(int_position, fin_position):
    int_row, int_column = int_position
    fin_row, fin_column = fin_position
    piece = chess_board[int_row][int_column]

    # This checks if the piece is a white bishop
    if piece == "\u2657":
        # Checks if the destination's steps to the right or left vertically, is the same number as to the right or left horizontally
        # It checks if the piece moves the same number of steps horizontally, as it moves vertically, which is DIAGONAL MOVEMENT
        if (fin_row - int_row == fin_column - int_column) or (fin_row - int_row == int_column - fin_column):
            # Checks if the piece is going diagonally upwards and creates an assigned variable which represents a step
            if fin_row > int_row:
                row_count = 1
            # Checks if the piece is going diagonally downwards and creates an assigned variable which represents a step           
            elif fin_row < int_row:
                row_count = -1
            
            # Checks if the piece is going diagonally to the right and creates an assigned variable which represents a step
            if fin_column > int_column:
                column_count = 1
            # Checks if the piece is going diagonally to the left and creates an assigned variable which represents a step
            elif fin_column < int_column:
                column_count = -1

            # Adds the step to the current row coordinate to move up or down row-wise
            row_path = int_row + row_count
            # Adds the step to the current row coordinate to move forward or backward column-wise
            column_path = int_column + column_count

            # After adding the steps, we basically view the coordinate and check if it is empty
            # Using the while loop, we do this for the whole path until we reach the final destination coordinates 
            # If the path is not empty, then the piece cannot travel to the destination
            while row_path != fin_row and column_path != fin_column:
                if chess_board[row_path][column_path] != " ":
                    return False
                # While the viewing coordinate is empty, we move onto the next coordinate by adding a step until we reach the final destination
                row_path = row_path + row_count
                column_path = column_path + column_count
            return True

    # We do the same thing here for the black bishop
    if piece == "\u265D":
        if (fin_row - int_row == fin_column - int_column) or (fin_row - int_row == int_column - fin_column):
            if fin_row > int_row:
                row_count = 1
            elif fin_row < int_row:
                row_count = -1
            
            if fin_column > int_column:
                column_count = 1
            elif fin_column < int_column:
                column_count = -1

            row_path = int_row + row_count
            column_path = int_column + column_count

            while row_path != fin_row and column_path != fin_column:
                if chess_board[row_path][column_path] != " ":
                    return False
                row_path = row_path + row_count
                column_path = column_path + column_count
            return True
    
    # Checks if destination does not have one of the player's own pieces to prevent player from capturing himself
    mistaken_elimination(int_position, fin_position)

# Checks if a move by a queen piece is valid or not
def allow_queen(int_position, fin_position):
    int_row, int_column = int_position
    fin_row, fin_column = fin_position
    piece = chess_board[int_row][int_column]

    # Checks if piece is a white queen
    if piece == "\u2655":
        # Since the queen's moves are a combination of the rook and the bishop, we validate queen piece moves by checking if it is a valid rook move or valid bishop move
        if allow_rook(int_position, fin_position) or allow_bishop(int_position, fin_position) == True:
            return True
    # Checks if piece is a black queen
    if piece == "\u265B":
        # Same validation as used for the white queen
        if allow_rook(int_position, fin_position) or allow_bishop(int_position, fin_position) == True:
            return True
        return False
    
    # Checks if destination does not have one of the player's own pieces to prevent player from capturing himself
    mistaken_elimination(int_position, fin_position)

# Checks if the move of a king piece is valid or not
def allow_king(int_position, fin_position):
    int_row, int_column = int_position
    fin_row, fin_column = fin_position
    piece = chess_board[int_row][int_column]

    # Checks if piece is a white king
    if piece == "\u2654":
        # Checks if king is moving along the same row(moving horizontally) and moving one space to any side and there are no white pieces in its destination
        if fin_row == int_row and abs(fin_column - int_column) == 1 and chess_board[fin_row][fin_column] != white_pieces:
            return True
        # Checks if king is moving along the same column(moving vertically) and moving one space up or down and there are no white pieces in its destination
        elif fin_column == int_column and abs(fin_row - int_row) == 1 and chess_board[fin_row][fin_column] != white_pieces:
            return True
        # Checks if king is moving up to the right and there are no white pieces in the destination
        elif fin_column == int_column + 1 and fin_row == int_row + 1 and chess_board[fin_row][fin_column] != white_pieces:
            return True
        # Checks if king is moving up to the left and there are no white pieces in the destination
        elif fin_column == int_column - 1 and fin_row == int_row + 1 and chess_board[fin_row][fin_column] != white_pieces:
            return True
        # Checks if king is moving down to the left and there are no white pieces in the destination
        elif fin_column == int_column - 1 and fin_row == int_row - 1 and chess_board[fin_row][fin_column] != white_pieces:
            return True
        # Checks if king is moving down to the right and there are no white pieces in the destination
        elif fin_column == int_column + 1 and fin_row == int_row - 1 and chess_board[fin_row][fin_column] != white_pieces:
            return True

    # Checks if piece is a black king
    if piece == "\u265A":
        # Checks if king is moving along the same row(moving horizontally) and moving one space to any side and there are no black pieces in its destination
        if fin_row == int_row and abs(fin_column - int_column) == 1 and chess_board[fin_row][fin_column] != black_pieces:
            return True
        # Checks if king is moving along the same column(moving vertically) and moving one space up or down and there are no black pieces in its destination        
        elif fin_column == int_column and abs(fin_row - int_row) == 1 and chess_board[fin_row][fin_column] != black_pieces:
            return True
        # Checks if king is moving up to the right and there are no black pieces in the destination        
        elif fin_column == int_column + 1 and fin_row == int_row + 1 and chess_board[fin_row][fin_column] != black_pieces:
            return True
        # Checks if king is moving up to the left and there are no black pieces in the destination
        elif fin_column == int_column - 1 and fin_row == int_row + 1 and chess_board[fin_row][fin_column] != black_pieces:
            return True
        # Checks if king is moving down to the left and there are no black pieces in the destination        
        elif fin_column == int_column - 1 and fin_row == int_row - 1 and chess_board[fin_row][fin_column] != black_pieces:
            return True
        # Checks if king is moving down to the right and there are no black pieces in the destination
        elif fin_column == int_column + 1 and fin_row == int_row - 1 and chess_board[fin_row][fin_column] != black_pieces:
            return True
        return False

# This validates the moves of the different pieces
def validate_move(int_position, fin_position):
    int_row, int_column = int_position
    fin_row, fin_column = fin_position
    piece = chess_board[int_row][int_column]

    # If piece is a pawn, it runs the allow_pawn function
    if piece in ("\u2659", "\u265F"):
        return allow_pawn(int_position, fin_position)
    # If piece is a knight, it runs the allow_knight function
    elif piece in ("\u2658","\u265E"):
        return allow_knight(int_position, fin_position)
    # If piece is a rook, it runs the allow_rook function
    elif piece in ("\u2656", "\u265C"):
        return allow_rook(int_position, fin_position)
    # If piece is a bishop, it runs the allow_bishop function
    elif piece in ("\u2657", "\u265D"):
        return allow_bishop(int_position, fin_position)
    # If piece is a queen, it runs the allow_queen function
    elif piece in ("\u2655", "\u265B"):
        return allow_queen(int_position, fin_position)
    # If piece is a king, it runs the allow_king function
    elif piece in ( "\u2654", "\u265A"):
        return allow_king(int_position, fin_position)
    return False

players = ["White", "Black"]
player_turn = 0

while True:
    print_game_board()
    print("Eliminated pieces:", eliminated_pieces)
    print(f"{players[player_turn]}'s move")
    

    int_position, fin_position = get_input()
    

    if player_move(int_position, fin_position) == True:
        player_turn = (player_turn + 1) % 2
    



    if "\u265A" in eliminated_pieces:
        print("Game Over!! White Wins!!!")
        break
    elif "\u2654" in eliminated_pieces:
        print("Game Over!! Black Wins !!!")
        break