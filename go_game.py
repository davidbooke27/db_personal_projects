import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter

class Board():
    def __init__(self, size=8, black_score=0, white_score=0):
        self.size = size
        self.board_intersections = np.zeros((size + 1, size + 1))
        self.black_score = black_score
        self.white_score = white_score
        self.black_stones_array = []
        self.white_stones_array = []
        self.red_spots_array = []
        self.black_stones_plot = []
        self.white_stones_plot = []
        self.red_spots_plot = []
        self.game_quit = False

    def plot_board(self):
        fig = plt.figure()
        ax = fig.gca()
        ax.set_xlim(left=0, right=self.size)
        ax.set_ylim(bottom=0, top=self.size)
        plt.grid(True, c='k')
        ax.xaxis.set_ticks(np.arange(0, self.size + 1, 1))
        ax.yaxis.set_ticks(np.arange(0, self.size + 1, 1))
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        ax.tick_params(axis='both', which='major', pad=15)
        plt.scatter(list(map(itemgetter(0), self.black_stones_plot)), list(map(itemgetter(1), self.black_stones_plot)),
                    marker='o', c='k', s=200, clip_on=False)
        plt.scatter(list(map(itemgetter(0), self.white_stones_plot)), list(map(itemgetter(1), self.white_stones_plot)),
                    marker='o', c='w', s=200, edgecolors='k', clip_on=False)
        plt.scatter(list(map(itemgetter(0), self.red_spots_plot)), list(map(itemgetter(1), self.red_spots_plot)),
                    marker='x', c='r', s=200, linewidth=4, clip_on=False)
        plt.show()

    # Converts y_coordinate in plot to row num in 2D array
    def convert_plot_to_array_y(self, y):
        if y - self.size == 0:
            array_row = 0
        elif y == self.size / 2:
            array_row = y
        elif y == 0:
            array_row = self.size
        else:
            array_row = int(y + (-(self.size) * ((self.size / 2) - (self.size - y)) / (self.size / 2)))
        return array_row

    # Returns false if any point on board is still equal to 0 (for checking if there are any possible intersections left)
    def check_is_full(self):
        for i in range(self.size + 1):
            for j in range(self.size + 1):
                if self.board_intersections[i, j] == 0:
                    return False
        return True

    # Returns list of coordinates adjacent to given coordinate
    def get_adjacent_points(self, new_row, new_col):
        adjacent = []
        if new_row - 1 >= 0:
            adjacent.append([new_row - 1, new_col])
        if new_col - 1 >= 0:
            adjacent.append([new_row, new_col - 1])
        if new_col + 1 <= self.size:
            adjacent.append([new_row, new_col + 1])
        if new_row + 1 <= self.size:
            adjacent.append([new_row + 1, new_col])
        return adjacent

    # Returns list of coordinates that are connected to given coordinate (connected stones must be same color)
    def get_connected(self, color, x_position, y_position):
        array_y = self.convert_plot_to_array_y(y_position)
        # Black stone have value of 1 in 2D array representation of board and white stones have value of 1
        if color == 'black':
            val_check = 1
        elif color == 'white':
            val_check = 2
        # Add given coordinate to list of connected coordinates and to list of coordinates to check
        connected = [[array_y, x_position]]
        new_points = [[array_y, x_position]]
        # While there are new points to check, checks adjacent coordinates to new point to see if they have the same value
        # as the given coordinate. If they do, adds them to connected list and to new_points to check points around it as
        # well (as long as the new point isn't already in the list of connected coordinates)
        while len(new_points) > 0:
            adjacent_points = self.get_adjacent_points(new_points[0][0], new_points[0][1])
            for point in adjacent_points:
                if self.board_intersections[point[0], point[1]] == val_check and point not in connected:
                    connected.append(point)
                    new_points.append(point)
            new_points.pop(0)
        return connected

    # Returns list of coordinates around connected stones of given coordinate
    def get_border(self, color, x_position, y_position):
        if color == 'black':
            val_check = 1
        elif color == 'white':
            val_check = 2
        connected = self.get_connected(color, x_position, y_position)
        border = []
        # For each connected coordinate, checks the adjacent coordinates to see if the point isn't in the list of connected
        # coordinates, isn't already in the list of border points, and isn't occupied by a stone of the same color/value.
        # If those conditions are met, then it adds the point to the list of border coordinates
        for point in connected:
            adjacent_points = self.get_adjacent_points(point[0], point[1])
            for adj_point in adjacent_points:
                if adj_point not in connected and adj_point not in border and self.board_intersections[
                    adj_point[0], adj_point[1]] != val_check:
                    border.append(adj_point)
        return border

    # After checking to see if coordinate is already occupied, places stone at given location and adds location to
    # relevant parameters of board object
    def place_stone(self, color, x_position, y_position):
        array_y = self.convert_plot_to_array_y(y_position)
        if x_position in range(self.size + 1) and array_y in range(self.size + 1):
            if color == 'black' and [array_y, x_position] not in self.black_stones_array and [array_y,
                                                                                              x_position] not in self.white_stones_array and [
                array_y, x_position] not in self.red_spots_array:
                self.black_stones_array.append([array_y, x_position])
                self.black_stones_plot.append([x_position, y_position])
                self.board_intersections[array_y, x_position] = 1
            elif color == 'white' and [array_y, x_position] not in self.black_stones_array and [array_y,
                                                                                                x_position] not in self.white_stones_array and [
                array_y, x_position] not in self.red_spots_array:
                self.white_stones_array.append([array_y, x_position])
                self.white_stones_plot.append([x_position, y_position])
                self.board_intersections[array_y, x_position] = 2
        else:
            return 'Invalid'

    # First checks to see if given location is valid. If it is, then this method checks to see if any stones of opposite
    # color need to be removed due to placement of stone at given location
    def play_turn(self, color, x_position, y_position):
        if color == 'black':
            opp_val = 2
            opp_color = 'white'
            same_val = 1
        else:
            opp_val = 1
            opp_color = 'black'
            same_val = 2
        array_y = self.convert_plot_to_array_y(y_position)
        result = self.place_stone(color, x_position, y_position)
        if result == 'Invalid':
            return 'Invalid'
        adj_points = self.get_adjacent_points(array_y, x_position)
        points_to_check = []
        # Creates lists of points to check if the stone adjacent to the placed stone is of the opposite color
        for point in adj_points:
            if self.board_intersections[point[0], point[1]] == opp_val:
                points_to_check.append(point)
        for point in points_to_check:
            # First get the connected points and border points of stone that potentially needs to be removed
            point_y = self.convert_plot_to_array_y(point[0])
            connected_points = self.get_connected(opp_color, point[1], point_y)
            border_points = self.get_border(opp_color, point[1], point_y)
            non_opp_points = 0
            # Checks to see if all stones around connected stones are opposite color
            for point in border_points:
                if self.board_intersections[point[0], point[1]] != same_val:
                    non_opp_points += 1
            # If all stones around connected stones are opposite color, needs to remove those stones from the list of
            # stones to plot, add red spots at those points, and update the board intersections parameter to value of red spot
            if non_opp_points == 0:
                for point in connected_points:
                    if color == 'black':
                        point_y = self.convert_plot_to_array_y(point[0])
                        self.white_stones_array.remove(point)
                        self.white_stones_plot.remove([point[1], point_y])
                        self.red_spots_array.append(point)
                        self.red_spots_plot.append([point[1], point_y])
                        self.board_intersections[point[0], point[1]] = 3
                    elif color == 'white':
                        point_y = self.convert_plot_to_array_y(point[0])
                        self.black_stones_array.remove(point)
                        self.black_stones_plot.remove([point[1], point_y])
                        self.red_spots_array.append(point)
                        self.red_spots_plot.append([point[1], point_y])
                        self.board_intersections[point[0], point[1]] = 3
                # Update score since stones were removed
                if color == 'black':
                    self.black_score += len(connected_points)
                elif color == 'white':
                    self.white_score += len(connected_points)

    # Plays the game. Plots the board, takes input from the players, and keeps track of the score until the game is over
    def play_game(self):
        # Black always goes first
        color = 'black'
        # Play the game while the game hasn't been resigned and the board isn't full
        while self.game_quit == False and self.check_is_full() == False:
            if color == 'black':
                next_color = 'white'
            else:
                next_color = 'black'
            self.plot_board()
            print("Black's score: {}".format(self.black_score))
            print("White's score: {}".format(self.white_score))
            print("It is {}'s turn".format(color))
            turn_input = input(
                'Please enter coordinates separated by comma (e.g. 2, 3), "Pass" to pass turn, or "Resign" to resign game: ')
            if turn_input.lower() == 'pass':
                print('Turn passed')
                color = next_color
            elif turn_input.lower() == 'resign':
                print('Game resigned')
                print('Final Score: Black - {0}, White - {1}'.format(str(self.black_score), str(self.white_score)))
                if self.black_score > self.white_score:
                    print('Black wins!')
                elif self.white_score > self.black_score:
                    print('White wins!')
                else:
                    print("It's a tie!")
                self.game_quit = True
            else:
                trimmed = turn_input.replace(' ', '')
                trimmed_components = trimmed.split(',')
                try:
                    x_position = int(trimmed_components[0])
                    y_position = int(trimmed_components[-1])
                    result = self.play_turn(color, x_position, y_position)
                except:
                    print("Invalid input. Please try again")
                else:
                    if result == 'Invalid':
                        print("Invalid input. Please try again")
                    else:
                        color = next_color

board = Board(size=8)
board.play_game()