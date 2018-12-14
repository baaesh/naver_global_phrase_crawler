import json

with open('data/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

processed = {}
for category in data:
    sentences = []
    for mid in data[category]:
        if not mid == '자주 쓰이는 표현':
            for small in data[category][mid]:
                sentences += data[category][mid][small]
    processed[category] = sentences

with open('data/processed.json', 'w', encoding='utf-8') as f:
    json.dump(processed, f, ensure_ascii=False)
