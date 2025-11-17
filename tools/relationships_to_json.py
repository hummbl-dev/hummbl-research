import csv
import json
import sys

# Usage: python relationships_to_json.py data/relationships.csv data/relationships.json

def main(input_csv, output_json):
    relationships = []
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        # Skip first row if it's a title
        if rows and 'HUMMBL-Relationships' in rows[0][0]:
            rows = rows[1:]
        header = rows[0]
        for row in rows[1:]:
            rel = dict(zip(header, row))
            relationships.append({
                'id': rel.get('relation_id', '').strip(),
                'from': rel.get('from_model', '').strip(),
                'to': rel.get('to_model', '').strip(),
                'type': rel.get('relation_type', '').strip().upper(),
                'strength': float(rel.get('strength', 0)),
                'direction': rel.get('direction', '').strip(),
                'description': rel.get('description', '').strip()
            })
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(relationships, f, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python relationships_to_json.py <input_csv> <output_json>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
