from tile_utils import tile_names, check_hand
from cal_shanten import cal_shanten_menzu  # 你需要實作這個函數：return cal_shanten_menzu(hand)

def ukeire_add1(hand, shanten_fn):
    """
    適用 3n+1 張的手牌：模擬摸進一張牌後是否能改善向聽數
    """
    ukeire = {}
    total_ukeire = 0
    original_shanten = shanten_fn(hand)

    for i in range(4):
        for j in range(len(hand[i])):
            remaining_count = 4 - hand[i][j]
            if remaining_count > 0:
                hand[i][j] += 1
                new_shanten = shanten_fn(hand)
                hand[i][j] -= 1
                if new_shanten < original_shanten:
                    ukeire[tile_names[i][j]] = remaining_count
                    total_ukeire += remaining_count

    return {
        "shanten": original_shanten,
        "ukeire": ukeire,
        "totalUkeire": total_ukeire
    }

def ukeire_remove1(hand, shanten_fn):
    """
    適用 3n+2 張的手牌：嘗試打出每張牌後再模擬摸牌分析受入
    """
    original_shanten = shanten_fn(hand)
    normal_discard = {}
    receding_discard = {}

    for i in range(4):
        for j in range(len(hand[i])):
            if hand[i][j] > 0:
                hand[i][j] -= 1
                result = ukeire_add1(hand, shanten_fn)
                hand[i][j] += 1
                tile = tile_names[i][j]
                if result["shanten"] > original_shanten:
                    receding_discard[tile] = result["ukeire"]
                else:
                    normal_discard[tile] = result["ukeire"]

    return {
        "shanten": original_shanten,
        "normalDiscard": normal_discard,
        "recedingDiscard": receding_discard
    }

def calc_ukeire(hand):
    """
    計算一手牌的打牌受入資訊，使用 Taiwan 規則（只支援標準面子手）
    :param hand: List[List[int]] 四個花色的手牌
    :return: dict，包括向聽數與每張牌的改善資訊
    """
    try:
        state = check_hand(hand)
    except Exception as e:
        raise ValueError(f"Invalid hand: {e}")

    shanten_fn = cal_shanten_menzu

    if state == "To draw":
        return ukeire_add1(hand, shanten_fn)
    else:
        return ukeire_remove1(hand, shanten_fn)
