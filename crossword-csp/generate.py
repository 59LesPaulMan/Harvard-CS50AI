import sys

from crossword import *


class CrosswordCreator:

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())
    
    # The following functions were rearranged by Kevin Via on 6-26-25 to follow logical order.
    # main will call the solve function above, solve called enforce_node_consistency, ac3 and then backtrack
    # The following are unary - enforce_node_consistency, binary revise and ac3
    # backtrack then uses selected_unassigned_variable, order_domain_values, Consistent, and finally 
    # assignment_complete.

    # Methods below reordered for logical readability and to reflect execution flow of the CSP solver.
    # Refactored on 6-26-25 by Kevin Via.

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.domains:  # all variables in self.domains
            not_length = set()  # set for not_length variables
            for word in self.domains[variable]:
                if len(word) != variable.length:
                    not_length.add(word)  # not length - add to set
            self.domains[variable] -= not_length  # remove set from self.domains

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Set a queue for all x,y in self.neighbors and y in crossword
        if arcs is None:
            queue = [(x, y) for x in self.domains for y in self.crossword.neighbors(x)]
        else:
            queue = list(arcs)  # queue is a list (arcs)

        while queue:
            x, y = queue.pop(0)  # FIFO queue type

            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                # Establish neighbors of x that are not y of variable z
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.append((z, x))
        return True

    # Methods below reordered for logical readability and to reflect execution flow of the CSP solver.
    # Refactored on 6-26-25 by Kevin Via.

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps[
            x, y
        ]  # self.overlaps within Crossword Object from crossword.py
        i, j = overlap
        revised = False
        for node_x in set(
            self.domains[x]
        ):  # create two nodes x and y based on i, j within self.crossword
            if not any(
                node_x[i] == node_y[j] for node_y in self.domains[y]
            ):  # if does not exist
                self.domains[x].remove(node_x)  # remove the node
                revised = True  # Set a revised to True to return
        return revised  # Return revised
    
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Take as input assignment and return  complete assignment
        if len(assignment) == len(self.crossword.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value

            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        return None

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = [var for var in self.crossword.variables if var not in assignment]

        def min_val(var):
            return len(self.domains[var])

        def h_degree(var):
            return sum(
                1
                for neighbor in self.crossword.neighbors(var)
                if neighbor not in assignment
            )

        unassigned.sort(key=lambda var: (min_val(var), -h_degree(var)))

        return unassigned[0]

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        constraints = {}

        for value in self.domains[var]:
            ruled_out = 0

            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    continue

                overlap = self.crossword.overlaps[var, neighbor]
                if overlap is None:
                    continue

                i, j = overlap
                for neighbor_val in self.domains[neighbor]:
                    if value[i] != neighbor_val[j]:
                        ruled_out += 1

            constraints[value] = ruled_out

        return sorted(constraints, key=constraints.get)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Unary checks length of variable
        for var, word in assignment.items():
            if len(word) != var.length:
                return False

        # Binary checks x == y
        for x in assignment:
            for y in assignment:
                if x == y:
                    continue
                overlap = self.crossword.overlaps.get((x, y))
                if overlap:
                    i, j = overlap
                    if assignment[x][i] != assignment[y][j]:
                        return False

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.crossword.variables:
            if (
                variable not in assignment or assignment[variable] is None
            ):  # variable (word) is not in assignment or None
                return False
        return True


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
