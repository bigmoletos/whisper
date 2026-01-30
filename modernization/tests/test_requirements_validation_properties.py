"""
Property-based tests for requirements validation engine.

Tests the requirements validation engine using property-based testing
to ensure correctness across a wide range of inputs.
"""

import pytest
from hypothesis import given, strategies as st, assume, settings, HealthCheck

from ..core.spec_compliance import (
    SpecComplianceModule, ValidationResult, EARSPattern
)


class TestRequirementsValidationProperties:
    """Property-based tests for requirements validation."""
    
    @pytest.fixture
    def spec_module(self):
        """Create a SpecComplianceModule instance for testing."""
        return SpecComplianceModule()
    
    @given(
        req_text=st.text(min_size=10, max_size=200),
        req_id=st.text(min_size=3, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc')))
    )
    @settings(max_examples=100, deadline=3000, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_requirements_validation_robustness(self, spec_module, req_text, req_id):
        """
        Feature: vtt-modernization, Property 1: Requirements Generation Compliance
        
        *For any* requirement text input, the validation engine should handle it gracefully
        without crashing and return a valid ValidationResult.
        **Validates: Requirements 1.2**
        """
        # Skip empty or whitespace-only strings
        assume(req_text.strip())
        assume(req_id.strip())
        
        requirements = {
            req_id: {
                'text': req_text,
                'acceptance_criteria': ['Test criterion'],
                'user_story': 'As a user, I want something so that I benefit'
            }
        }
        
        try:
            result = spec_module.validate_requirements(requirements)
            
            # Properties that should always hold
            assert isinstance(result, ValidationResult), "Should return ValidationResult instance"
            assert isinstance(result.is_valid, bool), "is_valid should be boolean"
            assert isinstance(result.errors, list), "errors should be a list"
            assert isinstance(result.warnings, list), "warnings should be a list"
            assert isinstance(result.suggestions, list), "suggestions should be a list"
            assert isinstance(result.quality_score, (int, float)), "quality_score should be numeric"
            assert 0.0 <= result.quality_score <= 1.0, "quality_score should be between 0 and 1"
            assert isinstance(result.incose_compliance, dict), "incose_compliance should be dict"
            
            # If there are errors, is_valid should be False
            if result.errors:
                assert not result.is_valid, "Should be invalid if there are errors"
            
            # Quality score should be 0 if invalid due to errors
            if result.errors and not result.is_valid:
                assert result.quality_score < 1.0, "Quality score should be less than 1.0 if there are errors"
                
        except Exception as e:
            pytest.fail(f"Validation should not raise exceptions for any input: {e}")
    
    @given(
        ears_pattern=st.sampled_from([
            "THE {system} SHALL {action}",
            "WHEN {trigger}, THE {system} SHALL {response}",
            "IF {condition}, THEN THE {system} SHALL {action}",
            "WHILE {state}, THE {system} SHALL {behavior}",
            "WHERE {feature}, THE {system} SHALL {optional_action}"
        ]),
        system_name=st.text(min_size=3, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll'))),
        action=st.text(min_size=5, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Zs')))
    )
    @settings(max_examples=30, deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_ears_pattern_recognition(self, spec_module, ears_pattern, system_name, action):
        """
        Feature: vtt-modernization, Property 1: Requirements Generation Compliance
        
        *For any* properly formatted EARS pattern, the validation engine should
        recognize it as valid and assign the correct pattern type.
        **Validates: Requirements 1.2**
        """
        assume(system_name.strip())
        assume(action.strip())
        assume(not any(char in system_name for char in ['{', '}', '\n', '\r']))
        assume(not any(char in action for char in ['{', '}', '\n', '\r']))
        
        # Create a valid EARS requirement
        if "THE {system} SHALL {action}" in ears_pattern:
            requirement = f"THE {system_name} SHALL {action}"
            expected_pattern = EARSPattern.UBIQUITOUS
        elif "WHEN" in ears_pattern:
            requirement = f"WHEN something happens, THE {system_name} SHALL {action}"
            expected_pattern = EARSPattern.EVENT_DRIVEN
        elif "IF" in ears_pattern:
            requirement = f"IF condition occurs, THEN THE {system_name} SHALL {action}"
            expected_pattern = EARSPattern.UNWANTED_BEHAVIOR
        elif "WHILE" in ears_pattern:
            requirement = f"WHILE in state, THE {system_name} SHALL {action}"
            expected_pattern = EARSPattern.STATE_DRIVEN
        elif "WHERE" in ears_pattern:
            requirement = f"WHERE feature exists, THE {system_name} SHALL {action}"
            expected_pattern = EARSPattern.OPTIONAL
        else:
            requirement = f"THE {system_name} SHALL {action}"
            expected_pattern = EARSPattern.UBIQUITOUS
        
        # Test EARS compliance
        is_compliant = spec_module.ensure_ears_compliance(requirement)
        assert is_compliant, f"Valid EARS pattern should be recognized: {requirement}"
        
        # Test full validation
        requirements = {
            'test_req': {
                'text': requirement,
                'acceptance_criteria': ['System shall meet this criterion'],
                'user_story': 'As a user, I want this so that I benefit'
            }
        }
        
        result = spec_module.validate_requirements(requirements)
        
        # Should be valid and have correct pattern type
        assert result.pattern_type == expected_pattern, f"Should detect correct EARS pattern type for: {requirement}"
        
        # Should have fewer errors for valid EARS patterns
        ears_errors = [error for error in result.errors if 'EARS' in error]
        assert len(ears_errors) == 0, f"Should not have EARS errors for valid pattern: {requirement}"
    
    @given(
        num_requirements=st.integers(min_value=1, max_value=10),
        req_data=st.dictionaries(
            keys=st.text(min_size=1, max_size=10, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
            values=st.dictionaries(
                keys=st.sampled_from(['text', 'acceptance_criteria', 'user_story', 'priority', 'source']),
                values=st.one_of([
                    st.text(min_size=1, max_size=100),
                    st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=5)
                ]),
                min_size=1,
                max_size=5
            ),
            min_size=1,
            max_size=10
        )
    )
    @settings(max_examples=25, deadline=5000, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_validation_consistency(self, spec_module, num_requirements, req_data):
        """
        Feature: vtt-modernization, Property 1: Requirements Generation Compliance
        
        *For any* set of requirements, validation should be consistent and
        the quality score should correlate with the number of issues found.
        **Validates: Requirements 1.2**
        """
        assume(len(req_data) >= 1)
        
        # Clean up the requirements data to ensure it's valid
        cleaned_requirements = {}
        for req_id, data in list(req_data.items())[:num_requirements]:
            if req_id.strip():  # Skip empty requirement IDs
                cleaned_data = {}
                for key, value in data.items():
                    if isinstance(value, str) and value.strip():
                        cleaned_data[key] = value.strip()
                    elif isinstance(value, list) and value:
                        cleaned_data[key] = [item.strip() for item in value if isinstance(item, str) and item.strip()]
                
                if cleaned_data:  # Only add if we have some data
                    cleaned_requirements[req_id.strip()] = cleaned_data
        
        assume(len(cleaned_requirements) >= 1)
        
        # Run validation twice to test consistency
        result1 = spec_module.validate_requirements(cleaned_requirements)
        result2 = spec_module.validate_requirements(cleaned_requirements)
        
        # Results should be identical (consistency property)
        assert result1.is_valid == result2.is_valid, "Validation should be consistent"
        assert result1.quality_score == result2.quality_score, "Quality score should be consistent"
        assert len(result1.errors) == len(result2.errors), "Error count should be consistent"
        assert len(result1.warnings) == len(result2.warnings), "Warning count should be consistent"
        
        # Quality score should be inversely related to number of issues
        total_issues = len(result1.errors) + len(result1.warnings)
        if total_issues == 0:
            assert result1.quality_score > 0.5, "Quality score should be high when no issues found"
        else:
            # More issues should generally mean lower quality score
            assert result1.quality_score >= 0.0, "Quality score should not be negative"
    
    @given(
        acceptance_criteria=st.lists(
            st.text(min_size=5, max_size=100, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Zs', 'Po'))),
            min_size=1,
            max_size=5
        )
    )
    @settings(max_examples=30, deadline=3000, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_acceptance_criteria_testability(self, spec_module, acceptance_criteria):
        """
        Feature: vtt-modernization, Property 1: Requirements Generation Compliance
        
        *For any* acceptance criteria, the testability check should correctly identify
        whether criteria contain testable elements.
        **Validates: Requirements 1.2**
        """
        # Filter out empty or whitespace-only criteria
        valid_criteria = [criterion.strip() for criterion in acceptance_criteria if criterion.strip()]
        assume(len(valid_criteria) >= 1)
        
        requirements = {
            'test_req': {
                'text': 'THE system SHALL do something',
                'acceptance_criteria': valid_criteria,
                'user_story': 'As a user, I want something so that I benefit'
            }
        }
        
        result = spec_module._check_verifiability(requirements)
        
        # Check each criterion for testability
        testable_keywords = ['shall', 'must', 'should', 'will', 'can', 'verify', 'validate', 'test', 'measure']
        
        for criterion in valid_criteria:
            criterion_lower = criterion.lower()
            has_testable_keyword = any(keyword in criterion_lower for keyword in testable_keywords)
            
            if not has_testable_keyword:
                # Should have warnings for non-testable criteria
                testability_warnings = [w for w in result['warnings'] if 'testable' in w.lower()]
                assert len(testability_warnings) > 0, f"Should warn about non-testable criterion: {criterion}"
    
    @given(
        template_name=st.sampled_from(['standard', 'agile', 'technical']),
        title=st.text(min_size=5, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Zs'))),
        version=st.text(min_size=3, max_size=10, alphabet=st.characters(whitelist_categories=('Nd', 'Po')))
    )
    @settings(max_examples=20, deadline=4000, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_document_generation_completeness(self, spec_module, template_name, title, version):
        """
        Feature: vtt-modernization, Property 1: Requirements Generation Compliance
        
        *For any* valid template and document metadata, the document generator should
        produce a complete document with all required sections.
        **Validates: Requirements 1.2, 1.4**
        """
        assume(title.strip())
        assume(version.strip())
        
        requirements_data = {
            'title': title.strip(),
            'version': version.strip(),
            'purpose': 'Test document generation',
            'scope': 'Property-based testing',
            'requirements': {
                'req_1': {
                    'text': 'THE system SHALL work correctly',
                    'acceptance_criteria': ['System functions as expected'],
                    'user_story': 'As a user, I want it to work so that I can use it'
                }
            }
        }
        
        try:
            document = spec_module.generate_requirements_document(requirements_data, template_name)
            
            # Document should have all required fields
            assert document.title == title.strip(), "Title should be preserved"
            assert document.version == version.strip(), "Version should be preserved"
            assert document.date, "Date should be set"
            assert document.introduction, "Introduction should be generated"
            assert isinstance(document.glossary, dict), "Glossary should be a dictionary"
            assert isinstance(document.requirements, dict), "Requirements should be a dictionary"
            assert isinstance(document.metadata, dict), "Metadata should be a dictionary"
            
            # Metadata should contain template information
            assert document.metadata.get('template_used') == template_name, "Template name should be recorded"
            assert 'generation_timestamp' in document.metadata, "Generation timestamp should be recorded"
            assert 'validation_score' in document.metadata, "Validation score should be recorded"
            
            # Requirements should be properly formatted
            for req_id, req_data in document.requirements.items():
                assert 'id' in req_data, "Requirement should have ID"
                assert 'title' in req_data, "Requirement should have title"
                assert 'display_id' in req_data, "Requirement should have display ID"
                
        except Exception as e:
            pytest.fail(f"Document generation should not fail for valid inputs: {e}")
    
    @given(
        export_format=st.sampled_from(['markdown', 'json', 'html'])
    )
    @settings(max_examples=15, deadline=3000, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_document_export_format_validity(self, spec_module, export_format):
        """
        Feature: vtt-modernization, Property 1: Requirements Generation Compliance
        
        *For any* supported export format, the exported document should be valid
        and contain the expected content structure.
        **Validates: Requirements 1.2, 1.4**
        """
        requirements_data = {
            'title': 'Test Document',
            'version': '1.0.0',
            'requirements': {
                'req_1': {
                    'text': 'THE system SHALL export documents',
                    'acceptance_criteria': ['Export works correctly'],
                    'user_story': 'As a user, I want to export so that I can share'
                }
            }
        }
        
        document = spec_module.generate_requirements_document(requirements_data)
        
        # Test export format
        if export_format == 'markdown':
            content = spec_module._export_to_markdown(document)
            assert content.startswith('# Test Document'), "Markdown should start with title"
            assert '## Glossary' in content, "Should contain glossary section"
            assert '## Requirements' in content, "Should contain requirements section"
            
        elif export_format == 'json':
            content = spec_module._export_to_json(document)
            import json
            parsed = json.loads(content)
            assert parsed['title'] == 'Test Document', "JSON should preserve title"
            assert 'requirements' in parsed, "JSON should contain requirements"
            
        elif export_format == 'html':
            content = spec_module._export_to_html(document)
            assert '<!DOCTYPE html>' in content, "HTML should have DOCTYPE"
            assert '<title>Test Document</title>' in content, "HTML should have title tag"
            assert '<h1>Test Document</h1>' in content, "HTML should have main heading"
        
        # Content should not be empty
        assert len(content.strip()) > 100, f"Exported content should be substantial for {export_format}"
    
    @given(
        feature_description=st.text(min_size=10, max_size=100),
        system_name=st.text(min_size=3, max_size=15, alphabet=st.characters(min_codepoint=65, max_codepoint=122)),
        user_role=st.text(min_size=4, max_size=20),
        benefit=st.text(min_size=5, max_size=50)
    )
    @settings(max_examples=100, deadline=10000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.filter_too_much])
    def test_property_requirements_generation_compliance(self, spec_module, feature_description, system_name, user_role, benefit):
        """
        Feature: vtt-modernization, Property 1: Requirements Generation Compliance
        
        *For any* feature description input, the generated requirements document should 
        follow EARS patterns and contain all required INCOSE quality elements.
        **Validates: Requirements 1.2**
        """
        # Filter inputs to ensure they are meaningful but be more permissive
        assume(feature_description.strip())
        assume(system_name.strip())
        assume(user_role.strip())
        assume(benefit.strip())
        assume(len(feature_description.strip()) >= 5)
        assume(len(system_name.strip()) >= 2)
        assume(len(user_role.strip()) >= 3)
        assume(len(benefit.strip()) >= 3)
        
        # Clean inputs
        feature_desc_clean = feature_description.strip()[:50]  # Limit length
        system_name_clean = ''.join(c for c in system_name.strip() if c.isalpha())[:10]
        user_role_clean = user_role.strip()[:15]
        benefit_clean = benefit.strip()[:30]
        
        # Skip if cleaning made them too short
        assume(len(feature_desc_clean) >= 5)
        assume(len(system_name_clean) >= 2)
        assume(len(user_role_clean) >= 3)
        assume(len(benefit_clean) >= 3)
        
        # Generate requirements from feature description
        requirements_data = {
            'title': f'{system_name_clean} Requirements',
            'version': '1.0.0',
            'purpose': f'Define requirements for {feature_desc_clean}',
            'scope': f'Requirements for {system_name_clean} system functionality',
            'requirements': {
                'req_generated': {
                    'title': f'{system_name_clean} Feature Requirement',
                    'text': f'THE {system_name_clean.upper()}_System SHALL {feature_desc_clean.lower()}',
                    'user_story': f'As a {user_role_clean.lower()}, I want {feature_desc_clean.lower()} so that {benefit_clean.lower()}',
                    'acceptance_criteria': [
                        f'THE system SHALL implement {feature_desc_clean.lower()}',
                        f'THE system SHALL provide {benefit_clean.lower()}',
                        f'THE system SHALL validate all inputs correctly'
                    ],
                    'priority': 'High',
                    'source': 'Generated from feature description',
                    'rationale': f'This feature is needed to {benefit_clean.lower()}'
                }
            }
        }
        
        try:
            # Test requirements validation (EARS and INCOSE compliance)
            validation_result = spec_module.validate_requirements(requirements_data['requirements'])
            
            # Property 1: Validation should complete without errors
            assert isinstance(validation_result, ValidationResult), "Should return ValidationResult instance"
            assert isinstance(validation_result.is_valid, bool), "is_valid should be boolean"
            assert isinstance(validation_result.errors, list), "errors should be a list"
            assert isinstance(validation_result.warnings, list), "warnings should be a list"
            assert isinstance(validation_result.suggestions, list), "suggestions should be a list"
            assert isinstance(validation_result.quality_score, (int, float)), "quality_score should be numeric"
            assert 0.0 <= validation_result.quality_score <= 1.0, "quality_score should be between 0 and 1"
            assert isinstance(validation_result.incose_compliance, dict), "incose_compliance should be dict"
            
            # Property 2: EARS pattern compliance should be detected
            # Our generated requirement follows EARS ubiquitous pattern
            ears_compliant = spec_module.ensure_ears_compliance(requirements_data['requirements']['req_generated']['text'])
            assert ears_compliant, f"Generated EARS requirement should be compliant: {requirements_data['requirements']['req_generated']['text']}"
            
            # Property 3: INCOSE quality elements should be present
            # Check that all required INCOSE elements are validated
            incose_rules = ['Completeness', 'Consistency', 'Verifiability', 'Clarity', 'Traceability', 'Feasibility']
            for rule_name in incose_rules:
                assert rule_name in validation_result.incose_compliance, f"INCOSE rule {rule_name} should be checked"
                assert isinstance(validation_result.incose_compliance[rule_name], bool), f"INCOSE {rule_name} result should be boolean"
            
            # Property 4: Document generation should succeed
            document = spec_module.generate_requirements_document(requirements_data)
            # Check document type by checking if it has the expected attributes
            assert hasattr(document, 'title'), "Document should have title attribute"
            assert hasattr(document, 'version'), "Document should have version attribute"
            assert hasattr(document, 'requirements'), "Document should have requirements attribute"
            assert document.title == requirements_data['title'], "Document title should match input"
            assert document.version == requirements_data['version'], "Document version should match input"
            assert document.introduction, "Document should have introduction"
            assert isinstance(document.glossary, dict), "Document should have glossary dict"
            assert isinstance(document.requirements, dict), "Document should have requirements dict"
            assert len(document.requirements) > 0, "Document should contain requirements"
            
            # Property 5: Generated document should contain INCOSE quality metadata
            assert isinstance(document.metadata, dict), "Document should have metadata"
            assert 'validation_score' in document.metadata, "Metadata should include validation score"
            assert 'ears_compliance' in document.metadata, "Metadata should include EARS compliance status"
            assert 'incose_compliance' in document.metadata, "Metadata should include INCOSE compliance details"
            assert 'generation_timestamp' in document.metadata, "Metadata should include generation timestamp"
            
            # Property 6: Export functionality should work for all formats
            for export_format in ['markdown', 'json', 'html']:
                if export_format == 'markdown':
                    content = spec_module._export_to_markdown(document)
                    assert content.startswith(f'# {document.title}'), f"Markdown should start with title"
                    assert '## Requirements' in content, "Markdown should contain requirements section"
                    assert 'EARS' in content or 'ears' in content.lower(), "Should reference EARS patterns"
                    
                elif export_format == 'json':
                    content = spec_module._export_to_json(document)
                    import json
                    parsed = json.loads(content)
                    assert parsed['title'] == document.title, "JSON should preserve title"
                    assert 'requirements' in parsed, "JSON should contain requirements"
                    assert 'metadata' in parsed, "JSON should contain metadata"
                    
                elif export_format == 'html':
                    content = spec_module._export_to_html(document)
                    assert '<!DOCTYPE html>' in content, "HTML should have DOCTYPE"
                    assert f'<title>{document.title}</title>' in content, "HTML should have title tag"
                    assert '<h2>Requirements</h2>' in content, "HTML should have requirements section"
                
                # All formats should contain substantial content
                assert len(content.strip()) > 200, f"Exported {export_format} content should be substantial"
            
            # Property 7: Quality score should reflect compliance level
            if validation_result.is_valid and not validation_result.errors:
                assert validation_result.quality_score > 0.3, "Quality score should be reasonable for valid requirements"
            
            if validation_result.errors:
                assert validation_result.quality_score < 1.0, "Quality score should be reduced when errors present"
            
            # Property 8: User story format should be validated
            user_story = requirements_data['requirements']['req_generated']['user_story']
            is_valid_format = spec_module._is_valid_user_story_format(user_story)
            assert is_valid_format, f"Generated user story should follow standard format: {user_story}"
            
        except Exception as e:
            pytest.fail(f"Requirements generation compliance test should not fail for valid inputs: {e}")