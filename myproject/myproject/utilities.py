def count_alphas(word):
    return sum([ch.isalpha() for ch in word])


def get_lettercase_permutation(word):
    """O(2^n) worst case time and space complexities"""
    result = ['']
    for ch in word:
        if ch.isalpha():
            result = [word + c for word in result for c in [ch.lower(), ch.upper()]]
        else:
            result = [word + ch for word in result]
    return result
