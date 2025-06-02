import os
import tempfile
from ultralytics import YOLO
from ukeire import calc_ukeire
from cal_shanten import cal_shanten_menzu
from tile_utils import tile_names, check_tile

model = YOLO("./trained_model/best.pt")

def tile_to_chinese(tile):
    number_map = {
        '1': '一', '2': '二', '3': '三', '4': '四', '5': '五',
        '6': '六', '7': '七', '8': '八', '9': '九'
    }
    honor_map = {
        '1z': '東風', '2z': '南風', '3z': '西風', '4z': '北風',
        '5z': '白板', '6z': '發財', '7z': '紅中'
    }

    if tile.endswith('m'):
        return number_map[tile[0]] + '萬'
    elif tile.endswith('p'):
        return number_map[tile[0]] + '筒'
    elif tile.endswith('s'):
        return number_map[tile[0]] + '條'
    elif tile in honor_map:
        return honor_map[tile]
    else:
        return tile

def chinese_to_tile(ch):
    reverse_number_map = {
        '一': '1', '二': '2', '三': '3', '四': '4', '五': '5',
        '六': '6', '七': '7', '八': '8', '九': '9'
    }
    reverse_honor_map = {
        '東風': '1z', '南風': '2z', '西風': '3z', '北風': '4z',
        '白板': '5z', '發財': '6z', '紅中': '7z'
    }

    if len(ch) == 2 and ch[0] in reverse_number_map:
        num = reverse_number_map[ch[0]]
        suit = ch[1]
        if suit == '萬':
            return num + 'm'
        elif suit == '筒':
            return num + 'p'
        elif suit == '條':
            return num + 's'
    elif ch in reverse_honor_map:
        return reverse_honor_map[ch]
    else:
        return None

def classify_tiles(tile_labels):
    suits = {'m': [0]*9, 'p': [0]*9, 's': [0]*9, 'z': [0]*7}

    for label in tile_labels:
        if not check_tile(label):
            print(f"⚠️ 無效牌名: {label}")
            continue

        suit = label[-1]
        index = int(label[:-1]) - 1
        suits[suit][index] += 1

    return [suits['m'], suits['p'], suits['s'], suits['z']]



def convert_label(label):
    if label.startswith("character_"):
        return label.split("_")[1] + "m"
    elif label.startswith("circle_"):
        return label.split("_")[1] + "p"
    elif label.startswith("bamboo_"):
        return label.split("_")[1] + "s"
    map_z = {"east": "1z", "south": "2z", "west": "3z", "north": "4z",
             "white": "5z", "green": "6z", "red": "7z"}
    return map_z.get(label, label)

def sort_tiles(tile_list):
    suit_order = {'m': 0, 'p': 1, 's': 2, 'z': 3}

    def tile_key(tile):
        suit = tile[-1]
        number = int(tile[:-1])
        return (suit_order[suit], number)

    return sorted(tile_list, key=tile_key)

def predict_tile_labels(image):
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        image.save(tmp.name)
        image_path = tmp.name

    try:
        results = model.predict(source=image_path)
        tile_labels = []

        for r in results:
            if hasattr(r, "boxes") and r.boxes:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    label = model.names[cls_id]
                    tile_labels.append(convert_label(label))

        if len(tile_labels) != 17:
            chinese_tiles = [tile_to_chinese(t) for t in tile_labels]
            return f"⚠️ 檢測牌數錯誤（辨識到 {len(tile_labels)} 張）: {', '.join(chinese_tiles)}"
        
        tile_labels = sort_tiles(tile_labels)
        return ", ".join(tile_to_chinese(t) for t in tile_labels)

    finally:
        os.remove(image_path)


def analyze_tile_string(tile_str):
    tile_labels = []
    for t in tile_str.split(","):
        t = t.strip()
        if not t:
            continue
        if check_tile(t):
            tile_labels.append(t)
        else:
            converted = chinese_to_tile(t)
            if converted and check_tile(converted):
                tile_labels.append(converted)
            else:
                tile_labels.append(t)

    if len(tile_labels) != 17:
        return f"⚠️ 牌數錯誤：應該是 17 張，現在是 {len(tile_labels)} 張。"

    if any(not check_tile(t) for t in tile_labels):
        return f"⚠️ 包含無效牌名，請確認格式為 '1m, 2m, 3m, ..., 7z'"

    tile_labels = sort_tiles(tile_labels)
    suits = classify_tiles(tile_labels)
    tile_count = sum(sum(suit) for suit in suits)
    if tile_count == 0:
        return "⚠️ 無法從輸入的文字建立合法的手牌，請檢查格式與拼字。"

    try:
        shanten = cal_shanten_menzu(suits)
        ukeire_result = calc_ukeire(suits)
    except Exception as e:
        return f"⚠️ 無法分析手牌：{e}"

    output = [f"📏 向聽數：{ukeire_result['shanten']} 向聽"]

    if 'ukeire' in ukeire_result:
        ukeire_lines = [f"🎯 有效進張：共 {ukeire_result['totalUkeire']} 張"]
        for tile, count in sorted(ukeire_result['ukeire'].items()):
            ukeire_lines.append(f"　- {tile_to_chinese(tile)} × {count}")
        output.extend(ukeire_lines)
    elif 'normalDiscard' in ukeire_result:
        output.append("🗑 建議打牌選擇：")
        for tile, uke in ukeire_result['normalDiscard'].items():
            uke_str = ", ".join(f"{tile_to_chinese(k)}×{v}" for k, v in uke.items())
            output.append(f"　- 打 {tile_to_chinese(tile)} → 有效牌: {uke_str}")

        if ukeire_result['recedingDiscard']:
            output.append("⚠️ 以下打牌會讓向聽變差：")
            for tile, uke in ukeire_result['recedingDiscard'].items():
                uke_str = ", ".join(f"{tile_to_chinese(k)}×{v}" for k, v in uke.items())
                output.append(f"　- 打 {tile_to_chinese(tile)} → 有效牌: {uke_str}")

    return "\n".join(output)
