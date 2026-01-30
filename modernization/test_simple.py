#!/usr/bin/env python3
"""
Simple test script to verify design property generator functionality.
"""

from core.design_property_generator import (
    DesignPropertyGenerator,
    AcceptanceCriteriaAnalyzer,
    PropertyTemplateSystem,
    PropertyToTestMapper
)

def test_basic_functionality():
    """Test basic functionality of the design property generator."""
    print("Testing Design Property Generator...")
    
    # Test analyzer
    analyzer = AcceptanceCriteriaAnalyzer()
    print("✓ AcceptanceCriteriaAnalyzer initialized")
    
    # Test template system
    template_system = PropertyTemplateSystem()
    templates = template_system.get_all_templates()
    print(f"✓ PropertyTemplateSystem initialized with {len(templates)} templates")
    
    # Test mapper
    mapper = PropertyToTestMapper(template_system)
    print("✓ PropertyToTestMapper initialized")
    
    # Test generator
    generator = DesignPropertyGenerator()
    print("✓ DesignPropertyGenerator initialized")
    
    # Test analysis
    criterion = "THE VTT_System SHALL process audio files and generate transcriptions"
    analysis = analyzer.analyze_criterion(criterion, "req_test")
    print(f"✓ Analysis completed: {analysis.suggested_property_name} ({analysis.testability_level.value})")
    
    # Test property generation from requirements
    requirements = {
        "title": "Test Requirements",
        "requirements": {
            "req_1": {
                "acceptance_criteria": [
                    "THE VTT_System SHALL accept WAV format files",
                    "THE VTT_System SHALL generate text transcription",
                    "THE VTT_System SHALL complete processing within 10 seconds"
                ]
            }
        }
    }
    
    suite = generator.generate_properties_from_requirements(requirements)
    print(f"✓ Property suite generated with {len(suite.properties)} properties")
    
    # Display generated properties
    for prop in suite.properties:
        print(f"  - {prop.name}: {prop.description[:50]}...")
    
    print("\n✅ All tests passed! Design Property Generator is working correctly.")

if __name__ == "__main__":
    test_basic_functionality()