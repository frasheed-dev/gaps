import numpy as np
import helpers

from solver.fitness import dissimilarity_measure

class Individual:
    """Class representing possible solution to puzzle.

    Individual object is one of the solutions to the problem (possible arrangement of the puzzle's pieces).
    It is created by random shuffling initial puzzle.

    :param pieces:  Array of pieces representing initial puzzle.
    :param rows:    Number of rows in input puzzle
    :param columns: Number of columns in input puzzle

    Usage::

        >>> from models import Individual
        >>> ind = Individual(pieces, 10, 15)

    """

    def __init__(self, pieces, rows, columns, shuffle=True):
        self.pieces  = pieces[:]
        self.rows    = rows
        self.columns = columns
        self.fitness = None

        if shuffle:
            np.random.shuffle(self.pieces)

        # Map piece ID to index in Individual's list
        self.piece_mapping = {piece.id: index for index, piece in enumerate(self.pieces)}

    def __getitem__(self, key):
        return self.pieces[key * self.columns : (key + 1) * self.columns]

    def piece_size(self):
        """Returns single piece size"""
        return self.pieces[0].size

    def piece_by_id(self, identifier):
        return self.pieces[self.piece_mapping[identifier]]

    def to_image(self):
        """Converts individual to showable image"""
        pieces = [piece.image for piece in self.pieces]
        return helpers.assemble_image(pieces, self.rows, self.columns)

    def edge(self, piece, orientation):
        edge_index = self.piece_mapping[piece]

        if (orientation == "T") and (edge_index >= self.columns):
            return self.pieces[edge_index - self.columns].id

        if (orientation == "R") and (edge_index % self.columns < self.columns - 1):
            return self.pieces[edge_index + 1].id

        if (orientation == "D") and (edge_index < (self.rows - 1) * self.columns):
            return self.pieces[edge_index + self.columns].id

        if (orientation == "L") and (edge_index % self.columns > 0):
            return self.pieces[edge_index - 1].id

    def contains_edge(self, src, dst, orientation):
        edges = [edge for edge in self.edges(src) if edge[1] == dst and edge[2] == orientation]
        return len(edges) > 0

class Piece:
    """Represents single jigsaw puzzle piece.

    Each piece has identifier so it can be
    tracked accross different individuals

    :param value: ndarray representing piece's RGB values
    :param index: Unique id withing piece's parent image

    Usage::

        >>> from models import Piece
        >>> piece = Piece(image[:28, :28, :], 42)

    """

    def __init__(self, image, index):
        self.image = image[:]
        self.id    = index

    def __getitem__(self, index):
        return self.image.__getitem__(index)

    def size(self):
        """Returns piece size"""
        return self.image.shape[0]

    def shape(self):
        """Retursn shape of piece's image"""
        return self.image.shape