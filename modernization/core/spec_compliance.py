"""
Spec Compliance Module for VTT System Modernization

This module ensures the VTT system follows modern specification standards,
including EARS patterns, INCOSE quality rules, and requirements traceability.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import re
import json
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class EARSPattern(Enum):
    """EARS (Easy Approach to Requirements Syntax) pattern types."""
    UBIQUITOUS = "ubiquitous"  # The system shall...
    EVENT_DRIVEN = "event_driven"  # When <trigger>, the system shall...
    UNWANTED_BEHAVIOR = "unwanted_behavior"  # If <condition>, then the system shall...
    STATE_DRIVEN = "state_driven"  # While <state>, the system shall...
    OPTIONAL = "optional"  # Where <feature>, the system shall...
    INVALID = "invalid"  # Does not match any EARS pattern


@dataclass
class ValidationResult:
    """Result of requirement validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    pattern_type: Optional[EARSPattern] = None
    quality_score: float = 0.0
    incose_compliance: Dict[str, bool] = field(default_factory=dict)
    suggestions: List[str] = field(default_factory=list)


@dataclass
class Property:
    """Generated correctness property from requirements."""
    name: str
    description: str
    property_type: str
    test_function_template: str
    requirements_reference: str
    validation_criteria: Dict[str, Any]


@dataclass
class TaskItem:
    """Individual task in the breakdown."""
    id: str
    title: str
    description: str
    requirements_refs: List[str]
    dependencies: List[str]
    estimated_effort: str


@dataclass
class TaskList:
    """Complete task breakdown structure."""
    tasks: List[TaskItem]
    total_tasks: int
    estimated_duration: str


@dataclass
class RequirementsDocument:
    """Generated requirements document structure."""
    title: str
    version: str
    date: str
    introduction: str
    glossary: Dict[str, str]
    requirements: Dict[str, Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentTemplate:
    """Template for requirements document generation."""
    name: str
    description: str
    sections: List[str]
    format_rules: Dict[str, Any]
    validation_rules: List[str]


class SpecComplianceModule:
    """
    Ensures the VTT system follows modern specification standards.
    
    This module validates requirements against EARS patterns, generates
    correctness properties, and maintains traceability between requirements,
    design, and implementation.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Spec Compliance Module.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.ears_patterns = self._initialize_ears_patterns()
        self.incose_rules = self._initialize_incose_rules()
        self.document_templates = self._initialize_document_templates()
        
        logger.info("Spec Compliance Module initialized")
    
    def validate_requirements(self, requirements: Dict[str, Any]) -> ValidationResult:
        """
        Validate requirements against EARS patterns and INCOSE quality rules.
        
        Args:
            requirements: Dictionary containing requirement specifications
            
        Returns:
            ValidationResult with validation status and details
        """
        logger.debug("Validating requirements: %d items", len(requirements))
        
        errors = []
        warnings = []
        suggestions = []
        pattern_type = None
        quality_score = 0.0
        incose_compliance = {}
        
        try:
            # Validate EARS pattern compliance
            ears_result = self._validate_ears_patterns(requirements)
            if not ears_result['is_valid']:
                errors.extend(ears_result['errors'])
                suggestions.extend(ears_result.get('suggestions', []))
            else:
                pattern_type = ears_result['pattern_type']
                quality_score += 0.4
            
            # Validate INCOSE quality rules
            incose_result = self._validate_incose_rules(requirements)
            incose_compliance = incose_result['compliance']
            if not incose_result['is_valid']:
                warnings.extend(incose_result['warnings'])
                suggestions.extend(incose_result.get('suggestions', []))
                # Add partial score for passed INCOSE rules
                passed_rules = sum(1 for rule_name, passed in incose_compliance.items() if passed)
                total_rules = len(incose_compliance)
                if total_rules > 0:
                    quality_score += 0.6 * (passed_rules / total_rules)
            else:
                quality_score += 0.6
            
            is_valid = len(errors) == 0
            
            logger.info("Requirements validation completed: valid=%s, score=%.2f",
                       is_valid, quality_score)
            
            return ValidationResult(
                is_valid=is_valid,
                errors=errors,
                warnings=warnings,
                pattern_type=pattern_type,
                quality_score=quality_score,
                incose_compliance=incose_compliance,
                suggestions=suggestions
            )
            
        except Exception as e:
            logger.error("Error during requirements validation: %s", e, exc_info=True)
            return ValidationResult(
                is_valid=False,
                errors=[f"Validation failed: {str(e)}"],
                warnings=[],
                pattern_type=None,
                quality_score=0.0,
                incose_compliance={},
                suggestions=[]
            )
    
    def generate_requirements_document(self, 
                                     requirements_data: Dict[str, Any],
                                     template_name: str = "standard") -> RequirementsDocument:
        """
        Generate a requirements document using specified template.
        
        Args:
            requirements_data: Raw requirements data to process
            template_name: Name of template to use for generation
            
        Returns:
            RequirementsDocument with formatted content
        """
        logger.debug("Generating requirements document with template: %s", template_name)
        
        try:
            template = self._get_document_template(template_name)
            if not template:
                raise ValueError(f"Template '{template_name}' not found")
            
            # Validate and process requirements
            validation_result = self.validate_requirements(requirements_data)
            
            # Generate document structure
            document = RequirementsDocument(
                title=requirements_data.get('title', 'Requirements Document'),
                version=requirements_data.get('version', '1.0.0'),
                date=datetime.now().strftime('%Y-%m-%d'),
                introduction=self._generate_introduction(requirements_data, template),
                glossary=self._generate_glossary(requirements_data),
                requirements=self._format_requirements(requirements_data, template),
                metadata={
                    'template_used': template_name,
                    'validation_score': validation_result.quality_score,
                    'ears_compliance': validation_result.pattern_type is not None,
                    'incose_compliance': validation_result.incose_compliance,
                    'generation_timestamp': datetime.now().isoformat()
                }
            )
            
            logger.info("Requirements document generated successfully")
            return document
            
        except Exception as e:
            logger.error("Error generating requirements document: %s", e, exc_info=True)
            raise
    
    def export_requirements_document(self, 
                                   document: RequirementsDocument,
                                   output_path: Path,
                                   format_type: str = "markdown") -> bool:
        """
        Export requirements document to specified format.
        
        Args:
            document: RequirementsDocument to export
            output_path: Path where to save the document
            format_type: Format type (markdown, json, html)
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            if format_type.lower() == "markdown":
                content = self._export_to_markdown(document)
            elif format_type.lower() == "json":
                content = self._export_to_json(document)
            elif format_type.lower() == "html":
                content = self._export_to_html(document)
            else:
                raise ValueError(f"Unsupported format type: {format_type}")
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(content, encoding='utf-8')
            
            logger.info("Requirements document exported to: %s", output_path)
            return True
            
        except Exception as e:
            logger.error("Error exporting requirements document: %s", e, exc_info=True)
            return False
    
    def generate_design_properties(self, requirements: Dict[str, Any]) -> List[Property]:
        """
        Generate correctness properties from acceptance criteria.
        
        Args:
            requirements: Dictionary containing requirement specifications
            
        Returns:
            List of Property objects for property-based testing
        """
        logger.debug("Generating design properties from requirements")
        
        properties = []
        
        try:
            for req_id, req_data in requirements.items():
                if 'acceptance_criteria' in req_data:
                    for idx, criterion in enumerate(req_data['acceptance_criteria']):
                        property_obj = self._create_property_from_criterion(
                            req_id, idx, criterion
                        )
                        if property_obj:
                            properties.append(property_obj)
            
            logger.info("Generated %d design properties", len(properties))
            return properties
            
        except Exception as e:
            logger.error("Error generating design properties: %s", e, exc_info=True)
            return []
    
    def create_task_breakdown(self, design: Dict[str, Any]) -> TaskList:
        """
        Create structured task breakdown following spec patterns.
        
        Args:
            design: Dictionary containing design specifications
            
        Returns:
            TaskList with structured task breakdown
        """
        logger.debug("Creating task breakdown from design")
        
        tasks = []
        
        try:
            # Extract components and create tasks
            if 'components' in design:
                for component_name, component_data in design['components'].items():
                    task = self._create_component_task(component_name, component_data)
                    if task:
                        tasks.append(task)
            
            # Extract properties and create testing tasks
            if 'properties' in design:
                for prop_data in design['properties']:
                    task = self._create_property_test_task(prop_data)
                    if task:
                        tasks.append(task)
            
            total_tasks = len(tasks)
            estimated_duration = self._estimate_duration(tasks)
            
            logger.info(f"Created task breakdown: {total_tasks} tasks, estimated {estimated_duration}")
            
            return TaskList(
                tasks=tasks,
                total_tasks=total_tasks,
                estimated_duration=estimated_duration
            )
            
        except Exception as e:
            logger.error(f"Error creating task breakdown: {e}", exc_info=True)
            return TaskList(tasks=[], total_tasks=0, estimated_duration="Unknown")
    
    def ensure_ears_compliance(self, requirement: str) -> bool:
        """
        Check if a requirement follows EARS patterns.
        
        Args:
            requirement: Requirement text to validate
            
        Returns:
            True if requirement follows EARS patterns
        """
        try:
            for pattern in self.ears_patterns:
                if pattern['regex'].match(requirement.strip()):
                    logger.debug(f"Requirement matches EARS pattern: {pattern['type']}")
                    return True
            
            logger.warning(f"Requirement does not match any EARS pattern: {requirement[:50]}...")
            return False
            
        except Exception as e:
            logger.error(f"Error checking EARS compliance: {e}", exc_info=True)
            return False
    
    def _detect_ears_pattern(self, requirement: str) -> EARSPattern:
        """
        Detect the specific EARS pattern type of a requirement.
        
        Args:
            requirement: Requirement text to analyze
            
        Returns:
            EARSPattern enum value indicating the detected pattern type
        """
        try:
            if not requirement or not requirement.strip():
                return EARSPattern.INVALID
            
            requirement_text = requirement.strip()
            
            # Check each EARS pattern in order
            for pattern in self.ears_patterns:
                if pattern['regex'].match(requirement_text):
                    logger.debug(f"Detected EARS pattern: {pattern['type']} for requirement: {requirement_text[:50]}...")
                    return pattern['type']
            
            # If no pattern matches, return INVALID
            logger.debug(f"No EARS pattern detected for requirement: {requirement_text[:50]}...")
            return EARSPattern.INVALID
            
        except Exception as e:
            logger.error(f"Error detecting EARS pattern: {e}", exc_info=True)
            return EARSPattern.INVALID
    
    def _initialize_ears_patterns(self) -> List[Dict[str, Any]]:
        """Initialize enhanced EARS pattern definitions."""
        return [
            {
                'type': EARSPattern.UBIQUITOUS,
                'regex': re.compile(r'^THE\s+\w+\s+SHALL\s+', re.IGNORECASE),
                'description': 'Ubiquitous requirement pattern',
                'template': 'THE {system} SHALL {action}',
                'examples': ['THE VTT_System SHALL process audio files'],
                'validation_rules': ['Must specify system entity', 'Must use SHALL verb']
            },
            {
                'type': EARSPattern.EVENT_DRIVEN,
                'regex': re.compile(r'^WHEN\s+.*,\s*THE\s+\w+\s+SHALL\s+', re.IGNORECASE),
                'description': 'Event-driven requirement pattern',
                'template': 'WHEN {trigger}, THE {system} SHALL {response}',
                'examples': ['WHEN user presses hotkey, THE VTT_System SHALL start recording'],
                'validation_rules': ['Must specify trigger condition', 'Must specify system response']
            },
            {
                'type': EARSPattern.UNWANTED_BEHAVIOR,
                'regex': re.compile(r'^IF\s+.*,\s*THEN\s+THE\s+\w+\s+SHALL\s+', re.IGNORECASE),
                'description': 'Unwanted behavior requirement pattern',
                'template': 'IF {unwanted_condition}, THEN THE {system} SHALL {mitigation}',
                'examples': ['IF audio input fails, THEN THE VTT_System SHALL use fallback engine'],
                'validation_rules': ['Must specify unwanted condition', 'Must specify mitigation']
            },
            {
                'type': EARSPattern.STATE_DRIVEN,
                'regex': re.compile(r'^WHILE\s+.*,\s*THE\s+\w+\s+SHALL\s+', re.IGNORECASE),
                'description': 'State-driven requirement pattern',
                'template': 'WHILE {state}, THE {system} SHALL {behavior}',
                'examples': ['WHILE recording audio, THE VTT_System SHALL monitor input levels'],
                'validation_rules': ['Must specify system state', 'Must specify continuous behavior']
            },
            {
                'type': EARSPattern.OPTIONAL,
                'regex': re.compile(r'^WHERE\s+.*,\s*THE\s+\w+\s+SHALL\s+', re.IGNORECASE),
                'description': 'Optional requirement pattern',
                'template': 'WHERE {feature_condition}, THE {system} SHALL {optional_behavior}',
                'examples': ['WHERE GPU is available, THE VTT_System SHALL use faster-whisper'],
                'validation_rules': ['Must specify optional condition', 'Must specify conditional behavior']
            }
        ]
    
    def _initialize_incose_rules(self) -> List[Dict[str, Any]]:
        """Initialize enhanced INCOSE quality rules."""
        return [
            {
                'name': 'Completeness',
                'description': 'Requirements should be complete and unambiguous',
                'validator': self._check_completeness,
                'weight': 0.25,
                'critical': True
            },
            {
                'name': 'Consistency',
                'description': 'Requirements should be consistent with each other',
                'validator': self._check_consistency,
                'weight': 0.20,
                'critical': True
            },
            {
                'name': 'Verifiability',
                'description': 'Requirements should be verifiable through testing',
                'validator': self._check_verifiability,
                'weight': 0.20,
                'critical': True
            },
            {
                'name': 'Clarity',
                'description': 'Requirements should be clear and unambiguous',
                'validator': self._check_clarity,
                'weight': 0.15,
                'critical': False
            },
            {
                'name': 'Traceability',
                'description': 'Requirements should be traceable to business needs',
                'validator': self._check_traceability,
                'weight': 0.10,
                'critical': False
            },
            {
                'name': 'Feasibility',
                'description': 'Requirements should be technically feasible',
                'validator': self._check_feasibility,
                'weight': 0.10,
                'critical': False
            }
        ]
    
    def _initialize_document_templates(self) -> Dict[str, DocumentTemplate]:
        """Initialize document templates for requirements generation."""
        return {
            'standard': DocumentTemplate(
                name='Standard Requirements Document',
                description='Standard template following IEEE 830 guidelines',
                sections=['introduction', 'glossary', 'requirements', 'appendices'],
                format_rules={
                    'requirement_numbering': 'hierarchical',
                    'acceptance_criteria_format': 'numbered_list',
                    'user_story_format': 'as_a_i_want_so_that'
                },
                validation_rules=['ears_compliance', 'incose_quality', 'traceability']
            ),
            'agile': DocumentTemplate(
                name='Agile Requirements Document',
                description='Agile-focused template with user stories and acceptance criteria',
                sections=['overview', 'user_stories', 'acceptance_criteria', 'definition_of_done'],
                format_rules={
                    'requirement_numbering': 'flat',
                    'acceptance_criteria_format': 'gherkin_style',
                    'user_story_format': 'as_a_i_want_so_that'
                },
                validation_rules=['testability', 'user_focus', 'iterative_delivery']
            ),
            'technical': DocumentTemplate(
                name='Technical Requirements Document',
                description='Technical specification template for system requirements',
                sections=['architecture', 'functional_requirements', 'non_functional_requirements', 'constraints'],
                format_rules={
                    'requirement_numbering': 'hierarchical',
                    'acceptance_criteria_format': 'technical_specification',
                    'user_story_format': 'system_behavior'
                },
                validation_rules=['ears_compliance', 'technical_feasibility', 'performance_criteria']
            )
        }
    
    def _validate_ears_patterns(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced validation of requirements against EARS patterns."""
        errors = []
        suggestions = []
        pattern_type = None
        pattern_distribution = {}
        
        for req_id, req_data in requirements.items():
            if 'text' in req_data:
                req_text = req_data['text'].strip()
                matched_pattern = None
                
                # Check each EARS pattern
                for pattern in self.ears_patterns:
                    if pattern['regex'].match(req_text):
                        matched_pattern = pattern['type']
                        pattern_distribution[matched_pattern] = pattern_distribution.get(matched_pattern, 0) + 1
                        if pattern_type is None:
                            pattern_type = matched_pattern
                        break
                
                if not matched_pattern:
                    errors.append(f"Requirement {req_id} does not follow EARS patterns")
                    # Provide specific suggestions based on content analysis
                    suggestions.extend(self._generate_ears_suggestions(req_text, req_id))
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'suggestions': suggestions,
            'pattern_type': pattern_type,
            'pattern_distribution': pattern_distribution
        }
    
    def _validate_incose_rules(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced validation of requirements against INCOSE quality rules."""
        warnings = []
        suggestions = []
        compliance = {}
        overall_score = 0.0
        
        for rule in self.incose_rules:
            try:
                rule_result = rule['validator'](requirements)
                rule_name = rule['name']
                rule_weight = rule.get('weight', 1.0)
                
                compliance[rule_name] = rule_result['is_valid']
                
                if rule_result['is_valid']:
                    overall_score += rule_weight
                else:
                    warnings.extend(rule_result['warnings'])
                    if 'suggestions' in rule_result:
                        suggestions.extend(rule_result['suggestions'])
                    
                    # Add critical rule failures as errors if needed
                    if rule.get('critical', False):
                        warnings.append(f"CRITICAL: {rule_name} validation failed")
                        
            except Exception as e:
                warnings.append(f"Error validating {rule['name']}: {str(e)}")
                compliance[rule['name']] = False
        
        return {
            'is_valid': len(warnings) == 0,
            'warnings': warnings,
            'suggestions': suggestions,
            'compliance': compliance,
            'quality_score': overall_score
        }
    
    def _check_completeness(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced check for requirements completeness."""
        warnings = []
        suggestions = []
        
        required_fields = ['text', 'acceptance_criteria', 'user_story']
        optional_fields = ['priority', 'source', 'rationale', 'dependencies']
        
        for req_id, req_data in requirements.items():
            # Check required fields
            for field in required_fields:
                if field not in req_data or not req_data[field]:
                    warnings.append(f"Requirement {req_id} missing required field: {field}")
                    suggestions.append(f"Add {field} to requirement {req_id}")
            
            # Check acceptance criteria quality
            if 'acceptance_criteria' in req_data:
                criteria = req_data['acceptance_criteria']
                if isinstance(criteria, list) and len(criteria) == 0:
                    warnings.append(f"Requirement {req_id} has empty acceptance criteria")
                elif isinstance(criteria, list):
                    for idx, criterion in enumerate(criteria):
                        if len(criterion.strip()) < 10:
                            warnings.append(f"Acceptance criterion {idx+1} in {req_id} is too brief")
            
            # Check user story format
            if 'user_story' in req_data:
                user_story = req_data['user_story']
                if not self._is_valid_user_story_format(user_story):
                    warnings.append(f"User story in {req_id} doesn't follow 'As a... I want... So that...' format")
                    suggestions.append(f"Reformat user story in {req_id} using standard template")
        
        return {
            'is_valid': len(warnings) == 0,
            'warnings': warnings,
            'suggestions': suggestions
        }
    
    def _check_consistency(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced check for requirements consistency."""
        warnings = []
        suggestions = []
        
        # Check for conflicting requirements
        system_entities = set()
        action_verbs = {}
        
        for req_id, req_data in requirements.items():
            if 'text' in req_data:
                req_text = req_data['text']
                
                # Extract system entity
                entity_match = re.search(r'THE\s+(\w+)\s+SHALL', req_text, re.IGNORECASE)
                if entity_match:
                    entity = entity_match.group(1).upper()
                    system_entities.add(entity)
                    
                    # Extract action verb
                    action_match = re.search(r'SHALL\s+(\w+)', req_text, re.IGNORECASE)
                    if action_match:
                        action = action_match.group(1).lower()
                        if entity not in action_verbs:
                            action_verbs[entity] = {}
                        if action not in action_verbs[entity]:
                            action_verbs[entity][action] = []
                        action_verbs[entity][action].append(req_id)
        
        # Check for inconsistent system entity naming
        if len(system_entities) > 3:  # Allow some variation but flag excessive diversity
            warnings.append(f"Multiple system entities found: {', '.join(system_entities)}")
            suggestions.append("Consider standardizing system entity names across requirements")
        
        # Check for potentially conflicting actions
        for entity, actions in action_verbs.items():
            conflicting_actions = ['start', 'stop', 'enable', 'disable', 'allow', 'prevent']
            found_conflicts = []
            for action in actions:
                for conflict in conflicting_actions:
                    if action == conflict:
                        opposite = {'start': 'stop', 'stop': 'start', 'enable': 'disable', 
                                  'disable': 'enable', 'allow': 'prevent', 'prevent': 'allow'}
                        if opposite.get(action) in actions:
                            found_conflicts.append((action, opposite[action]))
            
            for conflict_pair in found_conflicts:
                warnings.append(f"Potentially conflicting actions for {entity}: {conflict_pair[0]} vs {conflict_pair[1]}")
        
        return {
            'is_valid': len(warnings) == 0,
            'warnings': warnings,
            'suggestions': suggestions
        }
    
    def _check_verifiability(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced check for requirements verifiability."""
        warnings = []
        suggestions = []
        
        testable_keywords = ['shall', 'must', 'should', 'will', 'can', 'verify', 'validate', 'test', 'measure']
        quantifiable_terms = ['within', 'less than', 'greater than', 'at least', 'at most', 'exactly', 'between']
        
        for req_id, req_data in requirements.items():
            if 'acceptance_criteria' in req_data:
                criteria = req_data['acceptance_criteria']
                if isinstance(criteria, list):
                    for idx, criterion in enumerate(criteria):
                        criterion_lower = criterion.lower()
                        
                        # Check for testable keywords
                        has_testable_keyword = any(keyword in criterion_lower for keyword in testable_keywords)
                        if not has_testable_keyword:
                            warnings.append(f"Criterion {idx+1} in {req_id} may not be testable: {criterion[:50]}...")
                            suggestions.append(f"Add testable verbs (shall, must, can) to criterion {idx+1} in {req_id}")
                        
                        # Check for quantifiable terms for performance requirements
                        if any(perf_word in criterion_lower for perf_word in ['performance', 'speed', 'time', 'latency', 'throughput']):
                            has_quantifiable = any(term in criterion_lower for term in quantifiable_terms)
                            if not has_quantifiable:
                                warnings.append(f"Performance criterion {idx+1} in {req_id} lacks quantifiable metrics")
                                suggestions.append(f"Add specific metrics to performance criterion {idx+1} in {req_id}")
                        
                        # Check for vague terms
                        vague_terms = ['appropriate', 'suitable', 'adequate', 'reasonable', 'efficient', 'user-friendly']
                        found_vague = [term for term in vague_terms if term in criterion_lower]
                        if found_vague:
                            warnings.append(f"Criterion {idx+1} in {req_id} contains vague terms: {', '.join(found_vague)}")
                            suggestions.append(f"Replace vague terms with specific, measurable criteria in {req_id}")
        
        return {
            'is_valid': len(warnings) == 0,
            'warnings': warnings,
            'suggestions': suggestions
        }
    
    def _check_clarity(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Check requirements clarity and readability."""
        warnings = []
        suggestions = []
        
        for req_id, req_data in requirements.items():
            if 'text' in req_data:
                req_text = req_data['text']
                
                # Check sentence length (readability)
                sentences = req_text.split('.')
                for sentence in sentences:
                    words = sentence.strip().split()
                    if len(words) > 25:  # Arbitrary threshold for complex sentences
                        warnings.append(f"Requirement {req_id} contains overly complex sentence")
                        suggestions.append(f"Break down complex sentences in {req_id} for better clarity")
                
                # Check for ambiguous pronouns
                ambiguous_pronouns = ['it', 'this', 'that', 'they', 'them']
                for pronoun in ambiguous_pronouns:
                    if f' {pronoun} ' in req_text.lower():
                        warnings.append(f"Requirement {req_id} contains ambiguous pronoun: {pronoun}")
                        suggestions.append(f"Replace ambiguous pronouns with specific nouns in {req_id}")
        
        return {
            'is_valid': len(warnings) == 0,
            'warnings': warnings,
            'suggestions': suggestions
        }
    
    def _check_traceability(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Check requirements traceability to business needs."""
        warnings = []
        suggestions = []
        
        for req_id, req_data in requirements.items():
            # Check for business justification
            if 'rationale' not in req_data:
                warnings.append(f"Requirement {req_id} lacks business rationale")
                suggestions.append(f"Add rationale field to {req_id} explaining business need")
            
            # Check for source attribution
            if 'source' not in req_data:
                warnings.append(f"Requirement {req_id} lacks source attribution")
                suggestions.append(f"Add source field to {req_id} identifying requirement origin")
            
            # Check user story connection
            if 'user_story' in req_data:
                user_story = req_data['user_story']
                if 'so that' not in user_story.lower():
                    warnings.append(f"User story in {req_id} lacks business value statement")
                    suggestions.append(f"Add 'so that' clause to user story in {req_id}")
        
        return {
            'is_valid': len(warnings) == 0,
            'warnings': warnings,
            'suggestions': suggestions
        }
    
    def _check_feasibility(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Check technical feasibility of requirements."""
        warnings = []
        suggestions = []
        
        # Define feasibility indicators
        high_risk_terms = ['real-time', 'instantaneous', '100%', 'never fail', 'always', 'perfect']
        technical_constraints = ['cpu', 'gpu', 'memory', 'disk', 'network', 'latency', 'throughput']
        
        for req_id, req_data in requirements.items():
            if 'text' in req_data:
                req_text = req_data['text'].lower()
                
                # Check for high-risk terms
                found_risks = [term for term in high_risk_terms if term in req_text]
                if found_risks:
                    warnings.append(f"Requirement {req_id} contains high-risk terms: {', '.join(found_risks)}")
                    suggestions.append(f"Review feasibility of absolute terms in {req_id}")
                
                # Check for technical constraints without specifications
                found_constraints = [term for term in technical_constraints if term in req_text]
                if found_constraints:
                    # Check if there are specific values mentioned
                    has_numbers = re.search(r'\d+', req_text)
                    if not has_numbers:
                        warnings.append(f"Requirement {req_id} mentions technical constraints without specific values")
                        suggestions.append(f"Add specific technical specifications to {req_id}")
        
        return {
            'is_valid': len(warnings) == 0,
            'warnings': warnings,
            'suggestions': suggestions
        }
    
    def _is_testable_criterion(self, criterion: str) -> bool:
        """Check if an acceptance criterion is testable."""
        testable_keywords = ['shall', 'must', 'should', 'will', 'can', 'verify', 'validate', 'test']
        return any(keyword in criterion.lower() for keyword in testable_keywords)
    
    def _create_property_from_criterion(self, req_id: str, idx: int, criterion: str) -> Optional[Property]:
        """Create a property object from an acceptance criterion."""
        try:
            property_name = f"property_{req_id.lower()}_{idx + 1}"
            
            return Property(
                name=property_name,
                description=criterion,
                property_type="invariant",
                test_function_template=f"def test_{property_name}(self, data): pass",
                requirements_reference=req_id,
                validation_criteria={'criterion': criterion}
            )
        except Exception as e:
            logger.error(f"Error creating property from criterion: {e}", exc_info=True)
            return None
    
    def _create_component_task(self, component_name: str, component_data: Dict[str, Any]) -> Optional[TaskItem]:
        """Create a task for implementing a component."""
        try:
            task_id = f"impl_{component_name.lower().replace(' ', '_')}"
            
            return TaskItem(
                id=task_id,
                title=f"Implement {component_name}",
                description=component_data.get('description', f"Implementation of {component_name} component"),
                requirements_refs=component_data.get('requirements', []),
                dependencies=component_data.get('dependencies', []),
                estimated_effort=component_data.get('effort', 'Medium')
            )
        except Exception as e:
            logger.error(f"Error creating component task: {e}", exc_info=True)
            return None
    
    def _create_property_test_task(self, prop_data: Dict[str, Any]) -> Optional[TaskItem]:
        """Create a task for implementing property tests."""
        try:
            task_id = f"test_{prop_data.get('name', 'property').lower()}"
            
            return TaskItem(
                id=task_id,
                title=f"Implement property test: {prop_data.get('name', 'Unknown')}",
                description=prop_data.get('description', 'Property-based test implementation'),
                requirements_refs=prop_data.get('requirements_reference', []),
                dependencies=[],
                estimated_effort='Small'
            )
        except Exception as e:
            logger.error(f"Error creating property test task: {e}", exc_info=True)
            return None
    
    def _estimate_duration(self, tasks: List[TaskItem]) -> str:
        """Estimate total duration for task list."""
        effort_weights = {'Small': 1, 'Medium': 3, 'Large': 5}
        total_weight = sum(effort_weights.get(task.estimated_effort, 3) for task in tasks)
        
        if total_weight <= 10:
            return "1-2 weeks"
        elif total_weight <= 20:
            return "2-4 weeks"
        else:
            return "4+ weeks"
    def _generate_ears_suggestions(self, req_text: str, req_id: str) -> List[str]:
        """Generate specific suggestions for EARS pattern compliance."""
        suggestions = []
        
        # Analyze the requirement text to provide targeted suggestions
        if 'shall' not in req_text.lower():
            suggestions.append(f"Add 'SHALL' verb to requirement {req_id} for EARS pattern compliance")
        
        if not re.search(r'^(THE|WHEN|IF|WHILE|WHERE)', req_text, re.IGNORECASE):
            suggestions.append(f"Start requirement {req_id} with EARS pattern keyword (THE, WHEN, IF, WHILE, WHERE)")
        
        # Suggest specific patterns based on content
        if any(trigger in req_text.lower() for trigger in ['when', 'if', 'after', 'before', 'upon']):
            suggestions.append(f"Consider using event-driven pattern (WHEN..., THE system SHALL...) for {req_id}")
        elif any(state in req_text.lower() for state in ['while', 'during', 'throughout']):
            suggestions.append(f"Consider using state-driven pattern (WHILE..., THE system SHALL...) for {req_id}")
        elif any(condition in req_text.lower() for condition in ['where', 'provided', 'given']):
            suggestions.append(f"Consider using optional pattern (WHERE..., THE system SHALL...) for {req_id}")
        else:
            suggestions.append(f"Consider using ubiquitous pattern (THE system SHALL...) for {req_id}")
        
        return suggestions
    
    def _is_valid_user_story_format(self, user_story: str) -> bool:
        """Check if user story follows standard format."""
        user_story_lower = user_story.lower()
        return ('as a' in user_story_lower and 
                'i want' in user_story_lower and 
                'so that' in user_story_lower)
    
    def _get_document_template(self, template_name: str) -> Optional[DocumentTemplate]:
        """Get document template by name."""
        return self.document_templates.get(template_name)
    
    def _generate_introduction(self, requirements_data: Dict[str, Any], 
                             template: DocumentTemplate) -> str:
        """Generate introduction section for requirements document."""
        intro_template = """
## Introduction

This document specifies the requirements for {title}. The requirements follow modern 
specification standards including EARS (Easy Approach to Requirements Syntax) patterns 
and INCOSE quality guidelines.

### Purpose

{purpose}

### Scope

{scope}

### Document Structure

This document is organized according to the {template_name} template and includes:
{sections}
        """.strip()
        
        purpose = requirements_data.get('purpose', 'Define system requirements and acceptance criteria')
        scope = requirements_data.get('scope', 'This document covers functional and non-functional requirements')
        sections = '\n'.join(f"- {section.title()}" for section in template.sections)
        
        return intro_template.format(
            title=requirements_data.get('title', 'System Requirements'),
            purpose=purpose,
            scope=scope,
            template_name=template.name,
            sections=sections
        )
    
    def _generate_glossary(self, requirements_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate glossary from requirements data."""
        glossary = requirements_data.get('glossary', {})
        
        # Add standard VTT terms if not present
        standard_terms = {
            'VTT_System': 'The complete Voice-to-Text Tools suite including all applications',
            'EARS': 'Easy Approach to Requirements Syntax - a structured way to write requirements',
            'INCOSE': 'International Council on Systems Engineering - provides quality standards',
            'Acceptance_Criteria': 'Specific conditions that must be met for a requirement to be satisfied'
        }
        
        for term, definition in standard_terms.items():
            if term not in glossary:
                glossary[term] = definition
        
        return glossary
    
    def _format_requirements(self, requirements_data: Dict[str, Any], 
                           template: DocumentTemplate) -> Dict[str, Dict[str, Any]]:
        """Format requirements according to template rules."""
        formatted_requirements = {}
        
        for req_id, req_data in requirements_data.get('requirements', {}).items():
            formatted_req = {
                'id': req_id,
                'title': req_data.get('title', f'Requirement {req_id}'),
                'text': req_data.get('text', ''),
                'user_story': req_data.get('user_story', ''),
                'acceptance_criteria': req_data.get('acceptance_criteria', []),
                'priority': req_data.get('priority', 'Medium'),
                'source': req_data.get('source', 'Unknown'),
                'rationale': req_data.get('rationale', ''),
                'dependencies': req_data.get('dependencies', [])
            }
            
            # Apply template-specific formatting
            if template.format_rules.get('requirement_numbering') == 'hierarchical':
                formatted_req['display_id'] = self._format_hierarchical_id(req_id)
            else:
                formatted_req['display_id'] = req_id
            
            formatted_requirements[req_id] = formatted_req
        
        return formatted_requirements
    
    def _format_hierarchical_id(self, req_id: str) -> str:
        """Format requirement ID in hierarchical format."""
        # Convert flat ID to hierarchical (e.g., "req_1_2" -> "1.2")
        if '_' in req_id:
            parts = req_id.replace('req_', '').split('_')
            return '.'.join(parts)
        return req_id
    
    def _export_to_markdown(self, document: RequirementsDocument) -> str:
        """Export requirements document to Markdown format."""
        content = []
        
        # Title and metadata
        content.append(f"# {document.title}")
        content.append(f"**Version:** {document.version}")
        content.append(f"**Date:** {document.date}")
        content.append("")
        
        # Introduction
        content.append(document.introduction)
        content.append("")
        
        # Glossary
        if document.glossary:
            content.append("## Glossary")
            content.append("")
            for term, definition in sorted(document.glossary.items()):
                content.append(f"- **{term}**: {definition}")
            content.append("")
        
        # Requirements
        content.append("## Requirements")
        content.append("")
        
        for req_id, req_data in document.requirements.items():
            content.append(f"### {req_data.get('display_id', req_id)}: {req_data.get('title', '')}")
            content.append("")
            
            if req_data.get('user_story'):
                content.append(f"**User Story:** {req_data['user_story']}")
                content.append("")
            
            if req_data.get('text'):
                content.append(f"**Requirement:** {req_data['text']}")
                content.append("")
            
            if req_data.get('acceptance_criteria'):
                content.append("**Acceptance Criteria:**")
                for idx, criterion in enumerate(req_data['acceptance_criteria'], 1):
                    content.append(f"{idx}. {criterion}")
                content.append("")
            
            if req_data.get('rationale'):
                content.append(f"**Rationale:** {req_data['rationale']}")
                content.append("")
            
            if req_data.get('dependencies'):
                content.append(f"**Dependencies:** {', '.join(req_data['dependencies'])}")
                content.append("")
        
        # Metadata
        if document.metadata:
            content.append("## Document Metadata")
            content.append("")
            for key, value in document.metadata.items():
                content.append(f"- **{key.replace('_', ' ').title()}:** {value}")
        
        return '\n'.join(content)
    
    def _export_to_json(self, document: RequirementsDocument) -> str:
        """Export requirements document to JSON format."""
        doc_dict = {
            'title': document.title,
            'version': document.version,
            'date': document.date,
            'introduction': document.introduction,
            'glossary': document.glossary,
            'requirements': document.requirements,
            'metadata': document.metadata
        }
        return json.dumps(doc_dict, indent=2, ensure_ascii=False)
    
    def _export_to_html(self, document: RequirementsDocument) -> str:
        """Export requirements document to HTML format."""
        # Pre-process introduction to avoid backslash in f-string
        introduction_html = document.introduction.replace('\n', '<br>')
        
        # Pre-process glossary items
        glossary_html = ''.join(
            f'<dt><strong>{term}</strong></dt><dd>{definition}</dd>' 
            for term, definition in document.glossary.items()
        )
        
        # Pre-process requirements
        requirements_html = ''.join(
            self._format_requirement_html(req_id, req_data) 
            for req_id, req_data in document.requirements.items()
        )
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{document.title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        h1, h2, h3 {{ color: #333; }}
        .metadata {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
        .requirement {{ border-left: 3px solid #007acc; padding-left: 15px; margin: 20px 0; }}
        .acceptance-criteria {{ background: #f9f9f9; padding: 10px; border-radius: 3px; }}
    </style>
</head>
<body>
    <h1>{document.title}</h1>
    <div class="metadata">
        <p><strong>Version:</strong> {document.version}</p>
        <p><strong>Date:</strong> {document.date}</p>
    </div>
    
    <div class="introduction">
        {introduction_html}
    </div>
    
    <h2>Glossary</h2>
    <dl>
        {glossary_html}
    </dl>
    
    <h2>Requirements</h2>
    {requirements_html}
    
</body>
</html>"""
        
        return html_content
    
    def _format_requirement_html(self, req_id: str, req_data: Dict[str, Any]) -> str:
        """Format a single requirement as HTML."""
        html = f"""
        <div class="requirement">
            <h3>{req_data.get('display_id', req_id)}: {req_data.get('title', '')}</h3>
            {f'<p><strong>User Story:</strong> {req_data["user_story"]}</p>' if req_data.get('user_story') else ''}
            {f'<p><strong>Requirement:</strong> {req_data["text"]}</p>' if req_data.get('text') else ''}
            {self._format_acceptance_criteria_html(req_data.get('acceptance_criteria', []))}
            {f'<p><strong>Rationale:</strong> {req_data["rationale"]}</p>' if req_data.get('rationale') else ''}
        </div>
        """
        return html
    
    def _format_acceptance_criteria_html(self, criteria: List[str]) -> str:
        """Format acceptance criteria as HTML."""
        if not criteria:
            return ''
        
        criteria_html = '<div class="acceptance-criteria"><strong>Acceptance Criteria:</strong><ol>'
        for criterion in criteria:
            criteria_html += f'<li>{criterion}</li>'
        criteria_html += '</ol></div>'
        
        return criteria_html