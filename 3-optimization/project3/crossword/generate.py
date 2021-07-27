import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
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
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        
        # Loop through the variable’s domain
        for v in self.crossword.variables:

            # Loop through the word domain
            for word in self.crossword.words:

                # If the length of the word does not equal variable
                # Remove it from the domain
                if len(word) != v.length:
                    self.domains[v].remove(word)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        revision = False

        # Get overlap (if exists) and create a copy of domain
        overlap = self.crossword.overlaps[x, y]
        domain = copy.deepcopy(self.domains)

        # Check if the overlap exists, if no then returns False by default
        if overlap:

            # Get cells that overlap
            char_x, char_y = overlap

            # Loop through X domain
            for word_x in domain[x]:

                match = False
                # Loop through Y domain
                for word_y in self.domains[y]:

                    # If X and Y have the same letter - ensure match
                    if word_x[char_x] == word_y[char_y]:
                        match = True
                        break

                # If we achieve a match then we move on the next X
                if match:
                    continue

                # If no match then we remove the X from the domain
                # And flag that a revision has been made
                else:
                    self.domains[x].remove(word_x)
                    revision = True

        return revision


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # Check if arcs exists
        if not arcs:

            # If no arcs exist create the initial arc
            arcs_list = []
            for v1 in self.crossword.variables:
                for v2 in self.crossword.neighbors(v1):
                    arcs_list.append((v1, v2))

        # Loop through the arcs
        while arcs_list:

            # Get list item
            x, y = arcs_list.pop(0)

            # Check revision status
            if self.revise(x, y):

                # If no domains remain afther the check return False
                if len(self.domains[x]) == 0:
                    return False

                # Move onto next
                for n in self.crossword.neighbors(x):
                    if n != y:
                        arcs_list.append((n, x))

        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # Loop through all of the variables in the domain
        # And check if they also exist in the assignment
        for v in self.domains:
            if v not in assignment:
                return False
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # We loop through the variables and check for inconsistencies
        # If no inconsistencies are found the function defaults to True at the end
        for x in assignment:

            # Extract the word and check if its length is the same as the assignments
            # If not return False
            word_x = assignment[x]
            if x.length != len(word_x):
                return False

            # Loop through other assignment variables
            for y in assignment:

                # Extract the word and compare if its the same assignment
                word_y = assignment[y]
                if x != y:

                    # Check if both of the words are not the same
                    # If they are return False
                    if word_x == word_y:
                        return False

                    # Check if both of the words overlap
                    overlap = self.crossword.overlaps[x, y]
                    if overlap:

                        # If they do overlap - check if they overlap over the same character
                        char_x, char_y = overlap
                        if word_x[char_x] != word_y[char_y]:
                            return False
        
        # If nothing else has failed up until this point
        # Exit with True
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # Get the set of all neighbors for var
        # Then get the unassigned neighbors
        neighbors = self.crossword.neighbors(var)
        for n in assignment:
            if n in neighbors:
                neighbors.remove(n)

        # Create a dict to store results of eliminations
        eliminations = {v: 0 for v in self.domains[var]}

        # Loop through all of the variables in the domain
        for v in self.domains[var]:

            # Then through the unassigned neighbors
            for n in neighbors:

                # Check the status of overlap
                char_x, char_y = self.crossword.overlaps[var, n]

                # Then go through each word in neighbors domain
                for v_n in self.domains[n]:

                    # And increase results in eliminations if the overlaps do not correspond
                    if v[char_x] != v_n[char_y]:
                        eliminations[v] += 1
        
        # From eliminations create a list of results by sorting the dictionary
        return [x[0] for x in sorted(eliminations.items(), key = lambda x: x[1])]


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # Get the unassigned variables
        variables = []
        for var in self.crossword.variables:
            if var not in assignment:

                # And retrieve the number of remaining values and degrees
                variables.append([var, len(self.domains[var]), len(self.crossword.neighbors(var))])

        # Sort the list with both remaining values and degrees
        # If there is no tie then the first value will be the one with minimum number of remaining values
        # If there is a tie then the first value will be with the highest degree
        variables.sort(key=lambda x: (x[1], -x[2]))
        return variables[0][0]


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # Check if the assignment is complete
        # If so return the assignment
        if self.assignment_complete(assignment):
            return assignment

        else:

            # Otherwise get the unassigned variable and loop through the domain
            var = self.select_unassigned_variable(assignment)
            for v in self.order_domain_values(var, assignment):

                # Copy the assignment and assign the new variable
                assignment_new = assignment.copy()
                assignment_new[var] = v

                # Check if the new assignment is consistent
                if self.consistent(assignment_new) and self.backtrack(assignment_new):
                    return self.backtrack(assignment_new)

            # If all fails return None
            return None


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
