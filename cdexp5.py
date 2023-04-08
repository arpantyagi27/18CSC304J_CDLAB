from collections import defaultdict

def compute_first_follow(grammar):
    first = defaultdict(set)
    follow = defaultdict(set)

    # Compute FIRST sets
    def compute_first(symbol):
        if symbol in first:
            return first[symbol]
        for production in grammar[symbol]:
            for i, symbol_i in enumerate(production):
                if symbol_i not in grammar:
                    first[symbol].add(symbol_i)
                    break
                else:
                    compute_first_i = compute_first(symbol_i)
                    first[symbol].update(compute_first_i - {'epsilon'})
                    if 'epsilon' not in compute_first_i:
                        break
            else:
                first[symbol].add('epsilon')
        return first[symbol]

    # Compute FOLLOW sets
    def compute_follow(symbol):
        if symbol in follow:
            return follow[symbol]
        if symbol == next(iter(grammar)):
            follow[symbol].add('$')
        for left, right in grammar.items():
            for production in right:
                if symbol in production:
                    i = production.index(symbol)
                    if i < len(production) - 1:
                        compute_first_i = compute_first(production[i+1])
                        follow[symbol].update(compute_first_i - {'epsilon'})
                    if i == len(production) - 1 or 'epsilon' in compute_first(production[i+1]):
                        follow[symbol].update(compute_follow(left))
        return follow[symbol]

    # Compute FIRST and FOLLOW sets for all non-terminals
    for symbol in grammar:
        compute_first(symbol)
        compute_follow(symbol)

    return {'FIRST': dict(first), 'FOLLOW': dict(follow)}

# Example usage
grammar = {
    'S': ['ABC', 'BC', 'A'],
    'A': ['a', 'epsilon'],
    'B': ['b', 'epsilon'],
    'C': ['c']
}

result = compute_first_follow(grammar)
print(result)
