#!/usr/bin/env python3
"""
HUMMBL Workflow Demonstration
Executable implementation of HUMMBL operators for engineering workflows

This demonstrates how mental models can be transformed into runnable code
that produces structured outputs for engineering decision-making.
"""

import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class HUMMBLOutput:
    """Standardized output format for HUMMBL operators"""
    operator: str
    model: str
    question: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    insights: List[str]
    confidence: float
    execution_time: float
    timestamp: str


class HUMMBLWorkflow:
    """Orchestrates sequences of HUMMBL operators"""

    def __init__(self):
        self.operators = {
            'DE01': self.decompose_root_cause,
            'P01': self.perspective_first_principles,
            'CO01': self.compose_modular_design,
            'IN01': self.invert_premortem,
            'SY01': self.synthesize_systems_view,
            'RE01': self.recurs_feedback_loops
        }

    def execute_sequence(self, problem: str, sequence: List[str]) -> List[HUMMBLOutput]:
        """Execute a sequence of operators on a problem"""
        results = []
        context = {'problem': problem}

        for operator_code in sequence:
            if operator_code in self.operators:
                result = self.operators[operator_code](context)
                results.append(result)
                # Update context with outputs for next operator
                context.update(result.outputs)

        return results

    def decompose_root_cause(self, context: Dict) -> HUMMBLOutput:
        """DE01: Break down problem into root causes and components"""
        problem = context.get('problem', '')

        # Extract components using pattern matching
        components = self._extract_components(problem)

        # Identify potential root causes
        root_causes = self._identify_root_causes(problem, components)

        # Build dependency relationships
        dependencies = self._build_dependencies(components)

        return HUMMBLOutput(
            operator='DE',
            model='DE01',
            question="What are the fundamental components and root causes?",
            inputs={'problem': problem},
            outputs={
                'components': components,
                'root_causes': root_causes,
                'dependencies': dependencies,
                'component_count': len(components)
            },
            insights=[
                f"Identified {len(components)} key components",
                f"Found {len(root_causes)} potential root causes",
                "Dependencies suggest " + self._analyze_complexity(dependencies)
            ],
            confidence=0.85,
            execution_time=0.15,
            timestamp=datetime.now().isoformat()
        )

    def perspective_first_principles(self, context: Dict) -> HUMMBLOutput:
        """P01: Strip away assumptions to fundamental truths"""
        problem = context.get('problem', '')

        # Identify assumptions in the problem statement
        assumptions = self._extract_assumptions(problem)

        # Derive first principles
        first_principles = self._derive_first_principles(problem, assumptions)

        # Generate fundamental questions
        fundamental_questions = self._generate_fundamental_questions(first_principles)

        return HUMMBLOutput(
            operator='P',
            model='P01',
            question="What are the fundamental truths underlying this problem?",
            inputs={'problem': problem, 'assumptions': assumptions},
            outputs={
                'first_principles': first_principles,
                'fundamental_questions': fundamental_questions,
                'assumptions_challenged': len(assumptions)
            },
            insights=[
                f"Challenged {len(assumptions)} assumptions",
                f"Derived {len(first_principles)} first principles",
                "Key insight: " + first_principles[0] if first_principles else "No clear first principles identified"
            ],
            confidence=0.78,
            execution_time=0.12,
            timestamp=datetime.now().isoformat()
        )

    def compose_modular_design(self, context: Dict) -> HUMMBLOutput:
        """CO01: Design modular system architecture"""
        components = context.get('components', [])
        dependencies = context.get('dependencies', {})

        # Design module boundaries
        modules = self._design_modules(components, dependencies)

        # Define interfaces
        interfaces = self._define_interfaces(modules)

        # Identify coupling points
        coupling_analysis = self._analyze_coupling(modules, dependencies)

        return HUMMBLOutput(
            operator='CO',
            model='CO01',
            question="How should components be organized into modules?",
            inputs={'components': components, 'dependencies': dependencies},
            outputs={
                'modules': modules,
                'interfaces': interfaces,
                'coupling_analysis': coupling_analysis,
                'modularity_score': self._calculate_modularity_score(modules)
            },
            insights=[
                f"Designed {len(modules)} modules",
                f"Defined {len(interfaces)} interfaces",
                f"Coupling score: {coupling_analysis['score']:.2f}"
            ],
            confidence=0.82,
            execution_time=0.18,
            timestamp=datetime.now().isoformat()
        )

    def invert_premortem(self, context: Dict) -> HUMMBLOutput:
        """IN01: Analyze what could cause this to fail"""
        components = context.get('components', [])
        root_causes = context.get('root_causes', [])

        # Invert success scenarios to find failure modes
        failure_scenarios = self._invert_success_scenarios(components)

        # Identify high-risk failure points
        risk_assessment = self._assess_failure_risks(failure_scenarios, root_causes)

        # Generate prevention strategies
        prevention_strategies = self._generate_prevention_strategies(risk_assessment)

        return HUMMBLOutput(
            operator='IN',
            model='IN01',
            question="What could cause this system to fail?",
            inputs={'components': components, 'root_causes': root_causes},
            outputs={
                'failure_scenarios': failure_scenarios,
                'risk_assessment': risk_assessment,
                'prevention_strategies': prevention_strategies,
                'high_risk_count': len([r for r in risk_assessment if r['risk'] > 0.7])
            },
            insights=[
                f"Identified {len(failure_scenarios)} failure scenarios",
                f"{len([r for r in risk_assessment if r['risk'] > 0.7])} high-risk areas found",
                "Top prevention priority: " + prevention_strategies[0]['strategy'] if prevention_strategies else "None identified"
            ],
            confidence=0.88,
            execution_time=0.14,
            timestamp=datetime.now().isoformat()
        )

    def synthesize_systems_view(self, context: Dict) -> HUMMBLOutput:
        """SY01: Understand system in broader context"""
        modules = context.get('modules', [])
        failure_scenarios = context.get('failure_scenarios', [])

        # Identify system-level patterns
        system_patterns = self._identify_system_patterns(modules, failure_scenarios)

        # Map ecosystem relationships
        ecosystem_map = self._map_ecosystem_relationships(modules)

        # Analyze emergent behaviors
        emergent_behaviors = self._analyze_emergent_behaviors(system_patterns)

        return HUMMBLOutput(
            operator='SY',
            model='SY01',
            question="How does this system interact with its ecosystem?",
            inputs={'modules': modules, 'failure_scenarios': failure_scenarios},
            outputs={
                'system_patterns': system_patterns,
                'ecosystem_map': ecosystem_map,
                'emergent_behaviors': emergent_behaviors,
                'system_complexity': self._assess_system_complexity(ecosystem_map)
            },
            insights=[
                f"Found {len(system_patterns)} system-level patterns",
                f"Identified {len(emergent_behaviors)} emergent behaviors",
                f"System complexity score: {self._assess_system_complexity(ecosystem_map):.2f}"
            ],
            confidence=0.76,
            execution_time=0.20,
            timestamp=datetime.now().isoformat()
        )

    def recurs_feedback_loops(self, context: Dict) -> HUMMBLOutput:
        """RE01: Identify feedback loops in the system"""
        dependencies = context.get('dependencies', {})
        failure_scenarios = context.get('failure_scenarios', [])

        # Identify feedback loops
        feedback_loops = self._identify_feedback_loops(dependencies)

        # Classify loop types (positive/negative, reinforcing/balancing)
        loop_classification = self._classify_loops(feedback_loops)

        # Analyze loop stability
        stability_analysis = self._analyze_loop_stability(loop_classification)

        return HUMMBLOutput(
            operator='RE',
            model='RE01',
            question="What feedback loops exist in this system?",
            inputs={'dependencies': dependencies, 'failure_scenarios': failure_scenarios},
            outputs={
                'feedback_loops': feedback_loops,
                'loop_classification': loop_classification,
                'stability_analysis': stability_analysis,
                'unstable_loops': len([l for l in loop_classification if not l['stable']])
            },
            insights=[
                f"Found {len(feedback_loops)} feedback loops",
                f"{len([l for l in loop_classification if not l['stable']])} potentially unstable loops",
                "Stability assessment: " + stability_analysis['overall']
            ],
            confidence=0.81,
            execution_time=0.16,
            timestamp=datetime.now().isoformat()
        )

    # Helper methods for analysis
    def _extract_components(self, problem: str) -> List[str]:
        """Extract system components from problem description"""
        # Simple pattern matching - in practice, this would use NLP
        patterns = [
            r'\b(API|database|service|cache|queue|worker)\b',
            r'\b(frontend|backend|gateway|proxy)\b',
            r'\b(user|data|content|model)\b'
        ]

        components = []
        for pattern in patterns:
            matches = re.findall(pattern, problem.lower())
            components.extend(matches)

        return list(set(components))  # Remove duplicates

    def _identify_root_causes(self, problem: str, components: List[str]) -> List[str]:
        """Identify potential root causes"""
        root_causes = []

        # Common failure patterns
        if 'timeout' in problem.lower():
            root_causes.append("Resource contention")
        if 'latency' in problem.lower():
            root_causes.append("Performance bottleneck")
        if 'error' in problem.lower():
            root_causes.append("Exception handling")

        # Component-specific causes
        for component in components:
            if component in ['database', 'cache']:
                root_causes.append(f"{component} connection issues")
            elif component in ['service', 'worker']:
                root_causes.append(f"{component} resource exhaustion")

        return list(set(root_causes))

    def _build_dependencies(self, components: List[str]) -> Dict[str, List[str]]:
        """Build dependency relationships between components"""
        dependencies = {}

        # Simple dependency rules - in practice, this would be learned
        for component in components:
            deps = []
            if component == 'api':
                deps = ['service', 'database']
            elif component == 'service':
                deps = ['database', 'cache']
            elif component == 'frontend':
                deps = ['api', 'gateway']

            dependencies[component] = deps

        return dependencies

    def _analyze_complexity(self, dependencies: Dict) -> str:
        """Analyze system complexity from dependencies"""
        total_deps = sum(len(deps) for deps in dependencies.values())
        if total_deps > 10:
            return "high complexity - consider modularization"
        elif total_deps > 5:
            return "moderate complexity - manageable"
        else:
            return "low complexity - straightforward"

    def _extract_assumptions(self, problem: str) -> List[str]:
        """Extract assumptions from problem statement"""
        assumptions = []

        # Look for assumptive language
        assumption_indicators = ['should', 'must', 'always', 'never', 'obviously']

        for indicator in assumption_indicators:
            if indicator in problem.lower():
                assumptions.append(f"Assumption: '{indicator}' implies fixed behavior")

        return assumptions

    def _derive_first_principles(self, problem: str, assumptions: List[str]) -> List[str]:
        """Derive first principles from problem and assumptions"""
        principles = [
            "Systems are composed of interacting parts",
            "Performance is limited by bottlenecks",
            "Reliability requires failure handling",
            "Scalability demands distribution"
        ]

        return principles

    def _generate_fundamental_questions(self, principles: List[str]) -> List[str]:
        """Generate fundamental questions from principles"""
        questions = []
        for principle in principles:
            questions.append(f"What does '{principle}' mean for this system?")

        return questions

    def _design_modules(self, components: List[str], dependencies: Dict) -> List[Dict]:
        """Design modular architecture"""
        modules = []

        # Group components by function
        data_components = [c for c in components if c in ['database', 'cache', 'data']]
        compute_components = [c for c in components if c in ['service', 'worker', 'model']]
        interface_components = [c for c in components if c in ['api', 'frontend', 'gateway']]

        if data_components:
            modules.append({
                'name': 'Data Layer',
                'components': data_components,
                'responsibility': 'Data persistence and access'
            })

        if compute_components:
            modules.append({
                'name': 'Compute Layer',
                'components': compute_components,
                'responsibility': 'Business logic and processing'
            })

        if interface_components:
            modules.append({
                'name': 'Interface Layer',
                'components': interface_components,
                'responsibility': 'External interactions'
            })

        return modules

    def _define_interfaces(self, modules: List[Dict]) -> List[Dict]:
        """Define interfaces between modules"""
        interfaces = []

        for i, module_a in enumerate(modules):
            for module_b in modules[i+1:]:
                interfaces.append({
                    'from': module_a['name'],
                    'to': module_b['name'],
                    'contract': f"{module_a['name']} → {module_b['name']} API",
                    'data_flow': 'bidirectional'
                })

        return interfaces

    def _analyze_coupling(self, modules: List[Dict], dependencies: Dict) -> Dict:
        """Analyze coupling between modules"""
        total_deps = sum(len(deps) for deps in dependencies.values())
        module_count = len(modules)

        coupling_score = total_deps / max(module_count * (module_count - 1), 1)

        return {
            'score': coupling_score,
            'assessment': 'tightly coupled' if coupling_score > 0.8 else 'loosely coupled',
            'recommendations': ['Consider interface simplification'] if coupling_score > 0.8 else []
        }

    def _calculate_modularity_score(self, modules: List[Dict]) -> float:
        """Calculate modularity score"""
        if not modules:
            return 0.0

        # Simple scoring based on module separation
        total_components = sum(len(m['components']) for m in modules)
        module_count = len(modules)

        # Higher score for better distribution
        if module_count == 0:
            return 0.0

        avg_components_per_module = total_components / module_count
        balance_score = 1.0 - abs(avg_components_per_module - 2.0) / 4.0  # Optimal ~2 components/module

        return max(0.0, min(1.0, balance_score))

    def _invert_success_scenarios(self, components: List[str]) -> List[Dict]:
        """Invert success scenarios to find failure modes"""
        failure_scenarios = []

        for component in components:
            if component == 'database':
                failure_scenarios.extend([
                    {'component': component, 'failure': 'connection timeout', 'impact': 'high'},
                    {'component': component, 'failure': 'disk full', 'impact': 'critical'},
                    {'component': component, 'failure': 'corruption', 'impact': 'critical'}
                ])
            elif component == 'api':
                failure_scenarios.extend([
                    {'component': component, 'failure': 'rate limit exceeded', 'impact': 'medium'},
                    {'component': component, 'failure': 'authentication failure', 'impact': 'high'}
                ])
            elif component == 'service':
                failure_scenarios.extend([
                    {'component': component, 'failure': 'memory leak', 'impact': 'high'},
                    {'component': component, 'failure': 'deadlock', 'impact': 'critical'}
                ])

        return failure_scenarios

    def _assess_failure_risks(self, failure_scenarios: List[Dict], root_causes: List[str]) -> List[Dict]:
        """Assess risk levels for failure scenarios"""
        risk_assessment = []

        for scenario in failure_scenarios:
            risk_score = 0.5  # Base risk

            # Increase risk based on impact
            if scenario['impact'] == 'critical':
                risk_score += 0.4
            elif scenario['impact'] == 'high':
                risk_score += 0.2

            # Increase risk if related to root causes
            for cause in root_causes:
                if scenario['component'].lower() in cause.lower():
                    risk_score += 0.2

            risk_assessment.append({
                'scenario': scenario,
                'risk': min(1.0, risk_score),
                'priority': 'high' if risk_score > 0.7 else 'medium' if risk_score > 0.4 else 'low'
            })

        return risk_assessment

    def _generate_prevention_strategies(self, risk_assessment: List[Dict]) -> List[Dict]:
        """Generate prevention strategies for high-risk scenarios"""
        strategies = []

        for assessment in risk_assessment:
            if assessment['risk'] > 0.6:
                scenario = assessment['scenario']
                component = scenario['component']
                failure = scenario['failure']

                if 'timeout' in failure:
                    strategies.append({
                        'component': component,
                        'failure': failure,
                        'strategy': f'Implement circuit breaker for {component}',
                        'effort': 'medium'
                    })
                elif 'memory' in failure:
                    strategies.append({
                        'component': component,
                        'failure': failure,
                        'strategy': f'Add memory monitoring and limits for {component}',
                        'effort': 'low'
                    })
                elif 'disk' in failure:
                    strategies.append({
                        'component': component,
                        'failure': failure,
                        'strategy': f'Implement disk usage alerts and cleanup for {component}',
                        'effort': 'medium'
                    })

        return strategies

    def _identify_system_patterns(self, modules: List[Dict], failure_scenarios: List[Dict]) -> List[str]:
        """Identify system-level patterns"""
        patterns = []

        # Analyze module interactions
        if len(modules) >= 3:
            patterns.append("Multi-layer architecture with separation of concerns")

        # Analyze failure patterns
        critical_failures = [s for s in failure_scenarios if s['impact'] == 'critical']
        if len(critical_failures) > 2:
            patterns.append("Single points of failure concentrated in data layer")

        # Common patterns
        patterns.extend([
            "Request-response flow with potential cascading failures",
            "Resource contention between compute and data layers",
            "External dependency on third-party services"
        ])

        return patterns

    def _map_ecosystem_relationships(self, modules: List[Dict]) -> Dict:
        """Map relationships with external systems"""
        ecosystem = {
            'internal': [m['name'] for m in modules],
            'external': ['User clients', 'Third-party APIs', 'Monitoring systems', 'CI/CD pipeline'],
            'relationships': []
        }

        # Define relationships
        for internal in ecosystem['internal']:
            for external in ecosystem['external']:
                if 'User' in external and 'Interface' in internal:
                    ecosystem['relationships'].append({
                        'from': internal,
                        'to': external,
                        'type': 'user_interaction'
                    })
                elif 'API' in external and 'Interface' in internal:
                    ecosystem['relationships'].append({
                        'from': internal,
                        'to': external,
                        'type': 'api_integration'
                    })

        return ecosystem

    def _analyze_emergent_behaviors(self, system_patterns: List[str]) -> List[str]:
        """Analyze emergent system behaviors"""
        behaviors = []

        for pattern in system_patterns:
            if 'cascading' in pattern:
                behaviors.append("Cascading failure amplification")
            elif 'resource' in pattern:
                behaviors.append("Resource competition under load")
            elif 'separation' in pattern:
                behaviors.append("Fault isolation between layers")

        behaviors.extend([
            "Adaptive performance degradation",
            "Self-healing through retries",
            "Load distribution across instances"
        ])

        return behaviors

    def _assess_system_complexity(self, ecosystem_map: Dict) -> float:
        """Assess overall system complexity"""
        internal_count = len(ecosystem_map.get('internal', []))
        external_count = len(ecosystem_map.get('external', []))
        relationship_count = len(ecosystem_map.get('relationships', []))

        # Complexity increases with interconnections
        complexity = (internal_count * external_count * relationship_count) / 100.0

        return min(1.0, complexity)

    def _identify_feedback_loops(self, dependencies: Dict) -> List[List[str]]:
        """Identify feedback loops in dependencies"""
        loops = []

        # Simple cycle detection - in practice, use proper graph algorithms
        for component, deps in dependencies.items():
            for dep in deps:
                if dep in dependencies and component in dependencies[dep]:
                    loops.append([component, dep, component])

        return loops

    def _classify_loops(self, feedback_loops: List[List[str]]) -> List[Dict]:
        """Classify feedback loops by type and stability"""
        classifications = []

        for loop in feedback_loops:
            # Simple classification - positive loops amplify, negative dampen
            loop_type = 'positive' if len(loop) % 2 == 1 else 'negative'
            stability = loop_type == 'negative'  # Negative loops are stabilizing

            classifications.append({
                'loop': loop,
                'type': loop_type,
                'reinforcing': loop_type == 'positive',
                'stable': stability,
                'description': f"{'Reinforcing' if loop_type == 'positive' else 'Balancing'} feedback loop"
            })

        return classifications

    def _analyze_loop_stability(self, loop_classifications: List[Dict]) -> Dict:
        """Analyze overall system stability from loops"""
        stable_loops = len([l for l in loop_classifications if l['stable']])
        unstable_loops = len(loop_classifications) - stable_loops

        if unstable_loops > stable_loops:
            overall = "potentially unstable - monitor closely"
        elif unstable_loops > 0:
            overall = "mixed stability - some risk areas"
        else:
            overall = "stable system dynamics"

        return {
            'overall': overall,
            'stable_loops': stable_loops,
            'unstable_loops': unstable_loops,
            'recommendations': [
                "Add monitoring for unstable loops" if unstable_loops > 0 else "System appears stable"
            ]
        }


def main():
    """Demonstrate HUMMBL workflow execution"""

    # Initialize workflow engine
    workflow = HUMMBLWorkflow()

    # Example problem
    problem = """
    Our e-commerce API is experiencing timeouts during peak traffic.
    The system includes a gateway, user service, product service, and database.
    Timeouts seem to cascade, causing the entire system to fail.
    """

    # Execute debugging sequence
    sequence = ['DE01', 'P01', 'CO01', 'IN01', 'SY01', 'RE01']

    print(f"🔍 Analyzing problem: {problem.strip()}")
    print(f"📋 Executing HUMMBL sequence: {' → '.join(sequence)}")
    print("=" * 80)

    results = workflow.execute_sequence(problem, sequence)

    # Display results
    for result in results:
        print(f"\n🧠 {result.operator}{result.model}: {result.question}")
        print(f"⏱️  Execution time: {result.execution_time:.3f}s")
        print(f"🎯 Confidence: {result.confidence:.2f}")

        if result.outputs:
            print("📊 Key outputs:")
            for key, value in result.outputs.items():
                if isinstance(value, list):
                    print(f"   • {key}: {len(value)} items")
                elif isinstance(value, dict):
                    print(f"   • {key}: {len(value)} properties")
                else:
                    print(f"   • {key}: {value}")

        if result.insights:
            print("💡 Insights:")
            for insight in result.insights[:2]:  # Show first 2
                print(f"   • {insight}")

    print("\n" + "=" * 80)
    print("✅ HUMMBL analysis complete!")
    print("💡 Use these structured outputs to guide your engineering decisions.")


if __name__ == "__main__":
    main()