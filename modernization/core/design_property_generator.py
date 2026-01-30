"""
Design Property Generator for VTT System Modernization

This module implements the design property generator that creates correctness
properties from acceptance criteria and maps them to testable implementations.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import re
from pathlib import Path
import json

try:
    from ..models.property_models import (
        TranscriptionProperty, PropertyType, ValidationCriteria, 
        ValidationCriteriaType, PropertySuite
    )
except ImportError:
    # Fallback for direct execution
    from models.property_models import (
        TranscriptionProperty, PropertyType, ValidationCriteria, 
        ValidationCriteriaType, PropertySuite
    )

logger = logging.getLogger(__name__)


class CriteriaType(Enum):
    """Types of acceptance criteria for analysis."""
    FUNCTIONAL = "functional"
    PERFORMANCE = "performance"
    SECURITY = "security"
    USABILITY = "usability"
    RELIABILITY = "reliability"
    COMPATIBILITY = "compatibility"
    MAINTAINABILITY = "maintainability"


class TestabilityLevel(Enum):
    """Levels of testability for acceptance criteria."""
    HIGHLY_TESTABLE = "highly_testable"  # Can be directly tested with property-based testing
    TESTABLE = "testable"  # Can be tested with unit tests and examples
    EDGE_CASE = "edge_case"  # Requires specific edge case testing
    NOT_TESTABLE = "not_testable"  # Cannot be automatically tested


@dataclass
class CriteriaAnalysis:
    """Analysis result for an acceptance criterion."""
    criterion_text: str
    criteria_type: CriteriaType
    testability_level: TestabilityLevel
    property_type: PropertyType
    test_strategy: str
    quantifiable_aspects: List[str]
    validation_approach: str
    complexity_score: float  # 0.0 to 1.0
    suggested_property_name: str
    test_template: str
    requirements_reference: str
    
    def is_property_testable(self) -> bool:
        """Check if criterion can be tested with property-based testing."""
        return self.testability_level in [TestabilityLevel.HIGHLY_TESTABLE, TestabilityLevel.TESTABLE]


@dataclass
class PropertyTemplate:
    """Template for generating property tests."""
    name: str
    description: str
    property_type: PropertyType
    test_function_template: str
    validation_criteria_template: Dict[str, Any]
    generator_hints: List[str]
    example_usage: str
    applicable_criteria_patterns: List[str]


@dataclass
class PropertyMapping:
    """Mapping between acceptance criteria and property tests."""
    criterion_id: str
    criterion_text: str
    property_name: str
    property_description: str
    test_function_name: str
    validation_criteria: ValidationCriteria
    requirements_reference: str
    implementation_notes: List[str]
    dependencies: List[str]


class AcceptanceCriteriaAnalyzer:
    """
    Analyzes acceptance criteria to determine testability and appropriate
    testing strategies.
    """
    
    def __init__(self):
        """Initialize the analyzer with pattern definitions."""
        self.functional_patterns = self._initialize_functional_patterns()
        self.performance_patterns = self._initialize_performance_patterns()
        self.security_patterns = self._initialize_security_patterns()
        self.quantifiable_indicators = self._initialize_quantifiable_indicators()
        
        logger.info("Acceptance Criteria Analyzer initialized")
    
    def analyze_criterion(self, 
                         criterion_text: str, 
                         requirements_reference: str = "") -> CriteriaAnalysis:
        """
        Analyze a single acceptance criterion.
        
        Args:
            criterion_text: The acceptance criterion text to analyze
            requirements_reference: Reference to the parent requirement
            
        Returns:
            CriteriaAnalysis with detailed analysis results
        """
        logger.debug(f"Analyzing criterion: {criterion_text[:50]}...")
        
        try:
            # Determine criteria type
            criteria_type = self._classify_criteria_type(criterion_text)
            
            # Assess testability
            testability_level = self._assess_testability(criterion_text)
            
            # Determine property type
            property_type = self._determine_property_type(criterion_text, criteria_type)
            
            # Extract quantifiable aspects
            quantifiable_aspects = self._extract_quantifiable_aspects(criterion_text)
            
            # Calculate complexity score
            complexity_score = self._calculate_complexity_score(criterion_text)
            
            # Generate property name
            suggested_property_name = self._generate_property_name(criterion_text, requirements_reference)
            
            # Determine test strategy and validation approach
            test_strategy = self._determine_test_strategy(testability_level, property_type)
            validation_approach = self._determine_validation_approach(criteria_type, quantifiable_aspects)
            
            # Generate test template
            test_template = self._generate_test_template(property_type, test_strategy)
            
            analysis = CriteriaAnalysis(
                criterion_text=criterion_text,
                criteria_type=criteria_type,
                testability_level=testability_level,
                property_type=property_type,
                test_strategy=test_strategy,
                quantifiable_aspects=quantifiable_aspects,
                validation_approach=validation_approach,
                complexity_score=complexity_score,
                suggested_property_name=suggested_property_name,
                test_template=test_template,
                requirements_reference=requirements_reference
            )
            
            logger.debug(f"Analysis completed: {analysis.suggested_property_name} ({analysis.testability_level.value})")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing criterion: {e}", exc_info=True)
            # Return a basic analysis as fallback
            return CriteriaAnalysis(
                criterion_text=criterion_text,
                criteria_type=CriteriaType.FUNCTIONAL,
                testability_level=TestabilityLevel.NOT_TESTABLE,
                property_type=PropertyType.INVARIANT,
                test_strategy="manual_testing",
                quantifiable_aspects=[],
                validation_approach="manual_validation",
                complexity_score=1.0,
                suggested_property_name="unknown_property",
                test_template="# Manual test required",
                requirements_reference=requirements_reference
            )
    
    def analyze_criteria_batch(self, 
                              criteria: List[Dict[str, Any]]) -> List[CriteriaAnalysis]:
        """
        Analyze multiple acceptance criteria.
        
        Args:
            criteria: List of criteria dictionaries with 'text' and optional 'requirement_id'
            
        Returns:
            List of CriteriaAnalysis results
        """
        logger.info(f"Analyzing batch of {len(criteria)} criteria")
        
        analyses = []
        for criterion in criteria:
            criterion_text = criterion.get('text', '')
            requirement_id = criterion.get('requirement_id', '')
            
            if criterion_text.strip():
                analysis = self.analyze_criterion(criterion_text, requirement_id)
                analyses.append(analysis)
        
        logger.info(f"Completed batch analysis: {len(analyses)} results")
        return analyses
    
    def _classify_criteria_type(self, criterion_text: str) -> CriteriaType:
        """Classify the type of acceptance criterion."""
        text_lower = criterion_text.lower()
        
        # Performance indicators
        if any(pattern in text_lower for pattern in self.performance_patterns):
            return CriteriaType.PERFORMANCE
        
        # Security indicators
        if any(pattern in text_lower for pattern in self.security_patterns):
            return CriteriaType.SECURITY
        
        # Usability indicators
        usability_patterns = ['user', 'interface', 'experience', 'usable', 'intuitive', 'accessible']
        if any(pattern in text_lower for pattern in usability_patterns):
            return CriteriaType.USABILITY
        
        # Reliability indicators
        reliability_patterns = ['reliable', 'stable', 'available', 'uptime', 'failure', 'recovery']
        if any(pattern in text_lower for pattern in reliability_patterns):
            return CriteriaType.RELIABILITY
        
        # Compatibility indicators
        compatibility_patterns = ['compatible', 'support', 'platform', 'version', 'browser', 'device']
        if any(pattern in text_lower for pattern in compatibility_patterns):
            return CriteriaType.COMPATIBILITY
        
        # Maintainability indicators
        maintainability_patterns = ['maintain', 'extend', 'modify', 'update', 'configure', 'document']
        if any(pattern in text_lower for pattern in maintainability_patterns):
            return CriteriaType.MAINTAINABILITY
        
        # Default to functional
        return CriteriaType.FUNCTIONAL
    
    def _assess_testability(self, criterion_text: str) -> TestabilityLevel:
        """Assess how testable a criterion is."""
        # Check for empty or whitespace-only text first
        if not criterion_text or not criterion_text.strip():
            return TestabilityLevel.NOT_TESTABLE
            
        text_lower = criterion_text.lower()
        
        # Highly testable indicators
        highly_testable_patterns = [
            'shall return', 'shall produce', 'shall generate', 'shall calculate',
            'shall validate', 'shall verify', 'shall process', 'shall convert',
            'shall parse', 'shall serialize', 'shall deserialize'
        ]
        
        if any(pattern in text_lower for pattern in highly_testable_patterns):
            return TestabilityLevel.HIGHLY_TESTABLE
        
        # Testable indicators
        testable_patterns = [
            'shall', 'must', 'will', 'should', 'can be', 'is able to',
            'responds to', 'handles', 'supports', 'provides'
        ]
        
        if any(pattern in text_lower for pattern in testable_patterns):
            # Check for quantifiable aspects
            if self._has_quantifiable_aspects(criterion_text):
                return TestabilityLevel.HIGHLY_TESTABLE
            return TestabilityLevel.TESTABLE
        
        # Edge case indicators
        edge_case_patterns = [
            'error', 'exception', 'failure', 'invalid', 'boundary', 'limit',
            'maximum', 'minimum', 'empty', 'null', 'zero'
        ]
        
        if any(pattern in text_lower for pattern in edge_case_patterns):
            return TestabilityLevel.EDGE_CASE
        
        # Not testable indicators
        not_testable_patterns = [
            'user-friendly', 'intuitive', 'easy to use', 'appropriate',
            'suitable', 'reasonable', 'adequate', 'good', 'better'
        ]
        
        if any(pattern in text_lower for pattern in not_testable_patterns):
            return TestabilityLevel.NOT_TESTABLE
        
        return TestabilityLevel.TESTABLE
    
    def _determine_property_type(self, criterion_text: str, criteria_type: CriteriaType) -> PropertyType:
        """Determine the appropriate property type for testing."""
        text_lower = criterion_text.lower()
        
        # Round-trip patterns
        if any(pattern in text_lower for pattern in ['serialize', 'deserialize', 'convert', 'parse', 'format']):
            return PropertyType.ROUND_TRIP
        
        # Performance patterns
        if criteria_type == CriteriaType.PERFORMANCE or any(pattern in text_lower for pattern in self.performance_patterns):
            return PropertyType.PERFORMANCE
        
        # Security patterns
        if criteria_type == CriteriaType.SECURITY or any(pattern in text_lower for pattern in self.security_patterns):
            return PropertyType.SECURITY
        
        # Error handling patterns
        if any(pattern in text_lower for pattern in ['error', 'exception', 'failure', 'invalid', 'fallback']):
            return PropertyType.ERROR_HANDLING
        
        # Metamorphic patterns (relationships between inputs/outputs)
        if any(pattern in text_lower for pattern in ['relationship', 'proportion', 'ratio', 'relative', 'compared']):
            return PropertyType.METAMORPHIC
        
        # Default to invariant
        return PropertyType.INVARIANT
    
    def _extract_quantifiable_aspects(self, criterion_text: str) -> List[str]:
        """Extract quantifiable aspects from criterion text."""
        quantifiable_aspects = []
        
        # Look for numeric values and units
        numeric_patterns = [
            r'\d+\s*(seconds?|minutes?|hours?|ms|milliseconds?)',  # Time
            r'\d+\s*(bytes?|kb|mb|gb|tb)',  # Size
            r'\d+\s*(%|percent)',  # Percentage
            r'\d+\s*(requests?|operations?|transactions?)',  # Count
            r'(less than|greater than|at least|at most|within|between)\s+\d+',  # Comparisons
            r'\d+\.\d+',  # Decimal numbers
            r'\d+'  # Integers
        ]
        
        for pattern in numeric_patterns:
            matches = re.findall(pattern, criterion_text, re.IGNORECASE)
            quantifiable_aspects.extend(matches)
        
        # Look for quantifiable indicators
        for indicator in self.quantifiable_indicators:
            if indicator in criterion_text.lower():
                quantifiable_aspects.append(indicator)
        
        return list(set(quantifiable_aspects))  # Remove duplicates
    
    def _has_quantifiable_aspects(self, criterion_text: str) -> bool:
        """Check if criterion has quantifiable aspects."""
        return len(self._extract_quantifiable_aspects(criterion_text)) > 0
    
    def _calculate_complexity_score(self, criterion_text: str) -> float:
        """Calculate complexity score (0.0 = simple, 1.0 = complex)."""
        score = 0.0
        
        # Length factor
        word_count = len(criterion_text.split())
        if word_count > 20:
            score += 0.3
        elif word_count > 10:
            score += 0.1
        
        # Complexity indicators
        complex_patterns = [
            'and', 'or', 'but', 'however', 'unless', 'except', 'provided',
            'multiple', 'various', 'different', 'complex', 'sophisticated'
        ]
        
        complexity_count = sum(1 for pattern in complex_patterns if pattern in criterion_text.lower())
        score += min(complexity_count * 0.1, 0.4)
        
        # Conditional complexity
        conditional_patterns = ['if', 'when', 'while', 'where', 'unless']
        conditional_count = sum(1 for pattern in conditional_patterns if pattern in criterion_text.lower())
        score += min(conditional_count * 0.15, 0.3)
        
        return min(score, 1.0)
    
    def _generate_property_name(self, criterion_text: str, requirements_reference: str) -> str:
        """Generate a suggested property name."""
        # Extract key words from criterion
        words = re.findall(r'\b\w+\b', criterion_text.lower())
        
        # Filter out common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'shall', 'must', 'will', 'should', 'can', 'be', 'is', 'are', 'was', 'were'}
        key_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Take first few meaningful words
        name_parts = key_words[:3] if key_words else ['property']
        
        # Add requirement reference if available
        if requirements_reference:
            req_suffix = requirements_reference.lower().replace(' ', '_').replace('.', '_')
            name_parts.append(req_suffix)
        
        return '_'.join(name_parts)
    
    def _determine_test_strategy(self, testability_level: TestabilityLevel, property_type: PropertyType) -> str:
        """Determine the appropriate test strategy."""
        if testability_level == TestabilityLevel.HIGHLY_TESTABLE:
            return "property_based_testing"
        elif testability_level == TestabilityLevel.TESTABLE:
            if property_type in [PropertyType.ROUND_TRIP, PropertyType.INVARIANT]:
                return "property_based_testing"
            else:
                return "unit_testing_with_examples"
        elif testability_level == TestabilityLevel.EDGE_CASE:
            return "edge_case_testing"
        else:
            return "manual_testing"
    
    def _determine_validation_approach(self, criteria_type: CriteriaType, quantifiable_aspects: List[str]) -> str:
        """Determine the validation approach."""
        if quantifiable_aspects:
            return "quantitative_validation"
        elif criteria_type in [CriteriaType.FUNCTIONAL, CriteriaType.RELIABILITY]:
            return "behavioral_validation"
        elif criteria_type == CriteriaType.PERFORMANCE:
            return "performance_validation"
        elif criteria_type == CriteriaType.SECURITY:
            return "security_validation"
        else:
            return "qualitative_validation"
    
    def _generate_test_template(self, property_type: PropertyType, test_strategy: str) -> str:
        """Generate a test template based on property type and strategy."""
        if test_strategy == "property_based_testing":
            if property_type == PropertyType.ROUND_TRIP:
                return """
@given(data=...)
def test_{property_name}(self, data):
    # Round-trip test
    processed = process_data(data)
    recovered = reverse_process(processed)
    assert data == recovered
"""
            elif property_type == PropertyType.INVARIANT:
                return """
@given(data=...)
def test_{property_name}(self, data):
    # Invariant test
    result = system_function(data)
    assert invariant_condition(result)
"""
            elif property_type == PropertyType.PERFORMANCE:
                return """
@given(data=...)
def test_{property_name}(self, data):
    # Performance test
    start_time = time.time()
    result = system_function(data)
    end_time = time.time()
    assert (end_time - start_time) < max_allowed_time
"""
            else:
                return """
@given(data=...)
def test_{property_name}(self, data):
    # Property test
    result = system_function(data)
    assert property_condition(result)
"""
        else:
            return """
def test_{property_name}(self):
    # Unit test with specific examples
    test_data = create_test_data()
    result = system_function(test_data)
    assert expected_condition(result)
"""
    
    def _initialize_functional_patterns(self) -> List[str]:
        """Initialize patterns for functional criteria."""
        return [
            'process', 'handle', 'manage', 'execute', 'perform',
            'create', 'generate', 'produce', 'calculate', 'compute',
            'validate', 'verify', 'check', 'confirm', 'ensure',
            'store', 'save', 'retrieve', 'load', 'fetch',
            'send', 'receive', 'transmit', 'communicate',
            'display', 'show', 'present', 'render'
        ]
    
    def _initialize_performance_patterns(self) -> List[str]:
        """Initialize patterns for performance criteria."""
        return [
            'performance', 'speed', 'fast', 'quick', 'rapid',
            'latency', 'response time', 'throughput', 'bandwidth',
            'memory', 'cpu', 'resource', 'efficient', 'optimize',
            'scalable', 'concurrent', 'parallel', 'load',
            'within', 'less than', 'under', 'maximum', 'minimum'
        ]
    
    def _initialize_security_patterns(self) -> List[str]:
        """Initialize patterns for security criteria."""
        return [
            'security', 'secure', 'protect', 'authentication', 'authorization',
            'encrypt', 'decrypt', 'hash', 'token', 'credential',
            'access control', 'permission', 'privilege', 'audit',
            'privacy', 'confidential', 'integrity', 'availability'
        ]
    
    def _initialize_quantifiable_indicators(self) -> List[str]:
        """Initialize indicators of quantifiable aspects."""
        return [
            'accuracy', 'precision', 'recall', 'f1-score',
            'uptime', 'availability', 'reliability',
            'count', 'number', 'quantity', 'amount',
            'rate', 'frequency', 'interval', 'duration',
            'size', 'length', 'width', 'height', 'volume',
            'temperature', 'pressure', 'voltage', 'current'
        ]


class PropertyTemplateSystem:
    """
    Manages templates for generating property tests from acceptance criteria.
    """
    
    def __init__(self):
        """Initialize the template system."""
        self.templates = self._initialize_templates()
        logger.info("Property Template System initialized")
    
    def get_template(self, property_type: PropertyType, criteria_type: CriteriaType) -> Optional[PropertyTemplate]:
        """
        Get appropriate template for property type and criteria type.
        
        Args:
            property_type: Type of property to test
            criteria_type: Type of acceptance criteria
            
        Returns:
            PropertyTemplate if found, None otherwise
        """
        template_key = f"{property_type.value}_{criteria_type.value}"
        return self.templates.get(template_key)
    
    def get_all_templates(self) -> Dict[str, PropertyTemplate]:
        """Get all available templates."""
        return self.templates.copy()
    
    def add_template(self, template: PropertyTemplate) -> None:
        """Add a new template to the system."""
        # Generate key from template properties
        template_key = f"{template.property_type.value}_{template.name}"
        self.templates[template_key] = template
        logger.info(f"Added template: {template_key}")
    
    def _initialize_templates(self) -> Dict[str, PropertyTemplate]:
        """Initialize the built-in property templates."""
        templates = {}
        
        # Round-trip templates
        templates["round_trip_functional"] = PropertyTemplate(
            name="round_trip_functional",
            description="Round-trip property for data serialization/deserialization",
            property_type=PropertyType.ROUND_TRIP,
            test_function_template="""
def test_{property_name}(self, data):
    '''Property: Round-trip consistency for {description}'''
    # Serialize data
    serialized = serialize_function(data)
    
    # Deserialize back
    deserialized = deserialize_function(serialized)
    
    # Assert round-trip consistency
    assert data == deserialized, f"Round-trip failed: {data} != {deserialized}"
""",
            validation_criteria_template={
                "criteria_type": ValidationCriteriaType.BOOLEAN,
                "expected_value": True
            },
            generator_hints=[
                "Use hypothesis.strategies for data generation",
                "Consider edge cases like empty data, large data",
                "Test with various data types and formats"
            ],
            example_usage="Test audio format conversion round-trip consistency",
            applicable_criteria_patterns=[
                "serialize", "deserialize", "convert", "parse", "format", "encode", "decode"
            ]
        )
        
        # Invariant templates
        templates["invariant_functional"] = PropertyTemplate(
            name="invariant_functional",
            description="Invariant property for system behavior",
            property_type=PropertyType.INVARIANT,
            test_function_template="""
def test_{property_name}(self, data):
    '''Property: Invariant condition for {description}'''
    # Execute system function
    result = system_function(data)
    
    # Check invariant condition
    assert invariant_condition(result), f"Invariant violated for input: {data}"
    
    # Additional invariant checks
    assert result is not None, "Result should not be None"
    assert isinstance(result, expected_type), f"Result type mismatch: {type(result)}"
""",
            validation_criteria_template={
                "criteria_type": ValidationCriteriaType.BOOLEAN,
                "expected_value": True
            },
            generator_hints=[
                "Define clear invariant conditions",
                "Test with boundary values",
                "Consider system state invariants"
            ],
            example_usage="Test that audio processing maintains sample rate invariant",
            applicable_criteria_patterns=[
                "shall maintain", "shall preserve", "shall ensure", "invariant", "consistent"
            ]
        )
        
        # Performance templates
        templates["performance_performance"] = PropertyTemplate(
            name="performance_performance",
            description="Performance property for timing and resource usage",
            property_type=PropertyType.PERFORMANCE,
            test_function_template="""
def test_{property_name}(self, data):
    '''Property: Performance requirement for {description}'''
    import time
    
    # Measure execution time
    start_time = time.time()
    result = system_function(data)
    end_time = time.time()
    
    execution_time = end_time - start_time
    
    # Assert performance requirement
    assert execution_time < max_allowed_time, f"Performance requirement violated: {execution_time}s > {max_allowed_time}s"
    
    # Additional performance checks
    assert result is not None, "Function should return a result"
""",
            validation_criteria_template={
                "criteria_type": ValidationCriteriaType.NUMERIC_RANGE,
                "max_value": 1.0  # Default 1 second max
            },
            generator_hints=[
                "Use realistic data sizes for testing",
                "Consider system load during testing",
                "Test with various input complexities"
            ],
            example_usage="Test that transcription completes within time limit",
            applicable_criteria_patterns=[
                "within", "less than", "under", "performance", "speed", "latency", "response time"
            ]
        )
        
        # Error handling templates
        templates["error_handling_functional"] = PropertyTemplate(
            name="error_handling_functional",
            description="Error handling property for exception scenarios",
            property_type=PropertyType.ERROR_HANDLING,
            test_function_template="""
def test_{property_name}(self, invalid_data):
    '''Property: Error handling for {description}'''
    # Test that system handles invalid input gracefully
    try:
        result = system_function(invalid_data)
        
        # If no exception, check that result indicates error
        assert is_error_result(result), f"Expected error indication for invalid input: {invalid_data}"
        
    except ExpectedException as e:
        # Expected exception - verify it's the right type and has useful message
        assert str(e), "Exception should have descriptive message"
        assert is_recoverable_error(e), "Error should be recoverable"
        
    except Exception as e:
        # Unexpected exception
        pytest.fail(f"Unexpected exception type: {type(e).__name__}: {e}")
""",
            validation_criteria_template={
                "criteria_type": ValidationCriteriaType.BOOLEAN,
                "expected_value": True
            },
            generator_hints=[
                "Generate various types of invalid input",
                "Test boundary conditions",
                "Verify error messages are helpful"
            ],
            example_usage="Test that invalid audio format is handled gracefully",
            applicable_criteria_patterns=[
                "error", "exception", "invalid", "failure", "fallback", "graceful", "handle"
            ]
        )
        
        # Security templates
        templates["security_security"] = PropertyTemplate(
            name="security_security",
            description="Security property for access control and data protection",
            property_type=PropertyType.SECURITY,
            test_function_template="""
def test_{property_name}(self, data):
    '''Property: Security requirement for {description}'''
    # Test security constraint
    result = system_function(data)
    
    # Verify security properties
    assert is_secure_result(result), f"Security requirement violated for: {data}"
    
    # Check for data leakage
    assert not contains_sensitive_data(result), "Result should not contain sensitive data"
    
    # Verify access control
    assert has_proper_access_control(result), "Proper access control should be enforced"
""",
            validation_criteria_template={
                "criteria_type": ValidationCriteriaType.BOOLEAN,
                "expected_value": True
            },
            generator_hints=[
                "Test with various permission levels",
                "Verify data encryption/decryption",
                "Check for information leakage"
            ],
            example_usage="Test that audio data is properly encrypted during storage",
            applicable_criteria_patterns=[
                "secure", "encrypt", "protect", "authentication", "authorization", "access control"
            ]
        )
        
        # Metamorphic templates
        templates["metamorphic_functional"] = PropertyTemplate(
            name="metamorphic_functional",
            description="Metamorphic property for input-output relationships",
            property_type=PropertyType.METAMORPHIC,
            test_function_template="""
def test_{property_name}(self, data1, data2):
    '''Property: Metamorphic relationship for {description}'''
    # Execute function with both inputs
    result1 = system_function(data1)
    result2 = system_function(data2)
    
    # Check metamorphic relationship
    assert metamorphic_relation(data1, data2, result1, result2), \\
        f"Metamorphic relation violated: f({data1}) = {result1}, f({data2}) = {result2}"
    
    # Additional relationship checks
    if data1 == data2:
        assert result1 == result2, "Same input should produce same output"
""",
            validation_criteria_template={
                "criteria_type": ValidationCriteriaType.BOOLEAN,
                "expected_value": True
            },
            generator_hints=[
                "Define clear metamorphic relationships",
                "Test with related inputs",
                "Consider commutative, associative properties"
            ],
            example_usage="Test that audio processing maintains volume relationships",
            applicable_criteria_patterns=[
                "relationship", "proportion", "ratio", "relative", "compared", "scale"
            ]
        )
        
        return templates


class PropertyToTestMapper:
    """
    Maps analyzed acceptance criteria to concrete property test implementations.
    """
    
    def __init__(self, template_system: PropertyTemplateSystem):
        """
        Initialize the mapper with template system.
        
        Args:
            template_system: PropertyTemplateSystem instance
        """
        self.template_system = template_system
        logger.info("Property-to-Test Mapper initialized")
    
    def create_property_mapping(self, analysis: CriteriaAnalysis) -> Optional[PropertyMapping]:
        """
        Create a property mapping from criteria analysis.
        
        Args:
            analysis: CriteriaAnalysis result
            
        Returns:
            PropertyMapping if successful, None otherwise
        """
        try:
            if not analysis.is_property_testable():
                logger.debug(f"Criterion not suitable for property testing: {analysis.suggested_property_name}")
                return None
            
            # Get appropriate template
            template = self.template_system.get_template(analysis.property_type, analysis.criteria_type)
            if not template:
                logger.warning(f"No template found for {analysis.property_type.value}_{analysis.criteria_type.value}")
                return None
            
            # Create validation criteria
            validation_criteria = self._create_validation_criteria(analysis, template)
            
            # Generate implementation notes
            implementation_notes = self._generate_implementation_notes(analysis, template)
            
            # Determine dependencies
            dependencies = self._determine_dependencies(analysis)
            
            mapping = PropertyMapping(
                criterion_id=f"criterion_{hash(analysis.criterion_text) % 10000}",
                criterion_text=analysis.criterion_text,
                property_name=analysis.suggested_property_name,
                property_description=f"Property test for: {analysis.criterion_text[:100]}...",
                test_function_name=f"test_{analysis.suggested_property_name}",
                validation_criteria=validation_criteria,
                requirements_reference=analysis.requirements_reference,
                implementation_notes=implementation_notes,
                dependencies=dependencies
            )
            
            logger.debug(f"Created property mapping: {mapping.property_name}")
            return mapping
            
        except Exception as e:
            logger.error(f"Error creating property mapping: {e}", exc_info=True)
            return None
    
    def create_property_mappings_batch(self, analyses: List[CriteriaAnalysis]) -> List[PropertyMapping]:
        """
        Create property mappings for multiple analyses.
        
        Args:
            analyses: List of CriteriaAnalysis results
            
        Returns:
            List of PropertyMapping objects
        """
        logger.info(f"Creating property mappings for {len(analyses)} analyses")
        
        mappings = []
        for analysis in analyses:
            mapping = self.create_property_mapping(analysis)
            if mapping:
                mappings.append(mapping)
        
        logger.info(f"Created {len(mappings)} property mappings")
        return mappings
    
    def generate_property_test_code(self, mapping: PropertyMapping) -> str:
        """
        Generate actual test code from property mapping.
        
        Args:
            mapping: PropertyMapping to generate code for
            
        Returns:
            Generated test code as string
        """
        try:
            # Get template for the property type
            template = None
            for tmpl in self.template_system.get_all_templates().values():
                if tmpl.property_type.value in mapping.property_name:
                    template = tmpl
                    break
            
            if not template:
                logger.warning(f"No template found for generating code for {mapping.property_name}")
                return f"# TODO: Implement test for {mapping.property_name}"
            
            # Replace placeholders in template
            code = template.test_function_template.format(
                property_name=mapping.property_name,
                description=mapping.property_description
            )
            
            # Add imports and setup
            imports = """
import pytest
from hypothesis import given, strategies as st
import time
from typing import Any

"""
            
            # Add property validation comment
            validation_comment = f"""
# Property validation for: {mapping.criterion_text}
# Requirements reference: {mapping.requirements_reference}
# Validation criteria: {mapping.validation_criteria.criteria_type.value}
"""
            
            return imports + validation_comment + code
            
        except Exception as e:
            logger.error(f"Error generating test code: {e}", exc_info=True)
            return f"# Error generating test code for {mapping.property_name}: {e}"
    
    def _create_validation_criteria(self, analysis: CriteriaAnalysis, template: PropertyTemplate) -> ValidationCriteria:
        """Create validation criteria from analysis and template."""
        template_criteria = template.validation_criteria_template
        
        # Extract specific values from quantifiable aspects if available
        if analysis.quantifiable_aspects:
            # Try to extract numeric values for range validation
            numeric_values = []
            for aspect in analysis.quantifiable_aspects:
                import re
                numbers = re.findall(r'\d+\.?\d*', str(aspect))
                numeric_values.extend([float(n) for n in numbers])
            
            if numeric_values and template_criteria.get("criteria_type") == ValidationCriteriaType.NUMERIC_RANGE:
                return ValidationCriteria(
                    criteria_type=ValidationCriteriaType.NUMERIC_RANGE,
                    min_value=min(numeric_values) if len(numeric_values) > 1 else None,
                    max_value=max(numeric_values),
                    error_message=f"Value outside expected range for {analysis.suggested_property_name}"
                )
        
        # Default validation criteria based on template
        criteria_type = ValidationCriteriaType(template_criteria.get("criteria_type", ValidationCriteriaType.BOOLEAN))
        
        return ValidationCriteria(
            criteria_type=criteria_type,
            expected_value=template_criteria.get("expected_value", True),
            min_value=template_criteria.get("min_value"),
            max_value=template_criteria.get("max_value"),
            pattern=template_criteria.get("pattern"),
            error_message=f"Validation failed for {analysis.suggested_property_name}"
        )
    
    def _generate_implementation_notes(self, analysis: CriteriaAnalysis, template: PropertyTemplate) -> List[str]:
        """Generate implementation notes for the property mapping."""
        notes = []
        
        # Add complexity-based notes
        if analysis.complexity_score > 0.7:
            notes.append("High complexity criterion - consider breaking into smaller properties")
        
        # Add testability-specific notes
        if analysis.testability_level == TestabilityLevel.EDGE_CASE:
            notes.append("Focus on edge cases and boundary conditions")
        
        # Add quantifiable aspect notes
        if analysis.quantifiable_aspects:
            notes.append(f"Quantifiable aspects found: {', '.join(analysis.quantifiable_aspects)}")
        
        # Add template-specific hints
        notes.extend(template.generator_hints)
        
        # Add validation approach note
        notes.append(f"Use {analysis.validation_approach} for validation")
        
        return notes
    
    def _determine_dependencies(self, analysis: CriteriaAnalysis) -> List[str]:
        """Determine dependencies for the property test."""
        dependencies = []
        
        # Add dependencies based on property type
        if analysis.property_type == PropertyType.PERFORMANCE:
            dependencies.append("performance_monitoring")
        
        if analysis.property_type == PropertyType.SECURITY:
            dependencies.append("security_framework")
        
        if analysis.property_type == PropertyType.ROUND_TRIP:
            dependencies.append("serialization_framework")
        
        # Add dependencies based on criteria type
        if analysis.criteria_type == CriteriaType.PERFORMANCE:
            dependencies.append("timing_utilities")
        
        return dependencies


class DesignPropertyGenerator:
    """
    Main class that orchestrates the design property generation process.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the design property generator.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.analyzer = AcceptanceCriteriaAnalyzer()
        self.template_system = PropertyTemplateSystem()
        self.mapper = PropertyToTestMapper(self.template_system)
        
        logger.info("Design Property Generator initialized")
    
    def generate_properties_from_requirements(self, requirements: Dict[str, Any]) -> PropertySuite:
        """
        Generate property suite from requirements document.
        
        Args:
            requirements: Requirements document with acceptance criteria
            
        Returns:
            PropertySuite with generated properties
        """
        logger.info("Generating properties from requirements document")
        
        try:
            # Extract acceptance criteria from requirements
            criteria_list = self._extract_criteria_from_requirements(requirements)
            
            # Analyze criteria
            analyses = self.analyzer.analyze_criteria_batch(criteria_list)
            
            # Create property mappings
            mappings = self.mapper.create_property_mappings_batch(analyses)
            
            # Generate TranscriptionProperty objects
            properties = []
            for mapping in mappings:
                prop = self._create_transcription_property(mapping)
                if prop:
                    properties.append(prop)
            
            # Create property suite
            suite = PropertySuite(
                name=f"generated_properties_{requirements.get('title', 'unknown')}",
                description=f"Generated properties for {requirements.get('title', 'requirements document')}",
                properties=properties,
                parallel_execution=self.config.get('parallel_execution', False)
            )
            
            logger.info(f"Generated property suite with {len(properties)} properties")
            return suite
            
        except Exception as e:
            logger.error(f"Error generating properties from requirements: {e}", exc_info=True)
            return PropertySuite(
                name="error_suite",
                description="Error occurred during property generation",
                properties=[]
            )
    
    def export_property_suite(self, suite: PropertySuite, output_path: Path) -> bool:
        """
        Export property suite to file.
        
        Args:
            suite: PropertySuite to export
            output_path: Path to save the suite
            
        Returns:
            True if export successful
        """
        try:
            suite_data = {
                'name': suite.name,
                'description': suite.description,
                'parallel_execution': suite.parallel_execution,
                'properties': [prop.get_metadata() for prop in suite.properties]
            }
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(suite_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Property suite exported to: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting property suite: {e}", exc_info=True)
            return False
    
    def generate_test_code_files(self, suite: PropertySuite, output_dir: Path) -> List[Path]:
        """
        Generate test code files from property suite.
        
        Args:
            suite: PropertySuite to generate code for
            output_dir: Directory to save test files
            
        Returns:
            List of generated file paths
        """
        logger.info(f"Generating test code files for suite: {suite.name}")
        
        generated_files = []
        
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Group properties by type for better organization
            properties_by_type = {}
            for prop in suite.properties:
                prop_type = prop.property_type.value
                if prop_type not in properties_by_type:
                    properties_by_type[prop_type] = []
                properties_by_type[prop_type].append(prop)
            
            # Generate a test file for each property type
            for prop_type, props in properties_by_type.items():
                file_path = output_dir / f"test_{prop_type}_properties.py"
                
                # Generate file content
                file_content = self._generate_test_file_content(props, prop_type)
                
                # Write file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_content)
                
                generated_files.append(file_path)
                logger.info(f"Generated test file: {file_path}")
            
            return generated_files
            
        except Exception as e:
            logger.error(f"Error generating test code files: {e}", exc_info=True)
            return []
    
    def _extract_criteria_from_requirements(self, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract acceptance criteria from requirements document."""
        criteria_list = []
        
        # Handle different requirement document formats
        if 'requirements' in requirements:
            for req_id, req_data in requirements['requirements'].items():
                if 'acceptance_criteria' in req_data:
                    criteria = req_data['acceptance_criteria']
                    if isinstance(criteria, list):
                        for criterion in criteria:
                            criteria_list.append({
                                'text': criterion,
                                'requirement_id': req_id
                            })
                    elif isinstance(criteria, str):
                        criteria_list.append({
                            'text': criteria,
                            'requirement_id': req_id
                        })
        
        return criteria_list
    
    def _create_transcription_property(self, mapping: PropertyMapping) -> Optional[TranscriptionProperty]:
        """Create TranscriptionProperty from PropertyMapping."""
        try:
            # Create a simple test function for now
            def test_function(context):
                # This would be replaced with actual test logic
                return True
            
            return TranscriptionProperty(
                name=mapping.property_name,
                description=mapping.property_description,
                property_type=self._map_to_property_type(mapping),
                test_function=test_function,
                requirements_reference=mapping.requirements_reference,
                validation_criteria=mapping.validation_criteria,
                priority=1,  # Default high priority
                enabled=True,
                tags=['generated', 'acceptance_criteria']
            )
            
        except Exception as e:
            logger.error(f"Error creating TranscriptionProperty: {e}", exc_info=True)
            return None
    
    def _map_to_property_type(self, mapping: PropertyMapping) -> PropertyType:
        """Map PropertyMapping to PropertyType enum."""
        # This is a simple mapping - could be enhanced
        if 'round_trip' in mapping.property_name:
            return PropertyType.ROUND_TRIP
        elif 'performance' in mapping.property_name:
            return PropertyType.PERFORMANCE
        elif 'security' in mapping.property_name:
            return PropertyType.SECURITY
        elif 'error' in mapping.property_name:
            return PropertyType.ERROR_HANDLING
        else:
            return PropertyType.INVARIANT
    
    def _generate_test_file_content(self, properties: List[TranscriptionProperty], prop_type: str) -> str:
        """Generate content for a test file."""
        content = f'''"""
Generated property tests for {prop_type} properties.

This file contains property-based tests generated from acceptance criteria.
"""

import pytest
from hypothesis import given, strategies as st
import time
from typing import Any

# Import VTT modernization components
from whisper.modernization.models.property_models import PropertyTestResult
from whisper.modernization.core.property_testing import PropertyTestFramework


class Test{prop_type.title()}Properties:
    """Test class for {prop_type} properties."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_framework = PropertyTestFramework()
    
'''
        
        # Add test methods for each property
        for prop in properties:
            content += f'''
    def test_{prop.name}(self):
        """
        {prop.description}
        
        Requirements reference: {prop.requirements_reference}
        Property type: {prop.property_type.value}
        """
        # TODO: Implement actual test logic
        # This is a placeholder generated from acceptance criteria
        
        # Test context
        context = {{
            'property_name': '{prop.name}',
            'requirements_ref': '{prop.requirements_reference}'
        }}
        
        # Execute property test
        result = prop.execute(context)
        
        # Assert test passed
        assert result.success, f"Property test failed: {{result.error_message}}"
    
'''
        
        return content