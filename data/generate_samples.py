"""
Sample conversation generator for testing the evaluation system.
Creates diverse conversation examples covering various scenarios.
"""

import json
import csv
from typing import List, Dict, Any
from dataclasses import dataclass
import random

@dataclass
class SampleConversation:
    id: str
    text: str
    context: str
    category: str
    expected_scores: Dict[str, int]
    description: str

def generate_sample_conversations() -> List[SampleConversation]:
    """Generate 50+ diverse conversation examples."""
    
    conversations = []
    
    # 1. Polite and Professional Conversations
    conversations.extend([
        SampleConversation(
            id="prof_001",
            text="Good morning! I hope you're having a wonderful day. Could you please help me understand the project requirements?",
            context="Professional workplace interaction",
            category="professional",
            expected_scores={
                "politeness": 5, "clarity": 4, "appropriateness": 5, "grammar": 5,
                "empathy": 4, "toxicity": 1, "bias": 1
            },
            description="Polite professional greeting with clear request"
        ),
        SampleConversation(
            id="prof_002", 
            text="Thank you so much for your detailed explanation. It really helped me understand the process better.",
            context="Follow-up professional conversation",
            category="professional",
            expected_scores={
                "politeness": 5, "clarity": 5, "empathy": 4, "grammar": 5,
                "appropriateness": 5, "toxicity": 1, "bias": 1
            },
            description="Expressing gratitude professionally"
        ),
        SampleConversation(
            id="prof_003",
            text="I apologize for the delay in my response. I was waiting for additional information from our team before getting back to you.",
            context="Professional apology",
            category="professional", 
            expected_scores={
                "politeness": 5, "clarity": 4, "appropriateness": 5, "grammar": 5,
                "empathy": 3, "toxicity": 1, "bias": 1
            },
            description="Professional apology with explanation"
        ),
    ])
    
    # 2. Casual and Friendly Conversations
    conversations.extend([
        SampleConversation(
            id="casual_001",
            text="Hey! How's it going? I heard you got that promotion - congratulations!",
            context="Casual friendly conversation",
            category="casual",
            expected_scores={
                "politeness": 4, "clarity": 4, "empathy": 5, "grammar": 4,
                "appropriateness": 4, "sentiment": 5, "toxicity": 1, "bias": 1
            },
            description="Friendly casual congratulations"
        ),
        SampleConversation(
            id="casual_002",
            text="Thanks for hanging out with me today! I had such a great time catching up.",
            context="End of casual meetup",
            category="casual",
            expected_scores={
                "politeness": 4, "clarity": 5, "empathy": 4, "grammar": 4,
                "sentiment": 5, "appropriateness": 4, "toxicity": 1, "bias": 1
            },
            description="Expressing enjoyment after social gathering"
        ),
        SampleConversation(
            id="casual_003",
            text="Haha, that's hilarious! You always know how to make me laugh.",
            context="Response to humor",
            category="casual",
            expected_scores={
                "politeness": 3, "clarity": 4, "empathy": 4, "grammar": 3,
                "sentiment": 5, "appropriateness": 4, "toxicity": 1, "bias": 1
            },
            description="Positive response to humor"
        ),
    ])
    
    # 3. Customer Service Scenarios
    conversations.extend([
        SampleConversation(
            id="service_001",
            text="I understand your frustration, and I'm here to help resolve this issue as quickly as possible. Let me look into this for you right away.",
            context="Customer service response",
            category="customer_service",
            expected_scores={
                "empathy": 5, "politeness": 5, "appropriateness": 5, "clarity": 4,
                "grammar": 5, "toxicity": 1, "bias": 1
            },
            description="Empathetic customer service response"
        ),
        SampleConversation(
            id="service_002",
            text="I apologize for the inconvenience this has caused. We take these matters very seriously and will ensure this doesn't happen again.",
            context="Customer service apology",
            category="customer_service",
            expected_scores={
                "empathy": 4, "politeness": 5, "appropriateness": 5, "grammar": 5,
                "clarity": 4, "toxicity": 1, "bias": 1
            },
            description="Formal customer service apology"
        ),
        SampleConversation(
            id="service_003",
            text="Great question! Our premium plan includes all the features you mentioned, plus 24/7 support and priority processing.",
            context="Product inquiry response",
            category="customer_service",
            expected_scores={
                "clarity": 5, "appropriateness": 5, "politeness": 4, "grammar": 5,
                "informativeness": 5, "toxicity": 1, "bias": 1
            },
            description="Informative product explanation"
        ),
    ])
    
    # 4. Educational/Instructional
    conversations.extend([
        SampleConversation(
            id="edu_001",
            text="Let me break this down step by step. First, we need to understand the basic concepts before moving to advanced topics.",
            context="Teaching explanation",
            category="educational",
            expected_scores={
                "clarity": 5, "appropriateness": 5, "grammar": 5, "coherence": 5,
                "informativeness": 4, "toxicity": 1, "bias": 1
            },
            description="Clear instructional explanation"
        ),
        SampleConversation(
            id="edu_002",
            text="That's an excellent question! It shows you're really thinking about the material. The answer involves several factors...",
            context="Responding to student question",
            category="educational",
            expected_scores={
                "empathy": 4, "clarity": 4, "appropriateness": 5, "grammar": 5,
                "politeness": 4, "toxicity": 1, "bias": 1
            },
            description="Encouraging educational response"
        ),
        SampleConversation(
            id="edu_003",
            text="Remember, there's no such thing as a stupid question. Learning is a process, and everyone progresses at their own pace.",
            context="Encouraging struggling student",
            category="educational",
            expected_scores={
                "empathy": 5, "appropriateness": 5, "clarity": 4, "grammar": 5,
                "emotional_appropriateness": 5, "toxicity": 1, "bias": 1
            },
            description="Supportive educational encouragement"
        ),
    ])
    
    # 5. Emotional Support/Counseling
    conversations.extend([
        SampleConversation(
            id="support_001",
            text="I can hear that you're going through a really difficult time. Your feelings are completely valid, and it's okay to feel overwhelmed.",
            context="Emotional support conversation",
            category="support",
            expected_scores={
                "empathy": 5, "emotional_appropriateness": 5, "clarity": 4, "grammar": 5,
                "appropriateness": 5, "compassion": 5, "toxicity": 1, "bias": 1
            },
            description="Validating emotional support"
        ),
        SampleConversation(
            id="support_002",
            text="You've shown incredible strength in dealing with this situation. Remember that it's okay to ask for help when you need it.",
            context="Encouraging someone in difficulty",
            category="support",
            expected_scores={
                "empathy": 5, "emotional_appropriateness": 5, "clarity": 4, "grammar": 4,
                "compassion": 5, "appropriateness": 5, "toxicity": 1, "bias": 1
            },
            description="Acknowledging strength and offering support"
        ),
    ])
    
    # 6. Conflict Resolution
    conversations.extend([
        SampleConversation(
            id="conflict_001",
            text="I understand we have different perspectives on this issue. Perhaps we can find a solution that works for both of us.",
            context="Conflict resolution attempt",
            category="conflict_resolution",
            expected_scores={
                "appropriateness": 5, "empathy": 4, "clarity": 4, "grammar": 5,
                "politeness": 4, "cooperation": 5, "toxicity": 1, "bias": 1
            },
            description="Diplomatic conflict resolution approach"
        ),
        SampleConversation(
            id="conflict_002",
            text="I appreciate you sharing your concerns with me. Let's work together to address these issues constructively.",
            context="Responding to criticism",
            category="conflict_resolution",
            expected_scores={
                "appropriateness": 5, "empathy": 4, "politeness": 5, "grammar": 5,
                "cooperation": 5, "emotional_stability": 4, "toxicity": 1, "bias": 1
            },
            description="Constructive response to criticism"
        ),
    ])
    
    # 7. Technical/Complex Explanations
    conversations.extend([
        SampleConversation(
            id="tech_001",
            text="The algorithm processes data through multiple layers, each extracting different features. Think of it like a filter that refines information at each step.",
            context="Technical explanation with analogy",
            category="technical",
            expected_scores={
                "clarity": 4, "informativeness": 5, "grammar": 5, "coherence": 4,
                "appropriateness": 4, "vocabulary_richness": 4, "toxicity": 1, "bias": 1
            },
            description="Technical concept explained with analogy"
        ),
        SampleConversation(
            id="tech_002",
            text="To troubleshoot this issue, we need to check three things: the network connection, the database configuration, and the API endpoints.",
            context="Technical troubleshooting",
            category="technical",
            expected_scores={
                "clarity": 5, "informativeness": 5, "grammar": 5, "coherence": 5,
                "appropriateness": 5, "conciseness": 4, "toxicity": 1, "bias": 1
            },
            description="Clear technical troubleshooting steps"
        ),
    ])
    
    # 8. Inappropriate/Problematic Content (for safety testing)
    conversations.extend([
        SampleConversation(
            id="problem_001",
            text="You're absolutely wrong and clearly don't understand anything about this topic. This is a waste of my time.",
            context="Hostile disagreement",
            category="problematic",
            expected_scores={
                "politeness": 1, "appropriateness": 1, "empathy": 1, "grammar": 4,
                "toxicity": 4, "emotional_appropriateness": 1, "bias": 2
            },
            description="Dismissive and hostile response"
        ),
        SampleConversation(
            id="problem_002",
            text="I don't have time to explain this to someone who obviously can't grasp basic concepts.",
            context="Condescending response",
            category="problematic",
            expected_scores={
                "politeness": 1, "appropriateness": 1, "empathy": 1, "grammar": 4,
                "toxicity": 3, "bias": 3, "emotional_appropriateness": 1
            },
            description="Condescending and dismissive"
        ),
    ])
    
    # 9. Ambiguous/Unclear Communication
    conversations.extend([
        SampleConversation(
            id="unclear_001",
            text="Yeah, so like, the thing we talked about before... you know what I mean? It's kinda complicated but not really.",
            context="Vague reference to previous conversation",
            category="unclear",
            expected_scores={
                "clarity": 1, "coherence": 2, "grammar": 2, "informativeness": 1,
                "appropriateness": 2, "conciseness": 2, "toxicity": 1, "bias": 1
            },
            description="Very vague and unclear communication"
        ),
        SampleConversation(
            id="unclear_002",
            text="The project, well, it's going... there are some challenges but also opportunities, if you know what I mean.",
            context="Project status update",
            category="unclear",
            expected_scores={
                "clarity": 2, "informativeness": 1, "grammar": 3, "coherence": 2,
                "appropriateness": 2, "conciseness": 2, "toxicity": 1, "bias": 1
            },
            description="Evasive and uninformative response"
        ),
    ])
    
    # 10. Multilingual/Cultural Context
    conversations.extend([
        SampleConversation(
            id="cultural_001",
            text="Namaste! I hope you and your family are in good health. I wanted to discuss the upcoming festival arrangements.",
            context="Cultural greeting in diverse workplace",
            category="cultural",
            expected_scores={
                "politeness": 5, "appropriateness": 5, "empathy": 4, "grammar": 5,
                "cultural_sensitivity": 5, "clarity": 4, "toxicity": 1, "bias": 1
            },
            description="Culturally inclusive greeting"
        ),
        SampleConversation(
            id="cultural_002",
            text="In my culture, we have a saying that translates to 'patience brings wisdom.' I think this applies to our current situation.",
            context="Sharing cultural wisdom",
            category="cultural",
            expected_scores={
                "appropriateness": 5, "clarity": 4, "grammar": 5, "empathy": 4,
                "cultural_sensitivity": 5, "wisdom": 4, "toxicity": 1, "bias": 1
            },
            description="Sharing cultural perspective constructively"
        ),
    ])
    
    # 11. Crisis/Emergency Communication
    conversations.extend([
        SampleConversation(
            id="crisis_001",
            text="I understand this is an urgent situation. I'm escalating this immediately to our emergency response team and will keep you updated every step of the way.",
            context="Emergency response",
            category="crisis",
            expected_scores={
                "appropriateness": 5, "clarity": 5, "empathy": 4, "grammar": 5,
                "responsiveness": 5, "professionalism": 5, "toxicity": 1, "bias": 1
            },
            description="Professional emergency response"
        ),
        SampleConversation(
            id="crisis_002",
            text="Please stay calm. Help is on the way. Can you tell me your exact location and describe what's happening?",
            context="Emergency assistance call",
            category="crisis",
            expected_scores={
                "appropriateness": 5, "clarity": 5, "empathy": 4, "grammar": 5,
                "calmness": 5, "helpfulness": 5, "toxicity": 1, "bias": 1
            },
            description="Calming emergency assistance"
        ),
    ])
    
    # 12. Creative/Imaginative Content
    conversations.extend([
        SampleConversation(
            id="creative_001",
            text="Imagine a world where colors have flavors and music creates visible patterns in the air. What would your favorite song taste like?",
            context="Creative conversation starter",
            category="creative",
            expected_scores={
                "creativity": 5, "clarity": 4, "grammar": 5, "appropriateness": 4,
                "engagement": 5, "imagination": 5, "toxicity": 1, "bias": 1
            },
            description="Imaginative and engaging question"
        ),
        SampleConversation(
            id="creative_002",
            text="Your idea reminds me of a story where every word someone spoke became a butterfly that carried their intentions to others.",
            context="Creative response to idea",
            category="creative",
            expected_scores={
                "creativity": 5, "clarity": 4, "grammar": 4, "appropriateness": 4,
                "imagination": 5, "engagement": 4, "toxicity": 1, "bias": 1
            },
            description="Creative metaphorical response"
        ),
    ])
    
    # Add more diverse examples...
    # 13-20: Various professional scenarios, personal conversations, etc.
    additional_conversations = [
        SampleConversation(
            id="misc_001",
            text="I'm sorry, but I don't have enough information to answer that question accurately. Could you provide more details?",
            context="Admitting knowledge limitation",
            category="honest_limitation",
            expected_scores={
                "honesty": 5, "appropriateness": 5, "politeness": 4, "grammar": 5,
                "clarity": 4, "humility": 4, "toxicity": 1, "bias": 1
            },
            description="Honest admission of knowledge limitation"
        ),
        SampleConversation(
            id="misc_002",
            text="Congratulations on your achievement! Your hard work and dedication really paid off. You should be proud of yourself.",
            context="Celebrating someone's success",
            category="celebration",
            expected_scores={
                "empathy": 5, "positivity": 5, "appropriateness": 5, "grammar": 5,
                "encouragement": 5, "clarity": 5, "toxicity": 1, "bias": 1
            },
            description="Genuine celebration of achievement"
        ),
        # Add more to reach 50+ total...
    ]
    
    # Generate additional conversations programmatically
    templates = [
        ("question_001", "Could you please explain how this process works? I'm having trouble understanding the steps involved.", "inquiry", {"clarity": 4, "politeness": 4, "appropriateness": 5}),
        ("feedback_001", "I really appreciate the effort you put into this project. The attention to detail is impressive.", "positive_feedback", {"empathy": 4, "positivity": 5, "appropriateness": 5}),
        ("suggestion_001", "I have an idea that might help improve efficiency. Would you be interested in hearing it?", "suggestion", {"politeness": 5, "appropriateness": 5, "collaboration": 4}),
        ("clarification_001", "Just to make sure I understand correctly, you're saying that we should prioritize the client requests first?", "clarification", {"clarity": 4, "appropriateness": 5, "attention_to_detail": 4}),
        ("scheduling_001", "I'm available for the meeting on Tuesday or Wednesday afternoon. What works best for your schedule?", "scheduling", {"politeness": 4, "flexibility": 5, "clarity": 5}),
    ]
    
    for temp_id, text, category, scores in templates:
        base_scores = {"grammar": 4, "clarity": 4, "appropriateness": 4, "toxicity": 1, "bias": 1}
        base_scores.update(scores)
        additional_conversations.append(
            SampleConversation(
                id=temp_id,
                text=text,
                context=f"Generated {category} example",
                category=category,
                expected_scores=base_scores,
                description=f"Template-generated {category} conversation"
            )
        )
    
    conversations.extend(additional_conversations)
    
    return conversations

def save_conversations_to_files(conversations: List[SampleConversation], output_dir: str = "data/sample_conversations"):
    """Save conversations to CSV and JSON files."""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Save as CSV
    csv_file = os.path.join(output_dir, "sample_conversations.csv")
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'text', 'context', 'category', 'description', 'expected_scores'])
        
        for conv in conversations:
            writer.writerow([
                conv.id,
                conv.text,
                conv.context,
                conv.category,
                conv.description,
                json.dumps(conv.expected_scores)
            ])
    
    # Save as JSON
    json_file = os.path.join(output_dir, "sample_conversations.json")
    conversations_dict = []
    for conv in conversations:
        conversations_dict.append({
            'id': conv.id,
            'text': conv.text,
            'context': conv.context,
            'category': conv.category,
            'description': conv.description,
            'expected_scores': conv.expected_scores
        })
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(conversations_dict, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(conversations)} conversations to {output_dir}")
    
    # Generate summary statistics
    stats_file = os.path.join(output_dir, "dataset_statistics.json")
    categories = {}
    total_facets = set()
    
    for conv in conversations:
        category = conv.category
        if category not in categories:
            categories[category] = 0
        categories[category] += 1
        total_facets.update(conv.expected_scores.keys())
    
    stats = {
        'total_conversations': len(conversations),
        'categories': categories,
        'unique_facets': len(total_facets),
        'facet_list': sorted(list(total_facets))
    }
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)

if __name__ == "__main__":
    conversations = generate_sample_conversations()
    print(f"Generated {len(conversations)} sample conversations")
    
    # Print first few examples
    for i, conv in enumerate(conversations[:3]):
        print(f"\nExample {i+1}:")
        print(f"ID: {conv.id}")
        print(f"Text: {conv.text}")
        print(f"Category: {conv.category}")
        print(f"Expected scores: {conv.expected_scores}")
    
    save_conversations_to_files(conversations)