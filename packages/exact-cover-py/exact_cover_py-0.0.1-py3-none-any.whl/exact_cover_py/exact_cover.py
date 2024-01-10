"""
Donald Knuth's Algorithm X implemented in Python.
"""

from dataclasses import dataclass

import numpy as np

@dataclass(slots=True)
class Node:
    """
    Node in a doubly-linked list.
    """
    left: 'Node'
    right: 'Node'
    up: 'Node'
    down: 'Node'
    # point to relative column header, also referred to as col_node
    # None for the col headers themselves
    col: 'Node'
    # row index for the non-header nodes
    # -1 for the header nodes
    row: int
    # the S heuristic
    sum: int = 0

    def __repr__(self):
        # root node
        if self.down is None:
            return "root"
        # a header node
        if self.col is None:
            return f"header [S={self.sum}]"
        else:
            return f"{self.row}x{self.col.row}"

    def insert_horizontally_after(self, where):
        """
        attach self to the right of where
        if where is None, self gets the single node in its row
        """
        if where is None:
            self.left = self
            self.right = self
        else:
            self.right = where.right
            self.left = where
            where.right.left = self
            where.right = self

    def insert_vertically_after(self, where):
        """
        attach self below where
        if where is None, self gets the single node in its column
        """
        if where is None:
            self.up = self
            self.down = self
        else:
            self.down = where.down
            self.up = where
            where.down.up = self
            where.down = self

    def cover_horizontally(self):
        """
        remove self from the row
        """
        if self.right is self:
            return
        self.right.left = self.left
        self.left.right = self.right

    def uncover_horizontally(self):
        """
        reinsert self into the row
        """
        self.right.left = self
        self.left.right = self

    def cover_vertically(self):
        """
        remove self from the column
        """
        if self.down is self:
            return
        self.down.up = self.up
        self.up.down = self.down

    def uncover_vertically(self):
        """
        reinsert self into the column
        """
        self.down.up = self
        self.up.down = self

    def cover_column(self):
        """
        remove the column from the matrix
        self is expected to be a column header
        """
        self.cover_horizontally()
        # iterating on the rows below the header
        nodei = self.down
        while nodei is not self:
            # iterating on the columns of the row
            nodej = nodei.right
            while nodej is not nodei:
                nodej.cover_vertically()
                nodej.col.sum -= 1
                nodej = nodej.right
            nodei = nodei.down

    def uncover_column(self):
        """
        reinsert the column into the matrix
        self is expected to be a column header
        """
        # iterating on the rows above the header
        nodei = self.up
        while nodei is not self:
            # iterating on the columns of the row
            nodej = nodei.left
            while nodej is not nodei:
                nodej.uncover_vertically()
                nodej.col.sum += 1
                nodej = nodej.left
            nodei = nodei.up
        self.uncover_horizontally()


@dataclass
class Matrix:
    """
    the sparse matrix that models a problem instance
    """
    root: Node

    def reverse(self):
        """
        reconstruct the input matrix for debugging
        """
        nodej = self.root.right
        ones = set()
        col_index = 0
        while nodej is not self.root:
            nodei = nodej.down
            while nodei is not nodej:
                ones.add((nodei.row, nodei.col.row))
                nodei = nodei.down
            nodej = nodej.right
            col_index += 1

        rows, cols = (max(ones, key=lambda x: x[0])[0],
                      max(ones, key=lambda x: x[1])[1])

        loop = np.zeros((rows+1, cols+1), dtype=np.uint8)
        for row, col in ones:
            loop[row, col] = True
        # outline empty rows and columns
        empty_rows = [i for i in range(rows+1)
                      if not np.any(loop[i])]
        empty_cols = [j for j in range(cols+1)
                        if not np.any(loop[:, j])]
        for i in empty_rows:
            loop[i] = 2
        for j in empty_cols:
            loop[:, j] = 2
        return loop

    @staticmethod
    def from_numpy(array: np.ndarray) -> 'Matrix':
        """
        Create a matrix from a numpy array.
        """
        # create the colomn headers
        _, width = array.shape
        root = nav = Node(None, None, None, None, None, -1)
        root.right = root.left = root
        # for direct access to the column headers
        column_headers = []
        for col_index in range(width):
            col_node = Node(None, None, None, None, None, col_index)
            col_node.insert_horizontally_after(nav)
            col_node.down = col_node.up = col_node
            nav = col_node
            column_headers.append(col_node)
        nav.right = root
        # fill the matrix
        for row_index, row in enumerate(array):
            where_in_row = None
            for col_index, (col_node, value) in enumerate(
                zip(column_headers, row)):
                if value:
                    node = Node(None, None, None, None, col_node, row_index)
                    # connect horizontally
                    node.insert_horizontally_after(where_in_row)
                    where_in_row = node
                    # connect vertically
                    where_in_column = column_headers[col_index].up
                    node.insert_vertically_after(where_in_column)
                    # update header's sum
                    col_node.sum += 1

        return Matrix(root)

    def optimal_column(self):
        """
        return the column header with the smallest sum
        """
        node = self.root.right
        min_sum = node.sum
        min_node = node
        while node is not self.root:
            if node.sum < min_sum:
                min_sum = node.sum
                min_node = node
            node = node.right
        return min_node

    def search(self, k=0):
        """
        a generator that yields all solutions
        """
        h = self.root
        if h.right is h:
            yield []
        else:
            # use the S heuristic
            c = self.optimal_column()
            c.cover_column()
            r = c.down
            while r is not c:
                solution = [r.row]
                j = r.right
                while j is not r:
                    j.col.cover_column()
                    j = j.right
                for s in self.search(k+1):
                    yield solution + s
                j = r.left
                while j is not r:
                    j.col.uncover_column()
                    j = j.left
                r = r.down
            c.uncover_column()

def exact_covers(array: np.ndarray):
    """
    a generator that yields all solutions
    """
    matrix = Matrix.from_numpy(array)
    yield from matrix.search()
