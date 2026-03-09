"""
Image and Diagram Generation Module
Generates diagram prompts and descriptions for ML concepts
"""

import os
from utils.genai_utils import generate_visual_description


def generate_diagram_prompt(topic: str) -> dict:
    """
    Generate a detailed prompt for creating diagrams of ML concepts
    Uses Gemini AI to create comprehensive visual descriptions
    
    Args:
        topic (str): The ML concept to create a diagram for
        
    Returns:
        dict: Contains 'success' status, 'prompt', 'description', and optional 'error'
    """
    try:
        # Get visual description from Gemini
        result = generate_visual_description(topic)
        
        if not result['success']:
            return result
        
        description = result['description']
        
        # Create a structured diagram prompt
        diagram_prompt = f"""
        Create a detailed educational diagram for: {topic}
        
        {description}
        
        Style Guidelines:
        - Use a clean, professional educational style
        - Include clear labels and annotations
        - Use arrows to show flow and relationships
        - Apply color coding for different components
        - Make it suitable for students learning ML
        """
        
        return {
            'success': True,
            'prompt': diagram_prompt,
            'description': description,
            'topic': topic,
            'message': 'Diagram prompt generated successfully'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Error generating diagram prompt: {str(e)}'
        }


def generate_mermaid_diagram(topic: str) -> dict:
    """
    Generate Mermaid.js syntax for creating flowcharts and diagrams
    
    Args:
        topic (str): The ML concept to visualize
        
    Returns:
        dict: Contains 'success' status, 'mermaid_code', and optional 'error'
    """
    try:
        # Predefined Mermaid diagrams for common ML topics
        mermaid_templates = {
            'neural network': """
graph LR
    A[Input Layer] --> B[Hidden Layer 1]
    B --> C[Hidden Layer 2]
    C --> D[Output Layer]
    style A fill:#e1f5ff
    style B fill:#fff9e1
    style C fill:#fff9e1
    style D fill:#e7ffe1
""",
            'backpropagation': """
graph TB
    A[Forward Pass] --> B[Calculate Loss]
    B --> C[Compute Gradients]
    C --> D[Backward Pass]
    D --> E[Update Weights]
    E --> F{Converged?}
    F -->|No| A
    F -->|Yes| G[Training Complete]
    style A fill:#e1f5ff
    style B fill:#ffe1e1
    style C fill:#fff9e1
    style D fill:#ffe1f5
    style E fill:#e1ffe1
    style G fill:#c8ffc8
""",
            'gradient descent': """
graph TB
    A[Initialize Parameters] --> B[Calculate Loss]
    B --> C[Compute Gradient]
    C --> D[Update Parameters]
    D --> E{Stopping Criteria?}
    E -->|No| B
    E -->|Yes| F[Optimal Parameters]
    style A fill:#e1f5ff
    style B fill:#ffe1e1
    style C fill:#fff9e1
    style D fill:#e1ffe1
    style F fill:#c8ffc8
""",
            'decision tree': """
graph TD
    A[Root Node] --> B{Feature 1}
    B -->|True| C{Feature 2}
    B -->|False| D[Class A]
    C -->|True| E[Class B]
    C -->|False| F[Class C]
    style A fill:#e1f5ff
    style B fill:#fff9e1
    style C fill:#fff9e1
    style D fill:#c8ffc8
    style E fill:#c8ffc8
    style F fill:#c8ffc8
"""
        }
        
        # Check if we have a predefined template
        topic_lower = topic.lower()
        mermaid_code = None
        
        for key, template in mermaid_templates.items():
            if key in topic_lower:
                mermaid_code = template
                break
        
        # If no template found, create a generic diagram description
        if not mermaid_code:
            mermaid_code = f"""
graph LR
    A[Start: {topic}] --> B[Process Data]
    B --> C[Apply Algorithm]
    C --> D[Generate Output]
    style A fill:#e1f5ff
    style B fill:#fff9e1
    style C fill:#ffe1f5
    style D fill:#c8ffc8
"""
        
        return {
            'success': True,
            'mermaid_code': mermaid_code,
            'topic': topic,
            'message': 'Mermaid diagram generated successfully'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Error generating Mermaid diagram: {str(e)}'
        }


def get_diagram_suggestions(topic: str) -> dict:
    """
    Get suggestions for different types of diagrams that could be created
    
    Args:
        topic (str): The ML concept
        
    Returns:
        dict: Contains suggested diagram types and tools
    """
    suggestions = {
        'success': True,
        'topic': topic,
        'diagram_types': [
            {
                'type': 'Flowchart',
                'description': 'Show the step-by-step process or algorithm flow',
                'tools': ['Mermaid.js', 'Draw.io', 'Lucidchart']
            },
            {
                'type': 'Architecture Diagram',
                'description': 'Visualize the structure of neural networks or model architecture',
                'tools': ['NN-SVG', 'PlotNeuralNet', 'TensorBoard']
            },
            {
                'type': 'Data Flow Diagram',
                'description': 'Illustrate how data moves through the system',
                'tools': ['Mermaid.js', 'Graphviz']
            },
            {
                'type': 'Concept Map',
                'description': 'Show relationships between different ML concepts',
                'tools': ['XMind', 'MindMeister']
            }
        ],
        'recommended_tool': 'Mermaid.js (integrated in this application)'
    }
    
    return suggestions
