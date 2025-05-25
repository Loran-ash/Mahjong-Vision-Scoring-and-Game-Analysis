from suit_combination import cal_optimal_suit_combination 

def hand_length(hand):
    return sum(sum(suit) for suit in hand)

def menzu_target(hand):
    """計算標準手牌所需的面子數"""
    length = hand_length(hand)
    return length // 3

def cal_shanten_menzu(hand, target=None):
    """
    計算面子手的向聽數
    :param hand: 4個 list 組成的手牌（萬、筒、索、字）
    :param target: 預期面子數，若為 None 則自動計算
    :return: 向聽數（整數）
    """

    def menzu_formula(deficit, taatsu, pair_exists):
        if taatsu < deficit + 1:
            return 2 * deficit - taatsu
        else:
            return deficit - int(pair_exists)

    stats = [
        cal_optimal_suit_combination(hand[0], is_honour=False),  # man
        cal_optimal_suit_combination(hand[1], is_honour=False),  # pin
        cal_optimal_suit_combination(hand[2], is_honour=False),  # sou
        cal_optimal_suit_combination(hand[3], is_honour=True),   # zi
    ]  

    if target is None:
        target = menzu_target(hand)

    deficit = target - sum(stat[0] for stat in stats)
    max_taatsus = sum(stat[1] for stat in stats)

    shanten = menzu_formula(deficit, max_taatsus, pair_exists=False)

    for stat in stats:
        if stat[2] > 0:
            taatsus_with_pair = max_taatsus - stat[1] + stat[2]
            shanten_with_pair = menzu_formula(deficit, taatsus_with_pair, pair_exists=True)
            shanten = min(shanten, shanten_with_pair)

    return shanten
