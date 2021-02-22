from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Implement rules of game
    # It is either Knight or Knave (OR)
    Or(AKnight, AKnave),
    # If it is Knave then it is not Knight and vice versa
    Implication(AKnight, Not(AKnave)),
    Implication(AKnave, Not(AKnight)),

    # Consider what A said
    Biconditional(AKnight, And(AKnight, AKnave)) # If I am a Knight then I am both Knight and Knave (False, I cannot be both)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Again implement rules of game but with two pairs
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Implication(AKnight, Not(AKnave)),
    Implication(AKnave, Not(AKnight)),
    Implication(BKnight, Not(BKnave)),
    Implication(BKnave, Not(BKnight)),

    # Consider what A said
    Biconditional(AKnight, And(AKnave, BKnave)) # If I am a Knight then me (A) and B are Knaves (False, because Knight cant be Knave)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Rules of game
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Implication(AKnight, Not(AKnave)),
    Implication(AKnave, Not(AKnight)),
    Implication(BKnight, Not(BKnave)),
    Implication(BKnave, Not(BKnight)),

    # Consider what A and B said
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))), # If I am a Knight then either we are both Knights or both Knaves (False, contradicts next sentence)
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))) # If I am a Knight then either one of us is knight or knave, or other is knave or knight
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Rules of game
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Implication(AKnight, Not(AKnave)),
    Implication(AKnave, Not(AKnight)),
    Implication(BKnight, Not(BKnave)),
    Implication(BKnave, Not(BKnight)),
    Implication(CKnight, Not(CKnave)),
    Implication(CKnave, Not(CKnight)),

    # Consider what A, B and C said
    Biconditional(AKnight, Or(AKnight, AKnave)), # If I am a Knight then I am either Knights or Knave
    Biconditional(BKnight, Biconditional(AKnight, AKnave)), # If I am Knight then A is a Knave
    Biconditional(BKnight, CKnave), # If I am a Knight then C is a Knave
    Biconditional(CKnight, AKnight) # If I am a Knight then A is a Knight
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
