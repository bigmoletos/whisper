"""
Unit tests for the Spec Compliance Module.

Tests the requirements validation engine, EARS pattern validation,
INCOSE quality rule checkers, and requirements document generator.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from ..core.spec_compliance import (
    SpecComplianceModule, ValidationResult, EARSPattern,
    RequirementsDocument, DocumentTemplate
)


class TestSpecComplianceModule:
    """Test cases for the Spec Compliance Module."""
    
    @pytest.fixture
    def spec_module(self):
        """Create a SpecComplianceModule instance for testing."""
        return SpecComplianceModule()
    
    @pytest.fixture
    def sample_requirements(self):
        """Sample requirements data for testing."""
        return {
            'req_1': {
                'title': 'Audio Processing Requirement',
                'text': 'THE VTT_System SHALL process audio files in real-time',
                'user_story': 'As a user, I want real-time audio processing so that I can get immediate transcription results',
                'acceptance_criteria': [
                    'THE system SHALL process audio with latency less than 500ms',
                    'THE system SHALL support WAV and MP3 formats',
                    'THE system SHALL handle audio files up to 60 minutes'
                ],
                'priority': 'High',
                'source': 'User Requirements Document',
                'rationale': 'Real-time processing is essential for user experience'
            },
            'req_2': {
                'title': 'Fallback Mechanism',
                'text': 'WHEN primary transcription engine fails, THE VTT_System SHALL automatically switch to backup engine',
                'user_story': 'As a user, I want automatic fallback so that transcription continues even if one engine fails',
                'acceptance_criteria': [
                    'THE system SHALL detect engine failures within 2 seconds',
                    'THE system SHALL switch to backup engine automatically',
                    'THE system SHALL log all fallback events'
                ],
                'priority': 'High',
                'source': 'Reliability Requirements'
            }
        }
    
    @pytest.fixture
    def invalid_requirements(self):
        """Invalid requirements data for testing validation."""
        return {
            'bad_req_1': {
                'text': 'The system should maybe do something',  # No EARS pattern
                'acceptance_criteria': []  # Empty criteria
            },
            'bad_req_2': {
                'title': 'Incomplete Requirement',
                # Missing text, user_story, acceptance_criteria
            }
        }
    
    def test_validate_requirements_valid_input(self, spec_module, sample_requirements):
        """Test validation with valid requirements."""
        result = spec_module.validate_requirements(sample_requirements)
        
        assert isinstance(result, ValidationResult)
        assert result.is_valid
        assert result.quality_score > 0.5
        assert result.pattern_type in [EARSPattern.UBIQUITOUS, EARSPattern.EVENT_DRIVEN]
        assert len(result.errors) == 0
    
    def test_validate_requirements_invalid_input(self, spec_module, invalid_requirements):
        """Test validation with invalid requirements."""
        result = spec_module.validate_requirements(invalid_requirements)
        
        assert isinstance(result, ValidationResult)
        assert not result.is_valid
        assert len(result.errors) > 0
        assert len(result.warnings) > 0
        assert len(result.suggestions) > 0
        assert result.quality_score < 0.5
    
    def test_ears_pattern_validation_ubiquitous(self, spec_module):
        """Test EARS ubiquitous pattern validation."""
        requirement = "THE VTT_System SHALL transcribe audio files"
        
        assert spec_module.ensure_ears_compliance(requirement)
    
    def test_ears_pattern_validation_event_driven(self, spec_module):
        """Test EARS event-driven pattern validation."""
        requirement = "WHEN user presses hotkey, THE VTT_System SHALL start recording"
        
        assert spec_module.ensure_ears_compliance(requirement)
    
    def test_ears_pattern_validation_invalid(self, spec_module):
        """Test EARS pattern validation with invalid input."""
        requirement = "The system should do something"
        
        assert not spec_module.ensure_ears_compliance(requirement)
    
    def test_incose_completeness_check(self, spec_module, sample_requirements):
        """Test INCOSE completeness quality rule."""
        result = spec_module._check_completeness(sample_requirements)
        
        assert result['is_valid']
        assert len(result['warnings']) == 0
    
    def test_incose_completeness_check_incomplete(self, spec_module, invalid_requirements):
        """Test INCOSE completeness check with incomplete requirements."""
        result = spec_module._check_completeness(invalid_requirements)
        
        assert not result['is_valid']
        assert len(result['warnings']) > 0
        assert len(result['suggestions']) > 0
    
    def test_incose_verifiability_check(self, spec_module, sample_requirements):
        """Test INCOSE verifiability quality rule."""
        result = spec_module._check_verifiability(sample_requirements)
        
        assert result['is_valid']
        assert len(result['warnings']) == 0
    
    def test_incose_clarity_check(self, spec_module):
        """Test INCOSE clarity quality rule."""
        requirements_with_clarity_issues = {
            'req_1': {
                'text': 'THE system SHALL do this and that and the other thing and also handle various edge cases and provide appropriate responses and maintain good performance and ensure user satisfaction and implement proper error handling',
                'acceptance_criteria': ['It should work properly']
            }
        }
        
        result = spec_module._check_clarity(requirements_with_clarity_issues)
        
        assert not result['is_valid']
        assert len(result['warnings']) > 0
        assert any('complex sentence' in warning for warning in result['warnings'])
    
    def test_generate_design_properties(self, spec_module, sample_requirements):
        """Test generation of design properties from requirements."""
        properties = spec_module.generate_design_properties(sample_requirements)
        
        assert len(properties) > 0
        
        for prop in properties:
            assert prop.name
            assert prop.description
            assert prop.requirements_reference in sample_requirements
            assert prop.test_function_template
    
    def test_create_task_breakdown(self, spec_module):
        """Test creation of task breakdown from design."""
        design_data = {
            'components': {
                'Audio Processor': {
                    'description': 'Processes audio input',
                    'requirements': ['req_1'],
                    'effort': 'Large'
                }
            },
            'properties': [
                {
                    'name': 'Audio Processing Property',
                    'description': 'Test audio processing behavior',
                    'requirements_reference': 'req_1'
                }
            ]
        }
        
        task_list = spec_module.create_task_breakdown(design_data)
        
        assert task_list.total_tasks > 0
        assert len(task_list.tasks) > 0
        assert task_list.estimated_duration
        
        # Check that tasks were created for components and properties
        task_titles = [task.title for task in task_list.tasks]
        assert any('Audio Processor' in title for title in task_titles)
    
    def test_generate_requirements_document(self, spec_module, sample_requirements):
        """Test requirements document generation."""
        requirements_data = {
            'title': 'VTT System Requirements',
            'version': '1.0.0',
            'purpose': 'Define VTT system requirements',
            'scope': 'Voice-to-text transcription functionality',
            'requirements': sample_requirements
        }
        
        document = spec_module.generate_requirements_document(requirements_data)
        
        assert isinstance(document, RequirementsDocument)
        assert document.title == 'VTT System Requirements'
        assert document.version == '1.0.0'
        assert document.introduction
        assert document.glossary
        assert len(document.requirements) == len(sample_requirements)
        assert document.metadata
    
    def test_export_requirements_document_markdown(self, spec_module, sample_requirements):
        """Test exporting requirements document to Markdown."""
        requirements_data = {
            'title': 'Test Requirements',
            'version': '1.0.0',
            'requirements': sample_requirements
        }
        
        document = spec_module.generate_requirements_document(requirements_data)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / 'requirements.md'
            success = spec_module.export_requirements_document(document, output_path, 'markdown')
            
            assert success
            assert output_path.exists()
            
            content = output_path.read_text(encoding='utf-8')
            assert '# Test Requirements' in content
            assert 'Version:' in content
            assert 'Glossary' in content
            assert 'Requirements' in content
    
    def test_export_requirements_document_json(self, spec_module, sample_requirements):
        """Test exporting requirements document to JSON."""
        requirements_data = {
            'title': 'Test Requirements',
            'version': '1.0.0',
            'requirements': sample_requirements
        }
        
        document = spec_module.generate_requirements_document(requirements_data)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / 'requirements.json'
            success = spec_module.export_requirements_document(document, output_path, 'json')
            
            assert success
            assert output_path.exists()
            
            import json
            content = json.loads(output_path.read_text(encoding='utf-8'))
            assert content['title'] == 'Test Requirements'
            assert content['version'] == '1.0.0'
            assert 'requirements' in content
    
    def test_export_requirements_document_html(self, spec_module, sample_requirements):
        """Test exporting requirements document to HTML."""
        requirements_data = {
            'title': 'Test Requirements',
            'version': '1.0.0',
            'requirements': sample_requirements
        }
        
        document = spec_module.generate_requirements_document(requirements_data)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / 'requirements.html'
            success = spec_module.export_requirements_document(document, output_path, 'html')
            
            assert success
            assert output_path.exists()
            
            content = output_path.read_text(encoding='utf-8')
            assert '<!DOCTYPE html>' in content
            assert '<title>Test Requirements</title>' in content
            assert '<h1>Test Requirements</h1>' in content
    
    def test_document_template_retrieval(self, spec_module):
        """Test document template retrieval."""
        template = spec_module._get_document_template('standard')
        
        assert isinstance(template, DocumentTemplate)
        assert template.name == 'Standard Requirements Document'
        assert 'introduction' in template.sections
        assert 'requirements' in template.sections
    
    def test_user_story_format_validation(self, spec_module):
        """Test user story format validation."""
        valid_story = "As a user, I want to transcribe audio so that I can convert speech to text"
        invalid_story = "User wants transcription functionality"
        
        assert spec_module._is_valid_user_story_format(valid_story)
        assert not spec_module._is_valid_user_story_format(invalid_story)
    
    def test_ears_suggestions_generation(self, spec_module):
        """Test EARS pattern suggestions generation."""
        invalid_req = "The system should do something"
        suggestions = spec_module._generate_ears_suggestions(invalid_req, 'req_1')
        
        assert len(suggestions) > 0
        assert any('SHALL' in suggestion for suggestion in suggestions)
        assert any('EARS' in suggestion for suggestion in suggestions)
    
    def test_error_handling_in_validation(self, spec_module):
        """Test error handling during validation."""
        # Test with malformed requirements data
        malformed_requirements = {
            'req_1': None,  # Invalid requirement data
            'req_2': {'text': 123}  # Invalid text type
        }
        
        result = spec_module.validate_requirements(malformed_requirements)
        
        # Should not crash and should return a result
        assert isinstance(result, ValidationResult)
        # May not be valid due to malformed data
        assert len(result.errors) > 0 or len(result.warnings) > 0


class TestEARSPatternValidation:
    """Specific tests for EARS pattern validation."""
    
    @pytest.fixture
    def spec_module(self):
        return SpecComplianceModule()
    
    @pytest.mark.parametrize("requirement,expected", [
        ("THE VTT_System SHALL process audio files", True),
        ("WHEN user clicks button, THE system SHALL respond", True),
        ("IF error occurs, THEN THE system SHALL log it", True),
        ("WHILE recording, THE system SHALL monitor levels", True),
        ("WHERE GPU available, THE system SHALL use acceleration", True),
        ("The system should do something", False),
        ("System processes audio", False),
        ("", False)
    ])
    def test_ears_pattern_validation_cases(self, spec_module, requirement, expected):
        """Test various EARS pattern validation cases."""
        result = spec_module.ensure_ears_compliance(requirement)
        assert result == expected


class TestINCOSEQualityRules:
    """Specific tests for INCOSE quality rules."""
    
    @pytest.fixture
    def spec_module(self):
        return SpecComplianceModule()
    
    def test_feasibility_check_high_risk_terms(self, spec_module):
        """Test feasibility check with high-risk terms."""
        requirements = {
            'req_1': {
                'text': 'THE system SHALL provide real-time response with 100% accuracy',
                'acceptance_criteria': ['System never fails']
            }
        }
        
        result = spec_module._check_feasibility(requirements)
        
        assert not result['is_valid']
        assert len(result['warnings']) > 0
        assert any('high-risk terms' in warning for warning in result['warnings'])
    
    def test_traceability_check_missing_rationale(self, spec_module):
        """Test traceability check with missing rationale."""
        requirements = {
            'req_1': {
                'text': 'THE system SHALL do something',
                'user_story': 'As a user, I want something',
                'acceptance_criteria': ['It works']
                # Missing rationale and source
            }
        }
        
        result = spec_module._check_traceability(requirements)
        
        assert not result['is_valid']
        assert len(result['warnings']) > 0
        assert any('rationale' in warning for warning in result['warnings'])
        assert any('source' in warning for warning in result['warnings'])