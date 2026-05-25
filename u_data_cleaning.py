import pandas as pd

def parse_group_lessons(row, cardio_classes = ['Running', 'Les Miles', 'HIT', 'Spinning', 'Zumba'], strength_classes = ['Kickboxen', 'BodyPump', 'XCore'], mind_body_classes = ['BodyBalance', 'Yoga', 'Pilates']):
    '''For each row, '''

    # For the case in which the person doesn't go regularly to group classes we can fill all those cols with 0
    if pd.isna(row['fav_group_lesson']):
        return pd.Series({'num_classes_attended': 0, 
                          'ratio_cardio': 0.0, 
                          'ratio_strength': 0.0, 
                          'ratio_mind_body': 0.0})
    
    classes = [c.strip() for c in row['fav_group_lesson'].split(',')]
    num_classes = len(classes)
    
    # Count occurrences per category
    cardio_count = sum(1 for c in classes if c in cardio_classes)
    strength_count = sum(1 for c in classes if c in strength_classes)
    mind_body_count = sum(1 for c in classes if c in mind_body_classes)
    
    # 3. Calculate ratios safely
    if num_classes > 0:
        return pd.Series({
            'num_classes_attended': num_classes,
            'ratio_cardio': cardio_count / num_classes,
            'ratio_strength': strength_count / num_classes,
            'ratio_mind_body': mind_body_count / num_classes
        })
    else:
        return pd.Series({'num_classes_attended': 0, 
                          'ratio_cardio': 0.0, 
                          'ratio_strength': 0.0, 
                          'ratio_mind_body': 0.0})
    

def calculate_weekend_ratio(days_str):
    if pd.isna(days_str) or not isinstance(days_str, str) or days_str.strip() == "":
        return 0.0

    days_list = [day.strip() for day in days_str.split(",")]

    total_days = len(days_list)
    if total_days == 0:
        return 0.0

  
    weekend_days = ["Sat", "Sun"]
    weekend_count = sum(1 for day in days_list if day in weekend_days)

    
    return weekend_count / total_days