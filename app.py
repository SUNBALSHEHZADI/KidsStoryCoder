# app.py - Enhanced Version with Improved UX
import streamlit as st
import random
import re
import time
import base64
import json
import requests
from PIL import Image
import io
import matplotlib.pyplot as plt
import numpy as np
from streamlit.components.v1 import html

# Configure Streamlit page
st.set_page_config(
    page_title="StoryCoder - Play & Learn Coding",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sound effects
SOUND_EFFECTS = {
    "click": "data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQoGAACBhYqNkJSZnJ+ipqmtr7K0t7m8vsDCxcfKzM/Q0tTW2Nvd3+Dh4+Xn6evt7/Dx8/T19/j5+vv8/f7/AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8gISIjJCUmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0+P0BBQkNERUZHSElKS0xNTk9QUVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6e3x9fn+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmqq6ytrq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t/g4eLj5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+//8=",
    "star": "data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQoGAACBhYqNkJSZnJ+ipqmtr7K0t7m8vsDCxcfKzM/Q0tTW2Nvd3+Dh4+Xn6evt7/Dx8/T19/j5+vv8/f7/AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8gISIjJCUmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0+P0BBQkNERUZHSElKS0xNTk9QUVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6e3x9fn+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmqq6ytrq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t/g4eLj5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+//8=",
    "obstacle": "data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQoGAACBhYqNkJSZnJ+ipqmtr7K0t7m8vsDCxcfKzM/Q0tTW2Nvd3+Dh4+Xn6evt7/Dx8/T19/j5+vv8/f7/AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8gISIjJCUmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0+P0BBQkNERUZHSElKS0xNTk9QUVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6e3x9fn+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmqq6ytrq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t/g4eLj5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+//8=",
    "goal": "data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQoGAACBhYqNkJSZnJ+ipqmtr7K0t7m8vsDCxcfKzM/Q0tTW2Nvd3+Dh4+Xn6evt7/Dx8/T19/j5+vv8/f7/AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8gISIjJCUmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0+P0BBQkNERUZHSElKS0xNTk9QUVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnS0dXZ3eHl6e3x9fn+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmqq6ytrq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t/g4eLj5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+//8="
}

# Custom CSS with light purple background and wave design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Comic+Neue:wght@700&display=swap');
    
    :root {
        --primary: #8A2BE2;
        --secondary: #9370DB;
        --accent: #FFD700;
        --dark: #4B0082;
        --light: #E6E6FA;
        --game-blue: #6A5ACD;
        --game-purple: #9400D3;
        --gradient-start: #E6E6FA;
        --gradient-mid: #D8BFD8;
        --gradient-end: #DDA0DD;
    }
    
    body {
        background: linear-gradient(135deg, var(--gradient-start), var(--gradient-mid), var(--gradient-end));
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Comic Neue', cursive;
        margin: 0;
        padding: 0;
        min-height: 100vh;
    }
    
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    
    .stApp {
        background: url('https://www.transparenttextures.com/patterns/always-grey.png');
        background-color: rgba(230, 230, 250, 0.9);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
    }
    
    .wave-divider {
        width: 100%;
        height: 150px;
        overflow: hidden;
        margin: -10px 0 20px 0;
        transform: rotate(180deg);
    }
    
    .wave-divider svg {
        height: 100%;
        width: 100%;
    }
    
    .wave-divider path {
        stroke: none;
        fill: var(--primary);
        opacity: 0.2;
    }
    
    .game-card {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(138, 43, 226, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.5);
        margin-bottom: 25px;
        transition: all 0.3s;
    }
    
    .game-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(138, 43, 226, 0.3);
    }
    
    .header {
        color: var(--dark);
        font-family: 'Fredoka One', cursive;
        text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.8);
    }
    
    .concept-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid var(--accent);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .stButton>button {
        background: linear-gradient(45deg, var(--primary), var(--game-purple));
        color: white;
        border-radius: 50px;
        padding: 12px 28px;
        font-weight: bold;
        font-size: 18px;
        border: none;
        transition: all 0.3s;
        font-family: 'Fredoka One', cursive;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(138, 43, 226, 0.4);
    }
    
    .stTextInput>div>div>input {
        border-radius: 20px;
        padding: 14px;
        border: 3px solid var(--accent);
        font-size: 18px;
        background: rgba(255, 255, 255, 0.9);
    }
    
    .tabs {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
        overflow-x: auto;
        background: rgba(255, 255, 255, 0.3);
        padding: 10px;
        border-radius: 20px;
        backdrop-filter: blur(5px);
    }
    
    .tab {
        padding: 12px 24px;
        background: rgba(255, 255, 255, 0.4);
        border-radius: 15px;
        cursor: pointer;
        font-weight: bold;
        white-space: nowrap;
        font-family: 'Fredoka One', cursive;
        font-size: 16px;
        transition: all 0.3s;
        color: var(--dark);
    }
    
    .tab.active {
        background: linear-gradient(45deg, var(--primary), var(--game-purple));
        color: white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .game-board {
        display: grid;
        grid-template-columns: repeat(8, 1fr);
        grid-template-rows: repeat(8, 1fr);
        gap: 4px;
        width: 500px;
        height: 500px;
        margin: 0 auto;
        background: rgba(147, 112, 219, 0.2);
        padding: 10px;
        border-radius: 15px;
    }
    
    .cell {
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 8px;
        font-size: 30px;
        background: rgba(255, 255, 255, 0.85);
        transition: all 0.2s;
        cursor: pointer;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .cell:hover {
        transform: scale(1.05);
        background: rgba(255, 255, 255, 1);
    }
    
    .player {
        background: linear-gradient(45deg, var(--primary), var(--game-blue));
        color: white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .goal {
        background: linear-gradient(45deg, var(--accent), #FFA500);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .obstacle {
        background: linear-gradient(45deg, var(--secondary), #8A2BE2);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .star {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .portal {
        background: linear-gradient(45deg, #9B5DE5, #6A0DAD);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .game-controls {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin: 25px 0;
    }
    
    .control-btn {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background: linear-gradient(45deg, var(--primary), var(--game-purple));
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        cursor: pointer;
        border: none;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        transition: all 0.2s;
    }
    
    .control-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }
    
    .score-board {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        font-family: 'Fredoka One', cursive;
        font-size: 24px;
        margin: 20px auto;
        width: 300px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        border: 2px solid var(--primary);
    }
    
    .level-indicator {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 10px 20px;
        text-align: center;
        font-family: 'Fredoka One', cursive;
        font-size: 20px;
        margin: 10px auto;
        width: 200px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 2px solid var(--accent);
    }
    
    .theme-customizer {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 8px 16px rgba(138, 43, 226, 0.2);
        border: 3px solid var(--primary);
    }
    
    .customizer-title {
        text-align: center;
        font-family: 'Fredoka One', cursive;
        color: var(--primary);
        margin-bottom: 20px;
        font-size: 24px;
    }
    
    .char-preview {
        text-align: center;
        font-size: 48px;
        margin: 10px 0;
    }
    
    @media (max-width: 768px) {
        .tabs {
            flex-wrap: wrap;
        }
        
        .game-board {
            width: 90vw;
            height: 90vw;
        }
        
        .control-btn {
            width: 60px;
            height: 60px;
            font-size: 24px;
        }
    }
    
    .typewriter h2 {
        overflow: hidden;
        border-right: .15em solid var(--accent);
        white-space: nowrap;
        margin: 0 auto;
        letter-spacing: .15em;
        animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite;
        color: var(--dark);
        font-family: 'Fredoka One', cursive;
    }
    
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: var(--accent); }
    }
    
    .floating {
        animation: floating 3s ease-in-out infinite;
    }
    
    @keyframes floating {
        0% { transform: translate(0,  0px); }
        50%  { transform: translate(0, 15px); }
        100%   { transform: translate(0, -0px); }
    }
    
    .concept-btn {
        background: linear-gradient(45deg, var(--primary), var(--game-purple));
        color: white;
        border-radius: 15px;
        padding: 12px;
        font-weight: bold;
        font-size: 16px;
        border: none;
        transition: all 0.3s;
        font-family: 'Fredoka One', cursive;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        margin: 5px;
        width: 100%;
        text-align: center;
    }
    
    .concept-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(138, 43, 226, 0.4);
    }
    
    .example-box {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        transition: all 0.3s;
        border: 2px solid rgba(138, 43, 226, 0.2);
    }
    
    .example-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(138, 43, 226, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'story' not in st.session_state:
        st.session_state.story = ""
    if 'concepts' not in st.session_state:
        st.session_state.concepts = []
    if 'game_scenario' not in st.session_state:
        st.session_state.game_scenario = ""
    if 'game_code' not in st.session_state:
        st.session_state.game_code = ""
    if 'game_explanation' not in st.session_state:
        st.session_state.game_explanation = ""
    if 'game_preview' not in st.session_state:
        st.session_state.game_preview = None
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "story"
    if 'loading' not in st.session_state:
        st.session_state.loading = False
    if 'game_state' not in st.session_state:
        reset_game_state()
    if 'player_char' not in st.session_state:
        st.session_state.player_char = "🦸"
    if 'goal_char' not in st.session_state:
        st.session_state.goal_char = "🏁"
    if 'obstacle_char' not in st.session_state:
        st.session_state.obstacle_char = "🪨"
    if 'current_level' not in st.session_state:
        st.session_state.current_level = 1
    if 'total_levels' not in st.session_state:
        st.session_state.total_levels = 3
    if 'selected_concept' not in st.session_state:
        st.session_state.selected_concept = None
    if 'sound_played' not in st.session_state:
        st.session_state.sound_played = False

# Play sound function
def play_sound(sound_type):
    audio_html = f"""
        <audio autoplay>
        <source src="{SOUND_EFFECTS[sound_type]}" type="audio/wav">
        Your browser does not support the audio element.
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# Concept database
CONCEPTS = {
    "loop": {
        "name": "Loop",
        "emoji": "🔄",
        "description": "Loops repeat actions multiple times",
        "example": "for i in range(5):\n    print('Hello!')",
        "color": "#8A2BE2",
        "game_example": "Repeating jumps to cross a river"
    },
    "conditional": {
        "name": "Conditional",
        "emoji": "❓",
        "description": "Conditionals make decisions in code",
        "example": "if sunny:\n    go_outside()\nelse:\n    stay_inside()",
        "color": "#9370DB",
        "game_example": "Choosing paths based on obstacles"
    },
    "function": {
        "name": "Function",
        "emoji": "✨",
        "description": "Functions are reusable blocks of code",
        "example": "def greet(name):\n    print(f'Hello {name}!')",
        "color": "#FFD700",
        "game_example": "Creating a jump function used multiple times"
    },
    "variable": {
        "name": "Variable",
        "emoji": "📦",
        "description": "Variables store information",
        "example": "score = 10\nplayer = 'Alex'",
        "color": "#6A5ACD",
        "game_example": "Keeping track of collected stars"
    },
    "list": {
        "name": "List",
        "emoji": "📝",
        "description": "Lists store collections of items",
        "example": "fruits = ['apple', 'banana', 'orange']",
        "color": "#9400D3",
        "game_example": "Storing collected treasures in a backpack"
    }
}

# Analyze story and extract concepts
def analyze_story(story):
    """Analyze story and identify programming concepts"""
    story_lower = story.lower()
    detected_concepts = []
    
    # Improved concept detection
    # Check for loops
    if any(word in story_lower for word in ["times", "repeat", "again", "multiple", "each", "every"]):
        detected_concepts.append("loop")
    
    # Check for conditionals
    if any(word in story_lower for word in ["if", "when", "unless", "whether", "decide", "choice", "otherwise"]):
        detected_concepts.append("conditional")
    
    # Check for functions
    if any(word in story_lower for word in ["make", "create", "do", "perform", "cast", "action", "use"]):
        detected_concepts.append("function")
    
    # Check for variables
    if any(word in story_lower for word in ["is", "has", "set to", "value", "score", "count", "number"]):
        detected_concepts.append("variable")
    
    # Check for lists
    if any(word in story_lower for word in ["and", "many", "several", "collection", "items", "group", "set of"]):
        detected_concepts.append("list")
    
    return list(set(detected_concepts)) if detected_concepts else ["variable", "function"]

# Generate game scenario
def generate_game_scenario(story, concepts):
    """Generate a game scenario based on the story and concepts"""
    # Fallback template
    concept_names = [CONCEPTS[c]['name'] for c in concepts]
    concept_list = ", ".join(concept_names)
    return f"""
Game Title: {story[:15]} Adventure
Game Objective: Complete challenges based on your story: {story[:100]}...
Characters: 
- Hero: The main character from your story
- Helper: A friendly guide who explains coding concepts
- Villain: A character that creates obstacles (if applicable)

Game Mechanics:
1. Move your character using arrow keys
2. Collect stars while avoiding obstacles
3. Reach the goal to win
4. Helper characters appear to teach {concept_list}

Coding Concepts: This game teaches {concept_list} through:
- Using loops to repeat actions
- Making decisions with conditionals
- Creating reusable functions
- Tracking progress with variables
- Managing collections with lists

Visual Description: Colorful game world with cartoon-style characters, vibrant landscapes, and magical effects.
"""

# Generate game code explanation
def generate_game_explanation(story, concepts, game_scenario):
    """Generate explanation of game code"""
    # Fallback explanation
    concept_explanations = "\n".join(
        [f"- {CONCEPTS[c]['name']}: {CONCEPTS[c]['game_example']}" for c in concepts]
    )
    return f"""
In this game based on your story "{story[:20]}...", we use programming concepts to make it work:

{concept_explanations}

As you play the game, think about:
1. How the game uses these concepts to create challenges
2. How you might change the code to make the game easier or harder

The code brings your story to life in a fun game world!
"""

# Generate game preview visualization
def generate_game_preview(story):
    """Generate a visual preview of the game"""
    try:
        # Extract keywords for theme
        theme = "space" if "space" in story.lower() else "jungle" if "jungle" in story.lower() else "fantasy"
        
        # Create a simple visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if theme == "space":
            bg_color = '#0B0B2B'
            player_color = '#8A2BE2'
            goal_color = '#FFD700'
            obstacle_color = '#9370DB'
            title = "Space Adventure"
        elif theme == "jungle":
            bg_color = '#143D2C'
            player_color = '#8A2BE2'
            goal_color = '#FFD700'
            obstacle_color = '#6A5ACD'
            title = "Jungle Adventure"
        else:
            bg_color = '#3A015C'
            player_color = '#8A2BE2'
            goal_color = '#FFD700'
            obstacle_color = '#9370DB'
            title = "Fantasy Quest"
        
        ax.set_facecolor(bg_color)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        
        # Draw game elements
        ax.text(5, 5, title, fontsize=20, ha='center', color='white')
        ax.plot([1, 9], [1, 1], 'w-', linewidth=2)  # Ground
        
        # Player character
        ax.plot(2, 2, 'o', markersize=15, color=player_color)
        ax.text(2, 2.7, 'You', ha='center', color='white', fontsize=12)
        
        # Goal
        ax.plot(8, 2, 'o', markersize=12, color=goal_color)
        ax.text(8, 2.7, 'Goal', ha='center', color='white', fontsize=12)
        
        # Obstacles
        for i in range(3):
            x = random.uniform(3, 7)
            y = random.uniform(1.5, 2.5)
            ax.plot(x, y, 's', markersize=15, color=obstacle_color)
            ax.text(x, y+0.4, 'Obstacle', ha='center', color='white', fontsize=8)
        
        # Stars
        for i in range(3):
            x = random.uniform(2.5, 7.5)
            y = random.uniform(1.2, 2.8)
            ax.plot(x, y, '*', markersize=15, color='yellow')
            ax.text(x, y+0.4, 'Star', ha='center', color='white', fontsize=8)
        
        # Path
        ax.plot([2, 8], [2, 2], 'y--', linewidth=1, alpha=0.5)
        
        ax.axis('off')
        ax.set_title("Game Preview", fontsize=16, color='white')
        
        # Save to bytes
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor=bg_color)
        buf.seek(0)
        return buf
    except Exception as e:
        st.error(f"Preview generation error: {str(e)}")
        return None

def reset_game_state():
    st.session_state.game_state = {
        "player_pos": [0, 0],
        "goal_pos": [7, 7],
        "obstacles": [[2, 2], [3, 4], [5, 3], [4, 6], [6, 5]],
        "stars": [[1, 1], [3, 3], [5, 5], [7, 1]],
        "score": 0,
        "moves": 0,
        "game_over": False,
        "portals": {
            "A": {"in": [6, 6], "out": [1, 7]},
            "B": {"in": [0, 3], "out": [7, 3]}
        }
    }

# Handle player movement
def move_player(direction):
    """Update player position based on movement direction"""
    state = st.session_state.game_state
    player_pos = state["player_pos"]
    goal_pos = state["goal_pos"]
    obstacles = state["obstacles"]
    stars = state["stars"]
    portals = state["portals"]
    
    new_pos = player_pos.copy()
    
    if direction == "up" and player_pos[0] > 0:
        new_pos[0] -= 1
    elif direction == "down" and player_pos[0] < 7:
        new_pos[0] += 1
    elif direction == "left" and player_pos[1] > 0:
        new_pos[1] -= 1
    elif direction == "right" and player_pos[1] < 7:
        new_pos[1] += 1
        
    # Check if new position is valid
    if new_pos != player_pos:
        # Check for obstacle collision
        if new_pos in obstacles:
            st.session_state.sound_played = "obstacle"
            return
        
        state["player_pos"] = new_pos
        state["moves"] += 1
        st.session_state.sound_played = "click"
        
        # Check for portal
        for portal, positions in portals.items():
            if new_pos == positions["in"]:
                state["player_pos"] = positions["out"].copy()
                state["moves"] += 1  # Count portal as a move
                st.session_state.sound_played = "click"
                break
        
        # Check for goal collision
        if new_pos == goal_pos:
            state["score"] += 20
            state["game_over"] = True
            st.session_state.sound_played = "goal"
        # Check for star collection
        elif new_pos in stars:
            state["score"] += 5
            state["stars"].remove(new_pos)
            st.session_state.sound_played = "star"
                
    st.session_state.game_state = state

# Create a playable game in the browser
def create_playable_game():
    """Create an interactive grid-based game"""
    st.subheader("🎮 Play Your Game Now!")
    
    state = st.session_state.game_state
    player_pos = state["player_pos"]
    goal_pos = state["goal_pos"]
    obstacles = state["obstacles"]
    stars = state["stars"]
    portals = state["portals"]
    
    # Level indicator
    st.markdown(f"""
    <div class="level-indicator">
        Level: {st.session_state.current_level}/{st.session_state.total_levels}
    </div>
    """, unsafe_allow_html=True)
    
    # Score board
    st.markdown(f"""
    <div class="score-board">
        Stars Collected: {state["score"]} &nbsp; | &nbsp; Moves: {state["moves"]}
    </div>
    """, unsafe_allow_html=True)
    
    # Game board
    st.markdown("<div class='game-board'>", unsafe_allow_html=True)
    
    # Create grid cells
    for row in range(8):
        cols = st.columns(8)
        for col in range(8):
            pos = [row, col]
            cell_class = "cell"
            cell_content = ""
            
            if pos == player_pos:
                cell_class += " player"
                cell_content = st.session_state.player_char
            elif pos == goal_pos:
                cell_class += " goal"
                cell_content = st.session_state.goal_char
            elif pos in obstacles:
                cell_class += " obstacle"
                cell_content = st.session_state.obstacle_char
            elif pos in stars:
                cell_class += " star"
                cell_content = "⭐"
            else:
                # Check for portals
                for portal, positions in portals.items():
                    if pos == positions["in"] or pos == positions["out"]:
                        cell_class += " portal"
                        cell_content = "🌀"
                        break
            
            with cols[col]:
                st.markdown(f"<div class='{cell_class}'>{cell_content}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Game controls
    st.markdown("<div class='game-controls'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("↑", key="up", on_click=move_player, args=("up",), use_container_width=True)
    with col2:
        st.button("←", key="left", on_click=move_player, args=("left",), use_container_width=True)
    with col3:
        st.button("↓", key="down", on_click=move_player, args=("down",), use_container_width=True)
    with col4:
        st.button("→", key="right", on_click=move_player, args=("right",), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Reset button
    st.button("🔄 Reset Game", on_click=reset_game_state, use_container_width=True)
    
    # Next level button
    if state["game_over"]:
        st.balloons()
        st.success(f"🎉 You won! Final Score: {state['score']} in {state['moves']} moves!")
        if st.session_state.current_level < st.session_state.total_levels:
            if st.button("Next Level →", use_container_width=True):
                st.session_state.current_level += 1
                reset_game_state()
                st.rerun()
    
    # Play sound if needed
    if st.session_state.sound_played:
        play_sound(st.session_state.sound_played)
        st.session_state.sound_played = False

# Add keyboard controls
def add_keyboard_controls():
    js = """
    <script>
    document.addEventListener('keydown', function(event) {
        const key = event.key;
        const buttons = {
            'ArrowUp': 'up',
            'ArrowLeft': 'left',
            'ArrowDown': 'down',
            'ArrowRight': 'right'
        };
        
        if (buttons[key]) {
            const button = document.querySelector(`button[data-testid="baseButton-${buttons[key]}"]`);
            if (button) {
                button.click();
            }
        }
    });
    </script>
    """
    html(js)

# Theme customizer section
def theme_customizer():
    """Theme customization section"""
    st.markdown("""
    <div class="wave-divider">
        <svg viewBox="0 0 1200 120" preserveAspectRatio="none">
            <path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" opacity=".25" class="shape-fill"></path>
            <path d="M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z" opacity=".5" class="shape-fill"></path>
            <path d="M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z" class="shape-fill"></path>
        </svg>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='theme-customizer'>", unsafe_allow_html=True)
        st.markdown("<div class='customizer-title'>🎨 Customize Your Game Theme</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state.player_char = st.selectbox(
                "Player Character",
                ["🦸", "👨‍🚀", "🧙‍♂️", "🐱", "🐉", "🦊"],
                index=0
            )
            st.markdown(f"<div class='char-preview floating'>{st.session_state.player_char}</div>", unsafe_allow_html=True)
            
        with col2:
            st.session_state.goal_char = st.selectbox(
                "Goal Character",
                ["🏁", "🏰", "🚩", "🎯", "🔑"],
                index=0
            )
            st.markdown(f"<div class='char-preview floating'>{st.session_state.goal_char}</div>", unsafe_allow_html=True)
            
        with col3:
            st.session_state.obstacle_char = st.selectbox(
                "Obstacle Character",
                ["🪨", "🌵", "🔥", "🌊", "🌳"],
                index=0
            )
            st.markdown(f"<div class='char-preview floating'>{st.session_state.obstacle_char}</div>", unsafe_allow_html=True)
        
        st.session_state.current_level = st.slider(
            "Select Difficulty Level",
            1, 5, st.session_state.current_level, step=1
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="wave-divider">
            <svg viewBox="0 0 1200 120" preserveAspectRatio="none">
                <path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" opacity=".25" class="shape-fill"></path>
                <path d="M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z" opacity=".5" class="shape-fill"></path>
                <path d="M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z" class="shape-fill"></path>
            </svg>
        </div>
        """, unsafe_allow_html=True)

# Copy story to clipboard
def copy_story(story_text):
    js = f"""
    <script>
    navigator.clipboard.writeText(`{story_text}`);
    alert("Story copied to clipboard!");
    </script>
    """
    html(js)

# Main application function
def main():
    init_session_state()
    
    st.title("🎮 StoryCoder - Play & Learn Coding!")
    st.markdown("<div class='typewriter'><h2>Turn stories into games, and games into coding skills!</h2></div>", 
                unsafe_allow_html=True)
    
    # Theme customizer
    theme_customizer()
    
    # Create tabs
    st.markdown('<div class="tabs">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("📖 Create Story", use_container_width=True):
            st.session_state.active_tab = "story"
            play_sound("click")
    with col2:
        if st.button("🎮 Play Game", use_container_width=True):
            st.session_state.active_tab = "game"
            play_sound("click")
    with col3:
        if st.button("🔍 Concepts", use_container_width=True):
            st.session_state.active_tab = "concepts"
            play_sound("click")
    with col4:
        if st.button("💻 Game Code", use_container_width=True):
            st.session_state.active_tab = "code"
            play_sound("click")
    with col5:
        if st.button("🔄 New Story", use_container_width=True):
            st.session_state.story = ""
            st.session_state.concepts = []
            st.session_state.game_scenario = ""
            st.session_state.game_code = ""
            st.session_state.game_explanation = ""
            st.session_state.game_preview = None
            st.session_state.active_tab = "story"
            reset_game_state()
            play_sound("click")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Story creation tab
    if st.session_state.active_tab == "story":
        with st.container():
            st.header("📖 Create Your Story")
            st.write("Write a short story (2-5 sentences) and I'll turn it into a playable game!")
            
            # Show examples
            st.subheader("✨ Story Examples")
            col1, col2, col3 = st.columns(3)
            example_stories = {
                "Space Explorer": {
                    "text": "An astronaut needs to collect 3 stars while avoiding asteroids in space. The stars are scattered across different planets. Each star gives special powers to the astronaut. The goal is to collect all stars before returning to Earth.",
                    "image": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=500"
                },
                "Jungle Adventure": {
                    "text": "A monkey swings through trees to collect bananas before sunset. There are dangerous snakes and rivers to avoid. Each banana gives energy to jump higher. Collect 10 bananas to win the game!",
                    "image": "https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=500"
                },
                "Dragon Quest": {
                    "text": "A dragon flies through clouds to collect magic crystals. The crystals are guarded by wizards and hidden in castles. Each crystal makes the dragon stronger. Collect 5 crystals to become the dragon king!",
                    "image": "https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=500"
                }
            }
            
            with col1:
                st.caption("Space Explorer")
                with st.container():
                    st.image(example_stories["Space Explorer"]["image"], 
                             use_container_width=True, 
                             caption="Space Explorer Game")
                    if st.button("Copy Story", key="copy_space", use_container_width=True):
                        st.session_state.story = example_stories["Space Explorer"]["text"]
                        copy_story(example_stories["Space Explorer"]["text"])
            
            with col2:
                st.caption("Jungle Adventure")
                with st.container():
                    st.image(example_stories["Jungle Adventure"]["image"], 
                             use_container_width=True, 
                             caption="Jungle Adventure Game")
                    if st.button("Copy Story", key="copy_jungle", use_container_width=True):
                        st.session_state.story = example_stories["Jungle Adventure"]["text"]
                        copy_story(example_stories["Jungle Adventure"]["text"])
            
            with col3:
                st.caption("Dragon Quest")
                with st.container():
                    st.image(example_stories["Dragon Quest"]["image"], 
                             use_container_width=True, 
                             caption="Dragon Quest Game")
                    if st.button("Copy Story", key="copy_dragon", use_container_width=True):
                        st.session_state.story = example_stories["Dragon Quest"]["text"]
                        copy_story(example_stories["Dragon Quest"]["text"])
            
            story = st.text_area(
                "Your story:",
                height=200,
                placeholder="Once upon a time, a brave knight had to collect 5 magical stars in a castle...",
                value=st.session_state.story,
                key="story_input"
            )
            
            if st.button("✨ Create Game!", use_container_width=True):
                if len(story) < 10:
                    st.error("Your story needs to be at least 10 characters long!")
                else:
                    st.session_state.story = story
                    st.session_state.loading = True
                    play_sound("click")
                    
                    with st.spinner("🧠 Analyzing your story for coding concepts..."):
                        st.session_state.concepts = analyze_story(story)
                    
                    with st.spinner("🎮 Creating your game scenario..."):
                        st.session_state.game_scenario = generate_game_scenario(
                            story, st.session_state.concepts
                        )
                    
                    with st.spinner("📚 Creating coding explanations..."):
                        st.session_state.game_explanation = generate_game_explanation(
                            story, st.session_state.concepts, st.session_state.game_scenario
                        )
                    
                    with st.spinner("🖼️ Generating game preview..."):
                        st.session_state.game_preview = generate_game_preview(story)
                    
                    reset_game_state()
                    st.session_state.active_tab = "game"
                    st.session_state.loading = False
                    st.rerun()
    
    # Game tab
    elif st.session_state.active_tab == "game":
        st.header("🎮 Your Story Game")
        
        if not st.session_state.story:
            st.warning("Please create a story first!")
            st.session_state.active_tab = "story"
            st.rerun()
        
        # Display game scenario
        st.subheader("🌟 Game Scenario")
        st.markdown(f'<div class="game-card">{st.session_state.game_scenario}</div>', unsafe_allow_html=True)
        
        # Display game preview
        st.subheader("🖼️ Game Preview")
        if st.session_state.game_preview:
            st.image(st.session_state.game_preview, use_container_width=True)
        else:
            st.info("Game preview visualization")
            st.image("https://images.unsplash.com/photo-1542751110-97427bbecf20?w=500", use_container_width=True)
        
        # Playable game
        create_playable_game()
        add_keyboard_controls()
        
        # Game explanation
        st.subheader("📚 How This Game Teaches Coding")
        st.markdown(f'<div class="game-card">{st.session_state.game_explanation}</div>', unsafe_allow_html=True)
        
        if st.button("Learn Coding Concepts", use_container_width=True):
            st.session_state.active_tab = "concepts"
            play_sound("click")
            st.rerun()
    
    # Concepts tab
    elif st.session_state.active_tab == "concepts":
        st.header("🔍 Coding Concepts in Your Game")
        st.subheader("Your game teaches these programming concepts:")
        
        if not st.session_state.concepts:
            st.warning("No concepts detected in your story! Try adding words like '3 times', 'if', or 'collect'.")
        else:
            # Concept buttons
            st.subheader("Select a concept to explore:")
            cols = st.columns(len(st.session_state.concepts))
            for i, concept in enumerate(st.session_state.concepts):
                with cols[i]:
                    if st.button(f"{CONCEPTS[concept]['emoji']} {CONCEPTS[concept]['name']}", 
                                key=f"concept_{concept}", use_container_width=True):
                        st.session_state.selected_concept = concept
                        play_sound("click")
            
            # Show explanation for selected concept
            if st.session_state.selected_concept:
                details = CONCEPTS[st.session_state.selected_concept]
                st.markdown(f"""
                <div class="concept-card" style="border-left: 5px solid {details['color']};">
                    <div style="display:flex; align-items:center; gap:15px;">
                        <span style="font-size:36px;">{details['emoji']}</span>
                        <h3 style="color:{details['color']};">{details['name']}</h3>
                    </div>
                    <p>{details['description']}</p>
                    <p><b>In your game:</b> {details['game_example']}</p>
                    <pre style="background:#f0f0f0; padding:10px; border-radius:8px;">{details['example']}</pre>
                </div>
                """, unsafe_allow_html=True)
        
        if st.button("See the Game Code", use_container_width=True):
            st.session_state.active_tab = "code"
            play_sound("click")
            st.rerun()
    
    # Code tab
    elif st.session_state.active_tab == "code":
        st.header("💻 Game Code")
        st.write("Here's the Python code for your game. Download it and run on your computer!")
        
        # Generate simple game code
        if st.session_state.story and st.session_state.concepts:
            # Extract keywords from story
            keywords = re.findall(r'\b\w{4,}\b', st.session_state.story)[:3]
            player_char = keywords[0].capitalize() if keywords else "Hero"
            collect_item = keywords[1] if len(keywords) > 1 else "star"
            obstacle = keywords[2] if len(keywords) > 2 else "rock"
            
            # Get concept emojis
            concept_emojis = "".join([CONCEPTS[c]['emoji'] for c in st.session_state.concepts])
            
            game_code = f"""
# {player_char}'s Adventure: {st.session_state.story[:20]}...
# Teaches: {concept_emojis} {", ".join([CONCEPTS[c]['name'] for c in st.session_state.concepts])}

import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("{player_char}'s Adventure")
clock = pygame.time.Clock()

# Colors
BACKGROUND = (230, 230, 250)  # Light purple
PLAYER_COLOR = (138, 43, 226) # Purple
GOAL_COLOR = (255, 215, 0)    # Gold
OBSTACLE_COLOR = (147, 112, 219) # Medium purple
TEXT_COLOR = (75, 0, 130)     # Indigo
STAR_COLOR = (255, 215, 0)    # Gold

# Player setup
player_size = 40
player_x = 100
player_y = HEIGHT // 2
player_speed = 5

# Goal setup
goal_size = 30
goal_x = WIDTH - 150
goal_y = HEIGHT // 2

# Variables concept: Tracking score
score = 0
font = pygame.font.SysFont(None, 36)

# List concept: Creating obstacles
obstacles = []
for i in range(5):
    obstacles.append([
        random.randint(200, WIDTH - 100),
        random.randint(50, HEIGHT - 100),
        random.randint(30, 70),
        random.randint(20, 50)
    ])

# List concept: Creating stars
stars = []
for i in range(5):
    stars.append([
        random.randint(100, WIDTH - 100),
        random.randint(50, HEIGHT - 100),
        20
    ])

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_y += player_speed
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_speed
    
    # Boundary checking
    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size, player_y))
    
    # Collision detection with goal
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    goal_rect = pygame.Rect(goal_x, goal_y, goal_size, goal_size)
    
    # Conditional concept: Check for collision
    if player_rect.colliderect(goal_rect):
        # Function concept: Increase score
        score += 10
        # Move goal to new position
        goal_x = random.randint(100, WIDTH - 100)
        goal_y = random.randint(50, HEIGHT - 100)
    
    # Collision detection with stars
    for star in stars[:]:
        star_rect = pygame.Rect(star[0], star[1], star[2], star[2])
        if player_rect.colliderect(star_rect):
            score += 5
            stars.remove(star)
    
    # Drawing
    screen.fill(BACKGROUND)
    
    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, OBSTACLE_COLOR, 
                         (obstacle[0], obstacle[1], obstacle[2], obstacle[3]))
    
    # Draw stars
    for star in stars:
        pygame.draw.circle(screen, STAR_COLOR, 
                          (star[0] + star[2]//2, star[1] + star[2]//2), star[2]//2)
    
    # Draw player and goal
    pygame.draw.rect(screen, PLAYER_COLOR, 
                    (player_x, player_y, player_size, player_size))
    pygame.draw.circle(screen, GOAL_COLOR, 
                      (goal_x + goal_size//2, goal_y + goal_size//2), goal_size//2)
    
    # Display score
    score_text = font.render(f"{collect_item.capitalize()}s: {{score}}", True, TEXT_COLOR)
    screen.blit(score_text, (20, 20))
    
    # Display story title
    title_text = font.render(f"{player_char}'s Adventure: {st.session_state.story[:20]}...", True, TEXT_COLOR)
    screen.blit(title_text, (WIDTH // 2 - 150, 20))
    
    # Display concepts
    concepts_text = font.render(f"Teaches: {', '.join([CONCEPTS[c]['name'] for c in st.session_state.concepts])}", True, TEXT_COLOR)
    screen.blit(concepts_text, (20, HEIGHT - 40))
    
    # Display instructions
    help_text = font.render("Arrow keys to move - Collect stars and reach the goal!", True, TEXT_COLOR)
    screen.blit(help_text, (WIDTH // 2 - 200, HEIGHT - 80))
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
"""
            
            # Display code with syntax highlighting
            st.subheader("Your Game Code")
            st.code(game_code, language="python")
            
            # Download button
            st.download_button(
                label="📥 Download Game Code",
                data=game_code,
                file_name="story_game.py",
                mime="text/python",
                use_container_width=True
            )
            
            # Code explanation
            st.subheader("🧠 Code Explanation")
            st.markdown("""
            <div class="game-card">
            <p>This code creates a game based on your story:</p>
            <ul>
                <li><strong>Variables:</strong> Used to track score and positions</li>
                <li><strong>Conditionals:</strong> Check collisions and game rules</li>
                <li><strong>Functions:</strong> pygame functions create the game mechanics</li>
                <li><strong>Loops:</strong> The game loop runs continuously</li>
                <li><strong>Lists:</strong> Store obstacles and collectible stars</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No game code generated yet!")
        
        if st.button("Create Another Story!", use_container_width=True):
            st.session_state.active_tab = "story"
            play_sound("click")
            st.rerun()

if __name__ == "__main__":
    main()
