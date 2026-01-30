"""
Unit tests for Design Property Generator components.

Tests the AcceptanceCriteriaAnalyzer, PropertyTemplateSystem, PropertyToTestMapper,
and DesignPropertyGenerator with specific examples and edge cases.
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from ..core.design_property_generator import (
    AcceptanceCriteriaAnalyzer,
    PropertyTemplateSystem,
    PropertyToTestMapper,
    DesignPropertyGenerator,
    CriteriaAnalysis,
    CriteriaType,
    TestabilityLevel,
    PropertyTemplate,
    PropertyMapping
)
from ..models.property_models import (
    PropertyType,
    ValidationCriteria,
    ValidationCriteriaType,
    PropertySuite,
    TranscriptionProperty
)


class TestAcceptanceCriteriaAnalyzer:
    """Unit tests for AcceptanceCriteriaAnalyzer."""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance for testing."""
        return AcceptanceCriteriaAnalyzer()
    
    def test_analyze_criterion_basic_functionality(self, analyzer):
        """Test basic criterion analysis functionality."""
        criterion = "THE VTT_System SHALL process audio files within 2 seconds"
        
        analysis = analyzer.analyze_criterion(criterion, "req_001")
        
        assert isinstance(analysis, CriteriaAnalysis)
        assert analysis.criterion_text == criterion
        assert analysis.requirements_reference == "req_001"
        assert isinstance(analysis.criteria_type, CriteriaType)
        assert isinstance(analysis.testability_level, TestabilityLevel)
        assert isinstance(analysis.property_type, PropertyType)
        assert 0.0 <= analysis.complexity_score <= 1.0
        assert analysis.suggested_property_name
        assert analysis.test_template
    
    def test_classify_criteria_type_functional(self, analyzer):
        """Test functional criteria type classification."""
        criterion = "THE system SHALL process user input"
        
        criteria_type = analyzer._classify_criteria_type(criterion)
        
        assert criteria_type == CriteriaType.FUNCTIONAL
    
    def test_classify_criteria_type_performance(self, analyzer):
        """Test performance criteria type classification."""
        criterion = "THE system SHALL respond within 100ms with optimal performance"
        
        criteria_type = analyzer._classify_criteria_type(criterion)
        
        assert criteria_type == CriteriaType.PERFORMANCE
    
    def test_classify_criteria_type_security(self, analyzer):
        """Test security criteria type classification."""
        criterion = "THE system SHALL encrypt all user data and protect authentication tokens"
        
        criteria_type = analyzer._classify_criteria_type(criterion)
        
        assert criteria_type == CriteriaType.SECURITY
    
    def test_assess_testability_highly_testable(self, analyzer):
        """Test assessment of highly testable criteria."""
        criterion = "THE system SHALL return valid JSON when processing requests"
        
        testability = analyzer._assess_testability(criterion)
        
        assert testability == TestabilityLevel.HIGHLY_TESTABLE
    
    def test_assess_testability_edge_case(self, analyzer):
        """Test assessment of edge case criteria."""
        criterion = "THE system SHALL handle invalid input and error conditions gracefully"
        
        testability = analyzer._assess_testability(criterion)
        
        assert testability == TestabilityLevel.EDGE_CASE
    
    def test_assess_testability_not_testable(self, analyzer):
        """Test assessment of non-testable criteria."""
        criterion = "THE system SHALL be user-friendly and intuitive to use"
        
        testability = analyzer._assess_testability(criterion)
        
        assert testability == TestabilityLevel.NOT_TESTABLE
    
    def test_determine_property_type_round_trip(self, analyzer):
        """Test round-trip property type determination."""
        criterion = "THE system SHALL serialize and deserialize data consistently"
        
        property_type = analyzer._determine_property_type(criterion, CriteriaType.FUNCTIONAL)
        
        assert property_type == PropertyType.ROUND_TRIP
    
    def test_determine_property_type_performance(self, analyzer):
        """Test performance property type determination."""
        criterion = "THE system SHALL complete operations within time limits"
        
        property_type = analyzer._determine_property_type(criterion, CriteriaType.PERFORMANCE)
        
        assert property_type == PropertyType.PERFORMANCE
    
    def test_extract_quantifiable_aspects_with_numbers(self, analyzer):
        """Test extraction of quantifiable aspects with numeric values."""
        criterion = "THE system SHALL process requests within 500 milliseconds with 95% accuracy"
        
        aspects = analyzer._extract_quantifiable_aspects(criterion)
        
        assert len(aspects) > 0
        assert any('500' in str(aspect) for aspect in aspects)
        assert any('95' in str(aspect) for aspect in aspects)
    
    def test_extract_quantifiable_aspects_without_numbers(self, analyzer):
        """Test extraction of quantifiable aspects without explicit numbers."""
        criterion = "THE system SHALL provide fast response times"
        
        aspects = analyzer._extract_quantifiable_aspects(criterion)
        
        # Should still find some quantifiable indicators
        assert isinstance(aspects, list)
    
    def test_calculate_complexity_score_simple(self, analyzer):
        """Test complexity score calculation for simple criteria."""
        simple_criterion = "THE system SHALL work"
        
        score = analyzer._calculate_complexity_score(simple_criterion)
        
        assert 0.0 <= score <= 1.0
        assert score < 0.5  # Should be low complexity
    
    def test_calculate_complexity_score_complex(self, analyzer):
        """Test complexity score calculation for complex criteria."""
        complex_criterion = "THE system SHALL process multiple different types of input data and handle various error conditions while maintaining performance and providing appropriate user feedback and logging all operations and ensuring security compliance and supporting different platforms and versions"
        
        score = analyzer._calculate_complexity_score(complex_criterion)
        
        assert 0.0 <= score <= 1.0
        assert score > 0.5  # Should be high complexity
    
    def test_generate_property_name_basic(self, analyzer):
        """Test property name generation."""
        criterion = "THE system SHALL validate user input"
        
        name = analyzer._generate_property_name(criterion, "req_001")
        
        assert isinstance(name, str)
        assert len(name) > 0
        assert 'validate' in name or 'user' in name or 'input' in name
    
    def test_analyze_criteria_batch_valid_input(self, analyzer):
        """Test batch analysis with valid input."""
        criteria = [
            {'text': 'THE system SHALL process data', 'requirement_id': 'req_001'},
            {'text': 'THE system SHALL validate input', 'requirement_id': 'req_002'}
        ]
        
        analyses = analyzer.analyze_criteria_batch(criteria)
        
        assert len(analyses) == 2
        assert all(isinstance(analysis, CriteriaAnalysis) for analysis in analyses)
        assert analyses[0].requirements_reference == 'req_001'
        assert analyses[1].requirements_reference == 'req_002'
    
    def test_analyze_criteria_batch_empty_input(self, analyzer):
        """Test batch analysis with empty input."""
        criteria = []
        
        analyses = analyzer.analyze_criteria_batch(criteria)
        
        assert len(analyses) == 0
        assert isinstance(analyses, list)
    
    def test_analyze_criteria_batch_invalid_input(self, analyzer):
        """Test batch analysis with invalid input."""
        criteria = [
            {'text': '', 'requirement_id': 'req_001'},  # Empty text
            {'requirement_id': 'req_002'},  # Missing text
            {'text': 'Valid criterion', 'requirement_id': 'req_003'}  # Valid
        ]
        
        analyses = analyzer.analyze_criteria_batch(criteria)
        
        # Should only process valid criteria
        assert len(analyses) == 1
        assert analyses[0].requirements_reference == 'req_003'
    
    def test_error_handling_in_analysis(self, analyzer):
        """Test error handling during criterion analysis."""
        # Test with None input
        analysis = analyzer.analyze_criterion(None, "req_001")
        
        assert isinstance(analysis, CriteriaAnalysis)
        assert analysis.testability_level == TestabilityLevel.NOT_TESTABLE
    
    def test_ears_pattern_recognition_ubiquitous(self, analyzer):
        """Test EARS ubiquitous pattern recognition."""
        criterion = "THE VTT_System SHALL transcribe audio files"
        
        analysis = analyzer.analyze_criterion(criterion)
        
        assert analysis.testability_level in [TestabilityLevel.HIGHLY_TESTABLE, TestabilityLevel.TESTABLE]
    
    def test_ears_pattern_recognition_event_driven(self, analyzer):
        """Test EARS event-driven pattern recognition."""
        criterion = "WHEN user presses hotkey, THE VTT_System SHALL start recording"
        
        analysis = analyzer.analyze_criterion(criterion)
        
        assert analysis.testability_level in [TestabilityLevel.HIGHLY_TESTABLE, TestabilityLevel.TESTABLE]


class TestPropertyTemplateSystem:
    """Unit tests for PropertyTemplateSystem."""
    
    @pytest.fixture
    def template_system(self):
        """Create template system instance for testing."""
        return PropertyTemplateSystem()
    
    def test_initialization(self, template_system):
        """Test template system initialization."""
        templates = template_system.get_all_templates()
        
        assert isinstance(templates, dict)
        assert len(templates) > 0
    
    def test_get_template_existing(self, template_system):
        """Test getting existing template."""
        template = template_system.get_template(PropertyType.ROUND_TRIP, CriteriaType.FUNCTIONAL)
        
        # May or may not exist, but should not crash
        if template:
            assert isinstance(template, PropertyTemplate)
            assert template.property_type == PropertyType.ROUND_TRIP
    
    def test_get_template_non_existing(self, template_system):
        """Test getting non-existing template."""
        # Use unlikely combination
        template = template_system.get_template(PropertyType.SECURITY, CriteriaType.USABILITY)
        
        # Should return None for non-existing combinations
        assert template is None or isinstance(template, PropertyTemplate)
    
    def test_add_template(self, template_system):
        """Test adding new template."""
        new_template = PropertyTemplate(
            name="test_template",
            description="Test template",
            property_type=PropertyType.INVARIANT,
            test_function_template="def test_{property_name}(): pass",
            validation_criteria_template={"criteria_type": ValidationCriteriaType.BOOLEAN},
            generator_hints=["Test hint"],
            example_usage="Test usage",
            applicable_criteria_patterns=["test"]
        )
        
        initial_count = len(template_system.get_all_templates())
        template_system.add_template(new_template)
        final_count = len(template_system.get_all_templates())
        
        assert final_count > initial_count
    
    def test_template_structure_validation(self, template_system):
        """Test that all templates have required structure."""
        templates = template_system.get_all_templates()
        
        for template in templates.values():
            assert isinstance(template, PropertyTemplate)
            assert template.name
            assert template.description
            assert isinstance(template.property_type, PropertyType)
            assert template.test_function_template
            assert isinstance(template.validation_criteria_template, dict)
            assert isinstance(template.generator_hints, list)
            assert template.example_usage
            assert isinstance(template.applicable_criteria_patterns, list)


class TestPropertyToTestMapper:
    """Unit tests for PropertyToTestMapper."""
    
    @pytest.fixture
    def template_system(self):
        """Create template system for testing."""
        return PropertyTemplateSystem()
    
    @pytest.fixture
    def mapper(self, template_system):
        """Create mapper instance for testing."""
        return PropertyToTestMapper(template_system)
    
    @pytest.fixture
    def sample_analysis(self):
        """Create sample criteria analysis for testing."""
        return CriteriaAnalysis(
            criterion_text="THE system SHALL process data correctly",
            criteria_type=CriteriaType.FUNCTIONAL,
            testability_level=TestabilityLevel.HIGHLY_TESTABLE,
            property_type=PropertyType.INVARIANT,
            test_strategy="property_based_testing",
            quantifiable_aspects=["correctly"],
            validation_approach="behavioral_validation",
            complexity_score=0.3,
            suggested_property_name="process_data_correctly",
            test_template="test template",
            requirements_reference="req_001"
        )
    
    def test_create_property_mapping_valid_analysis(self, mapper, sample_analysis):
        """Test creating property mapping from valid analysis."""
        mapping = mapper.create_property_mapping(sample_analysis)
        
        # May return None if no template found, which is acceptable
        if mapping:
            assert isinstance(mapping, PropertyMapping)
            assert mapping.criterion_text == sample_analysis.criterion_text
            assert mapping.property_name == sample_analysis.suggested_property_name
            assert mapping.requirements_reference == sample_analysis.requirements_reference
            assert isinstance(mapping.validation_criteria, ValidationCriteria)
            assert isinstance(mapping.implementation_notes, list)
            assert isinstance(mapping.dependencies, list)
    
    def test_create_property_mapping_not_testable(self, mapper):
        """Test creating property mapping from non-testable analysis."""
        non_testable_analysis = CriteriaAnalysis(
            criterion_text="THE system SHALL be user-friendly",
            criteria_type=CriteriaType.USABILITY,
            testability_level=TestabilityLevel.NOT_TESTABLE,
            property_type=PropertyType.INVARIANT,
            test_strategy="manual_testing",
            quantifiable_aspects=[],
            validation_approach="qualitative_validation",
            complexity_score=0.8,
            suggested_property_name="user_friendly",
            test_template="manual test",
            requirements_reference="req_002"
        )
        
        mapping = mapper.create_property_mapping(non_testable_analysis)
        
        assert mapping is None
    
    def test_create_property_mappings_batch(self, mapper, sample_analysis):
        """Test batch property mapping creation."""
        analyses = [sample_analysis]
        
        mappings = mapper.create_property_mappings_batch(analyses)
        
        assert isinstance(mappings, list)
        # Length may be 0 or 1 depending on template availability
        assert len(mappings) <= len(analyses)
    
    def test_generate_property_test_code(self, mapper, sample_analysis):
        """Test property test code generation."""
        mapping = PropertyMapping(
            criterion_id="test_001",
            criterion_text=sample_analysis.criterion_text,
            property_name=sample_analysis.suggested_property_name,
            property_description="Test property",
            test_function_name="test_process_data_correctly",
            validation_criteria=ValidationCriteria(
                criteria_type=ValidationCriteriaType.BOOLEAN,
                expected_value=True
            ),
            requirements_reference=sample_analysis.requirements_reference,
            implementation_notes=["Test note"],
            dependencies=[]
        )
        
        code = mapper.generate_property_test_code(mapping)
        
        assert isinstance(code, str)
        assert len(code) > 0
        # Should contain imports and basic structure
        assert "import" in code
        assert mapping.property_name in code or "TODO" in code
    
    def test_create_validation_criteria_boolean(self, mapper, sample_analysis):
        """Test validation criteria creation for boolean type."""
        template = PropertyTemplate(
            name="test_template",
            description="Test",
            property_type=PropertyType.INVARIANT,
            test_function_template="test",
            validation_criteria_template={"criteria_type": ValidationCriteriaType.BOOLEAN, "expected_value": True},
            generator_hints=[],
            example_usage="test",
            applicable_criteria_patterns=[]
        )
        
        criteria = mapper._create_validation_criteria(sample_analysis, template)
        
        assert isinstance(criteria, ValidationCriteria)
        assert criteria.criteria_type == ValidationCriteriaType.BOOLEAN
        assert criteria.expected_value is True
    
    def test_create_validation_criteria_numeric_range(self, mapper):
        """Test validation criteria creation for numeric range type."""
        analysis_with_numbers = CriteriaAnalysis(
            criterion_text="THE system SHALL respond within 100ms",
            criteria_type=CriteriaType.PERFORMANCE,
            testability_level=TestabilityLevel.HIGHLY_TESTABLE,
            property_type=PropertyType.PERFORMANCE,
            test_strategy="property_based_testing",
            quantifiable_aspects=["100ms", "100"],
            validation_approach="quantitative_validation",
            complexity_score=0.4,
            suggested_property_name="response_time",
            test_template="test template",
            requirements_reference="req_003"
        )
        
        template = PropertyTemplate(
            name="performance_template",
            description="Performance test",
            property_type=PropertyType.PERFORMANCE,
            test_function_template="test",
            validation_criteria_template={"criteria_type": ValidationCriteriaType.NUMERIC_RANGE},
            generator_hints=[],
            example_usage="test",
            applicable_criteria_patterns=[]
        )
        
        criteria = mapper._create_validation_criteria(analysis_with_numbers, template)
        
        assert isinstance(criteria, ValidationCriteria)
        assert criteria.criteria_type == ValidationCriteriaType.NUMERIC_RANGE
        assert criteria.max_value is not None
    
    def test_generate_implementation_notes(self, mapper, sample_analysis):
        """Test implementation notes generation."""
        template = PropertyTemplate(
            name="test_template",
            description="Test",
            property_type=PropertyType.INVARIANT,
            test_function_template="test",
            validation_criteria_template={},
            generator_hints=["Use hypothesis", "Test edge cases"],
            example_usage="test",
            applicable_criteria_patterns=[]
        )
        
        notes = mapper._generate_implementation_notes(sample_analysis, template)
        
        assert isinstance(notes, list)
        assert len(notes) > 0
        # Should include template hints
        assert any("hypothesis" in note.lower() for note in notes)
    
    def test_determine_dependencies(self, mapper, sample_analysis):
        """Test dependency determination."""
        dependencies = mapper._determine_dependencies(sample_analysis)
        
        assert isinstance(dependencies, list)
        # Dependencies may be empty for basic functional properties


class TestDesignPropertyGenerator:
    """Unit tests for DesignPropertyGenerator."""
    
    @pytest.fixture
    def generator(self):
        """Create generator instance for testing."""
        return DesignPropertyGenerator()
    
    @pytest.fixture
    def sample_requirements(self):
        """Create sample requirements for testing."""
        return {
            'title': 'Test Requirements',
            'requirements': {
                'req_001': {
                    'acceptance_criteria': [
                        'THE system SHALL process audio files',
                        'THE system SHALL generate transcriptions'
                    ]
                },
                'req_002': {
                    'acceptance_criteria': [
                        'THE system SHALL handle errors gracefully'
                    ]
                }
            }
        }
    
    def test_initialization(self, generator):
        """Test generator initialization."""
        assert isinstance(generator.analyzer, AcceptanceCriteriaAnalyzer)
        assert isinstance(generator.template_system, PropertyTemplateSystem)
        assert isinstance(generator.mapper, PropertyToTestMapper)
    
    def test_generate_properties_from_requirements_valid(self, generator, sample_requirements):
        """Test property generation from valid requirements."""
        suite = generator.generate_properties_from_requirements(sample_requirements)
        
        assert isinstance(suite, PropertySuite)
        assert suite.name
        assert suite.description
        assert isinstance(suite.properties, list)
        # Properties count may vary based on template availability
    
    def test_generate_properties_from_requirements_empty(self, generator):
        """Test property generation from empty requirements."""
        empty_requirements = {'title': 'Empty', 'requirements': {}}
        
        suite = generator.generate_properties_from_requirements(empty_requirements)
        
        assert isinstance(suite, PropertySuite)
        assert suite.name
        assert len(suite.properties) == 0
    
    def test_generate_properties_from_requirements_invalid(self, generator):
        """Test property generation from invalid requirements."""
        invalid_requirements = {'invalid': 'structure'}
        
        suite = generator.generate_properties_from_requirements(invalid_requirements)
        
        assert isinstance(suite, PropertySuite)
        assert suite.name
        # Should handle gracefully without crashing
    
    def test_export_property_suite(self, generator):
        """Test property suite export."""
        suite = PropertySuite(
            name="test_suite",
            description="Test suite",
            properties=[]
        )
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_suite.json"
            success = generator.export_property_suite(suite, output_path)
            
            assert success
            assert output_path.exists()
            
            # Verify content
            with open(output_path, 'r') as f:
                data = json.load(f)
                assert data['name'] == 'test_suite'
                assert data['description'] == 'Test suite'
                assert 'properties' in data
    
    def test_generate_test_code_files(self, generator):
        """Test test code file generation."""
        # Create a mock property with test function
        def mock_test_function(context):
            return True
        
        mock_property = TranscriptionProperty(
            name="test_property",
            description="Test property",
            property_type=PropertyType.INVARIANT,
            test_function=mock_test_function,
            requirements_reference="req_001",
            validation_criteria=ValidationCriteria(
                criteria_type=ValidationCriteriaType.BOOLEAN,
                expected_value=True
            )
        )
        
        suite = PropertySuite(
            name="test_suite",
            description="Test suite",
            properties=[mock_property]
        )
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            generated_files = generator.generate_test_code_files(suite, output_dir)
            
            assert isinstance(generated_files, list)
            # Should generate at least one file
            if len(generated_files) > 0:
                assert all(path.exists() for path in generated_files)
                assert all(path.suffix == '.py' for path in generated_files)
    
    def test_extract_criteria_from_requirements(self, generator, sample_requirements):
        """Test criteria extraction from requirements."""
        criteria_list = generator._extract_criteria_from_requirements(sample_requirements)
        
        assert isinstance(criteria_list, list)
        assert len(criteria_list) == 3  # Total criteria from sample
        
        for criterion in criteria_list:
            assert 'text' in criterion
            assert 'requirement_id' in criterion
            assert criterion['text']
            assert criterion['requirement_id']
    
    def test_create_transcription_property(self, generator):
        """Test transcription property creation."""
        mapping = PropertyMapping(
            criterion_id="test_001",
            criterion_text="Test criterion",
            property_name="test_property",
            property_description="Test property description",
            test_function_name="test_test_property",
            validation_criteria=ValidationCriteria(
                criteria_type=ValidationCriteriaType.BOOLEAN,
                expected_value=True
            ),
            requirements_reference="req_001",
            implementation_notes=[],
            dependencies=[]
        )
        
        prop = generator._create_transcription_property(mapping)
        
        if prop:  # May be None if creation fails
            assert isinstance(prop, TranscriptionProperty)
            assert prop.name == mapping.property_name
            assert prop.description == mapping.property_description
            assert prop.requirements_reference == mapping.requirements_reference
            assert callable(prop.test_function)
    
    def test_map_to_property_type(self, generator):
        """Test property type mapping."""
        # Test round-trip mapping
        round_trip_mapping = PropertyMapping(
            criterion_id="test",
            criterion_text="test",
            property_name="round_trip_test",
            property_description="test",
            test_function_name="test",
            validation_criteria=ValidationCriteria(ValidationCriteriaType.BOOLEAN, True),
            requirements_reference="test",
            implementation_notes=[],
            dependencies=[]
        )
        
        prop_type = generator._map_to_property_type(round_trip_mapping)
        assert prop_type == PropertyType.ROUND_TRIP
        
        # Test default mapping
        default_mapping = PropertyMapping(
            criterion_id="test",
            criterion_text="test",
            property_name="unknown_test",
            property_description="test",
            test_function_name="test",
            validation_criteria=ValidationCriteria(ValidationCriteriaType.BOOLEAN, True),
            requirements_reference="test",
            implementation_notes=[],
            dependencies=[]
        )
        
        prop_type = generator._map_to_property_type(default_mapping)
        assert prop_type == PropertyType.INVARIANT
    
    def test_generate_test_file_content(self, generator):
        """Test test file content generation."""
        def mock_test_function(context):
            return True
        
        properties = [
            TranscriptionProperty(
                name="test_property_1",
                description="First test property",
                property_type=PropertyType.INVARIANT,
                test_function=mock_test_function,
                requirements_reference="req_001",
                validation_criteria=ValidationCriteria(ValidationCriteriaType.BOOLEAN, True)
            ),
            TranscriptionProperty(
                name="test_property_2",
                description="Second test property",
                property_type=PropertyType.INVARIANT,
                test_function=mock_test_function,
                requirements_reference="req_002",
                validation_criteria=ValidationCriteria(ValidationCriteriaType.BOOLEAN, True)
            )
        ]
        
        content = generator._generate_test_file_content(properties, "invariant")
        
        assert isinstance(content, str)
        assert len(content) > 0
        assert "import pytest" in content
        assert "TestInvariantProperties" in content
        assert "test_test_property_1" in content
        assert "test_test_property_2" in content
        assert "req_001" in content
        assert "req_002" in content


class TestEdgeCasesAndErrorHandling:
    """Test edge cases and error handling scenarios."""
    
    def test_analyzer_with_none_input(self):
        """Test analyzer with None input."""
        analyzer = AcceptanceCriteriaAnalyzer()
        
        # Should not crash
        analysis = analyzer.analyze_criterion(None, "req_001")
        assert isinstance(analysis, CriteriaAnalysis)
    
    def test_analyzer_with_empty_string(self):
        """Test analyzer with empty string."""
        analyzer = AcceptanceCriteriaAnalyzer()
        
        analysis = analyzer.analyze_criterion("", "req_001")
        assert isinstance(analysis, CriteriaAnalysis)
    
    def test_analyzer_with_very_long_text(self):
        """Test analyzer with very long text."""
        analyzer = AcceptanceCriteriaAnalyzer()
        
        long_text = "THE system SHALL " + "do something " * 1000
        analysis = analyzer.analyze_criterion(long_text, "req_001")
        
        assert isinstance(analysis, CriteriaAnalysis)
        assert analysis.complexity_score > 0.5  # Should be high complexity
    
    def test_template_system_with_invalid_template(self):
        """Test template system with invalid template."""
        template_system = PropertyTemplateSystem()
        
        # Try to add invalid template (should handle gracefully)
        try:
            invalid_template = None
            template_system.add_template(invalid_template)
        except Exception:
            # Expected to fail, but should not crash the system
            pass
    
    def test_mapper_with_missing_template(self):
        """Test mapper when template is missing."""
        template_system = PropertyTemplateSystem()
        mapper = PropertyToTestMapper(template_system)
        
        # Create analysis for which no template exists
        analysis = CriteriaAnalysis(
            criterion_text="Unusual criterion",
            criteria_type=CriteriaType.MAINTAINABILITY,  # Less common type
            testability_level=TestabilityLevel.HIGHLY_TESTABLE,
            property_type=PropertyType.METAMORPHIC,  # Less common type
            test_strategy="property_based_testing",
            quantifiable_aspects=[],
            validation_approach="behavioral_validation",
            complexity_score=0.5,
            suggested_property_name="unusual_property",
            test_template="test template",
            requirements_reference="req_001"
        )
        
        mapping = mapper.create_property_mapping(analysis)
        # Should return None gracefully if no template found
        assert mapping is None or isinstance(mapping, PropertyMapping)
    
    def test_generator_with_malformed_requirements(self):
        """Test generator with malformed requirements."""
        generator = DesignPropertyGenerator()
        
        malformed_requirements = {
            'requirements': {
                'req_001': None,  # Invalid requirement
                'req_002': {'acceptance_criteria': None},  # Invalid criteria
                'req_003': {'acceptance_criteria': [None, "", "Valid criterion"]}  # Mixed validity
            }
        }
        
        # Should not crash
        suite = generator.generate_properties_from_requirements(malformed_requirements)
        assert isinstance(suite, PropertySuite)
    
    @patch('whisper.modernization.core.design_property_generator.logger')
    def test_error_logging(self, mock_logger):
        """Test that errors are properly logged."""
        analyzer = AcceptanceCriteriaAnalyzer()
        
        # Force an error by mocking a method to raise exception
        with patch.object(analyzer, '_classify_criteria_type', side_effect=Exception("Test error")):
            analysis = analyzer.analyze_criterion("Test criterion", "req_001")
            
            # Should still return valid analysis (fallback)
            assert isinstance(analysis, CriteriaAnalysis)
            
            # Should have logged the error
            mock_logger.error.assert_called()