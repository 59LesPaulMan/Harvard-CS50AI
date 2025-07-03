from logic import Symbol, And, Implication, model_check

A = Symbol("A")
B = Symbol("B")

knowledge = And(
    Implication(A, B),
    A
)

query = B

print(model_check(knowledge, query))  # Should return True