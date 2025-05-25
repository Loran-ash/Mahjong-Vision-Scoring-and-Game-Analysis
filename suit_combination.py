from functools import lru_cache
from copy import deepcopy

# 快取結果避免重複計算
suit_cache = {}

def suit_to_str(suit, is_honour):
    if is_honour:
        count = [0, 0, 0, 0]
        for tile in suit:
            if tile > 0:
                count[tile - 1] += 1
        return '0' + ''.join(str(c) for c in count)
    else:
        return ''.join(str(x) if x > 0 else ' ' for x in suit).strip()

def cal_optimal_suit_combination(suit_input, is_honour=False):
    suit_str = suit_to_str(suit_input, is_honour)
    if suit_str in suit_cache:
        return suit_cache[suit_str]

    suit = list(suit_input)
    residuals = []
    groups = 0
    taatsus = 0
    pairs = 0
    max_groups = 0
    max_taatsus = 0
    max_taatsus_with_pair = 0

    def suit_len(s):
        return sum(s)

    def remove_groups(i=0):
        nonlocal groups, max_groups, residuals, suit
        if groups > max_groups:
            max_groups = groups
            residuals = []
        if groups == max_groups:
            residuals.append(deepcopy(suit))

        if i >= len(suit):
            return

        while i < len(suit) and suit[i] == 0:
            i += 1
        if i >= len(suit):
            return

        # Triplet
        if suit[i] >= 3:
            groups += 1
            suit[i] -= 3
            remove_groups(i)
            suit[i] += 3
            groups -= 1

        # Sequence
        if not is_honour and i <= len(suit) - 3 and suit[i+1] > 0 and suit[i+2] > 0:
            groups += 1
            suit[i] -= 1
            suit[i+1] -= 1
            suit[i+2] -= 1
            remove_groups(i)
            suit[i] += 1
            suit[i+1] += 1
            suit[i+2] += 1
            groups -= 1

        remove_groups(i + 1)

    def remove_taatsus(i=0):
        nonlocal taatsus, pairs, max_taatsus, max_taatsus_with_pair, suit

        if taatsus > max_taatsus:
            max_taatsus = taatsus
        if pairs > 0 and taatsus > max_taatsus_with_pair:
            max_taatsus_with_pair = taatsus

        if i >= len(suit):
            return

        while i < len(suit) and suit[i] == 0:
            i += 1
        if i >= len(suit):
            return

        # Pair
        if suit[i] >= 2:
            taatsus += 1
            pairs += 1
            suit[i] -= 2
            remove_taatsus(i)
            suit[i] += 2
            taatsus -= 1
            pairs -= 1

        # Protoruns
        if not is_honour:
            if i <= len(suit) - 2 and suit[i+1] > 0:
                taatsus += 1
                suit[i] -= 1
                suit[i+1] -= 1
                remove_taatsus(i)
                suit[i] += 1
                suit[i+1] += 1
                taatsus -= 1
            if i <= len(suit) - 3 and suit[i+2] > 0:
                taatsus += 1
                suit[i] -= 1
                suit[i+2] -= 1
                remove_taatsus(i)
                suit[i] += 1
                suit[i+2] += 1
                taatsus -= 1

        remove_taatsus(i + 1)

    remove_groups()

    for residual in residuals:
        suit = list(residual)
        taatsus = 0
        pairs = 0
        remove_taatsus()
        if suit_len(suit) <= 1 and pairs > 0:
            break

    result = (max_groups, max_taatsus, max_taatsus_with_pair)
    suit_cache[suit_str] = result
    return result
