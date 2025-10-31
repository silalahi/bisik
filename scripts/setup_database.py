from pathlib import Path
import csv


def create_english_samples():
    samples = [
        {"id": 1, "text": "The quick brown fox jumps over the lazy dog", "difficulty": "easy", "category": "sentence"},
        {"id": 2, "text": "She sells seashells by the seashore", "difficulty": "medium", "category": "tongue_twister"},
        {"id": 3, "text": "Peter Piper picked a peck of pickled peppers", "difficulty": "hard", "category": "tongue_twister"},
        {"id": 4, "text": "How much wood would a woodchuck chuck if a woodchuck could chuck wood", "difficulty": "hard", "category": "tongue_twister"},
        {"id": 5, "text": "Hello how are you today", "difficulty": "easy", "category": "greeting"},
        {"id": 6, "text": "I would like to improve my pronunciation", "difficulty": "medium", "category": "statement"},
        {"id": 7, "text": "The weather is beautiful today", "difficulty": "easy", "category": "statement"},
        {"id": 8, "text": "Artificial intelligence is transforming technology", "difficulty": "hard", "category": "technical"},
        {"id": 9, "text": "Red lorry yellow lorry", "difficulty": "medium", "category": "tongue_twister"},
        {"id": 10, "text": "Unique New York", "difficulty": "easy", "category": "tongue_twister"},
    ]
    
    db_path = Path("databases/english_samples.csv")
    db_path.parent.mkdir(exist_ok=True)
    
    with open(db_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'text', 'difficulty'])
        writer.writeheader()
        writer.writerows(samples)
    
    print(f"✓ Created {db_path}")


def create_german_samples():
    samples = [
        {"id": 1, "text": "Guten Tag wie geht es Ihnen", "difficulty": "easy", "category": "greeting"},
        {"id": 2, "text": "Der schnelle braune Fuchs", "difficulty": "easy", "category": "sentence"},
        {"id": 3, "text": "Ich möchte meine Aussprache verbessern", "difficulty": "medium", "category": "statement"},
        {"id": 4, "text": "Das Wetter ist heute wunderschön", "difficulty": "easy", "category": "statement"},
        {"id": 5, "text": "Fischers Fritz fischt frische Fische", "difficulty": "hard", "category": "tongue_twister"},
    ]
    
    db_path = Path("databases/german_samples.csv")
    db_path.parent.mkdir(exist_ok=True)
    
    with open(db_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'text', 'difficulty'])
        writer.writeheader()
        writer.writerows(samples)
    
    print(f"✓ Created {db_path}")


if __name__ == '__main__':
    create_english_samples()
    create_german_samples()
    print("\n✓ All databases initialized!")