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
    Or(AKnight, AKnave),  # You are one or the other Knight or Knave
    Not(
        And(AKnight, AKnave)
    ),  # Not a Knight because Knight tells the truth and you can't be both (aka - lie = Knave)
    Implication(
        AKnight, And(AKnight, AKnave)
    ),  # Implication of Knight which choice (Knight, Knave)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.

# Psuedocode - A is a Knave:
# Then statement is false = They are not both Knaves since a Knave lies.
# This means one is a Knave and one is a Knight since they are not both Knaves.
# A would have to be lying which means that A is indeed a Knave and B is a Knight.

knowledge1 = And(
    Or(AKnight, AKnave),  # A is either a Knight or Knave
    Or(BKnight, BKnave),  # B is either a Knight or a Knave
    Implication(
        AKnave, Not(And(AKnave, BKnave))
    ),  # If A is a Knave, their statement is fasle both being Knaves
    Implication(
        AKnight, And(AKnave, BKnave)
    ),  # If A is a Knight, implies A is also AKnave and B is a Knave
)

# Puzzle 2
# A says "We are the same kind.
# B says "We are of different kinds.
knowledge2 = And(
    Or(AKnight, AKnave),  # A is either a Knight or Knave
    Or(BKnight, BKnave),  # B is either a Knight or a Knave
    Implication(
        AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))
    ),  # A is a Knight
    Implication(
        AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))
    ),  # A is a Knave
    Implication(
        BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))
    ),  # B is a Knight
    Implication(
        BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight)))
    ),  # B is a Knave
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),  # A is either a Knight or a Knave
    Or(BKnight, BKnave),  # B is either a Knight or Knave
    Or(CKnight, CKnave),  # C is either a Knifht or a Knave
    # Nothing to code for "A says" statement -
    Not(BKnight),  # B - Knight cannot lie and say they are a Knave
    Implication(
        BKnave, AKnight
    ),  # B is a Knave, then Not (A said "I am a knave"), A said "I am a Knight"
    Implication(BKnight, CKnave),  # B is a Knight and says C is a Knave
    Implication(BKnave, CKnight),  # B is a Knave and C is a Knight
    Implication(CKnight, AKnight),
    Implication(CKnave, AKnave),  # C is a Knight
    # C is a Knave
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
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
