# HUMMBL Workflow Checklists

Practical checklists for applying HUMMBL operators in engineering scenarios. Each checklist provides step-by-step guidance for executing mental models.

## Debugging Checklist (P18 → DE06 → IN01 → SY04)

### P18: Systems Thinking

- [ ] **View problem holistically**: Consider how this issue affects the entire system, not just the failing component
- [ ] **Map interconnections**: Draw connections between components, data flows, and dependencies
- [ ] **Identify feedback loops**: Look for cycles where A affects B, which affects A
- [ ] **Consider time dimensions**: How does this problem evolve over time?
- [ ] **Question**: "What system-level patterns am I missing?"

### DE06: Failure Mode Analysis
- [ ] **List all components**: Identify every service, database, cache, queue, and external dependency
- [ ] **For each component, ask**: "How can this fail?"
  - Network timeouts, connection failures
  - Resource exhaustion (CPU, memory, disk)
  - Data corruption or loss
  - Configuration errors
  - Third-party service outages
- [ ] **Rate failure impacts**: High/Medium/Low for each failure mode
- [ ] **Document failure symptoms**: What would you observe for each failure?
- [ ] **Question**: "What's the complete failure landscape?"

### IN01: Premortem Analysis
- [ ] **Invert success**: "What would have to fail for this to be working?"
- [ ] **Worst-case scenarios**: What are the most damaging failure combinations?
- [ ] **Hidden assumptions**: What must be true for the system to work?
- [ ] **Early warning signs**: What subtle indicators precede major failures?
- [ ] **Prevention strategies**: What could prevent each failure scenario?
- [ ] **Question**: "How could this get worse before we notice?"

### SY04: Cascade Analysis
- [ ] **Map failure propagation**: If Component A fails, what fails next?
- [ ] **Identify amplification points**: Where does one failure trigger many?
- [ ] **Find critical paths**: Which failure chains cause the most damage?
- [ ] **Assess recovery time**: How long does each cascade take to resolve?
- [ ] **Design circuit breakers**: Where to add isolation to prevent cascades?
- [ ] **Question**: "How do failures spread through the system?"

## Architecture Design Checklist (P01 → DE01 → CO01 → SY01)

### P01: First Principles Thinking
- [ ] **Strip assumptions**: What do you "know" that might not be true?
- [ ] **Fundamental truths**: What physical, technical, or business laws apply?
- [ ] **Core requirements**: What must the system absolutely do?
- [ ] **Remove constraints**: If cost/time weren't factors, what would you build?
- [ ] **Rebuild from scratch**: How would you design this with perfect knowledge?
- [ ] **Question**: "What are the immutable truths here?"

### DE01: Root Cause Analysis
- [ ] **5 Whys technique**: Ask "why" repeatedly until you reach root cause
- [ ] **Component breakdown**: Divide system into smallest functional units
- [ ] **Dependency mapping**: What does each component absolutely need?
- [ ] **Failure isolation**: Which components can fail independently?
- [ ] **Interface identification**: Where do components interact?
- [ ] **Question**: "What are the fundamental building blocks?"

### CO01: Modular Design
- [ ] **Single responsibility**: Each module does one thing well
- [ ] **Interface design**: Clean contracts between modules
- [ ] **Dependency injection**: Modules don't create their dependencies
- [ ] **Testability**: Each module can be tested in isolation
- [ ] **Replaceability**: Modules can be swapped without affecting others
- [ ] **Question**: "How do these components fit together?"

### SY01: System-of-Systems View
- [ ] **Ecosystem mapping**: How does this system interact with others?
- [ ] **Data flows**: Where does information enter/exit the system?
- [ ] **External dependencies**: What other systems must be available?
- [ ] **Scaling boundaries**: Where does this system stop and others begin?
- [ ] **Integration points**: How does this fit into the larger architecture?
- [ ] **Question**: "How does this system serve the broader ecosystem?"

## Performance Optimization Checklist (DE02 → P19 → CO03 → RE16)

### DE02: Value Stream Mapping
- [ ] **Map the flow**: Trace requests from entry to completion
- [ ] **Identify bottlenecks**: Where do requests queue or slow down?
- [ ] **Measure latency**: Time spent in each component
- [ ] **Find waste**: Steps that don't add value
- [ ] **Document handoffs**: Where work transfers between components
- [ ] **Question**: "Where does time get spent?"

### P19: Opportunity Cost Analysis
- [ ] **Current performance**: What's the baseline performance?
- [ ] **Cost of optimization**: Time, complexity, risk of each improvement
- [ ] **Expected benefit**: How much performance gain from each option?
- [ ] **Alternative uses**: What else could you build with that time?
- [ ] **Diminishing returns**: When does optimization cost more than it saves?
- [ ] **Question**: "Is this optimization worth the cost?"

### CO03: Pipeline Design
- [ ] **Stage identification**: Break work into sequential stages
- [ ] **Parallel opportunities**: Which stages can run simultaneously?
- [ ] **Queue management**: Where to buffer work between stages
- [ ] **Backpressure handling**: What happens when downstream is slow?
- [ ] **Error handling**: How to handle failures in each stage
- [ ] **Question**: "How can work flow more efficiently?"

### RE16: Recursive Optimization
- [ ] **Meta-optimization**: Optimize the optimization process itself
- [ ] **Measurement improvement**: Better ways to measure performance
- [ ] **Automation**: Tools to continuously monitor and adjust
- [ ] **Feedback integration**: Use results to improve future optimizations
- [ ] **Scaling optimization**: Apply successful patterns to other areas
- [ ] **Question**: "How can I optimize the optimization?"

## Feature Development Checklist (CO04 → DE19 → IN17 → SY17)

### CO04: Interface Design
- [ ] **User needs first**: Design for how people actually use the feature
- [ ] **Progressive disclosure**: Show basic features first, advanced later
- [ ] **Error prevention**: Design to prevent common mistakes
- [ ] **Feedback systems**: Clear indication of actions and results
- [ ] **Accessibility**: Works for all users regardless of ability
- [ ] **Question**: "How will people actually interact with this?"

### DE19: Responsibility Decomposition
- [ ] **Clear ownership**: Each feature/component has one clear owner
- [ ] **Separation of concerns**: UI, business logic, and data are separate
- [ ] **Dependency management**: Minimize coupling between components
- [ ] **Error boundaries**: Failures in one area don't break others
- [ ] **Testing boundaries**: Each component can be tested independently
- [ ] **Question**: "Who is responsible for what?"

### IN17: Assumption Inversion
- [ ] **Challenge requirements**: What if the stated needs are wrong?
- [ ] **User behavior**: What if users behave differently than expected?
- [ ] **Technical constraints**: What if current tech choices limit us?
- [ ] **Business priorities**: What if business goals change?
- [ ] **Market conditions**: What if the market evolves differently?
- [ ] **Question**: "What if everything we assume is wrong?"

### SY17: Paradox Resolution
- [ ] **Identify conflicts**: Where do requirements seem contradictory?
- [ ] **Higher perspective**: Find the underlying need behind conflicting requirements
- [ ] **Creative solutions**: Both/and solutions instead of either/or choices
- [ ] **Trade-off clarity**: Make explicit trade-offs visible and understandable
- [ ] **Iterative refinement**: Test solutions and learn from results
- [ ] **Question**: "How can we satisfy seemingly conflicting needs?"

## Incident Response Checklist (DE06 → CO17 → RE06 → SY19)

### DE06: Failure Mode Analysis
- [ ] **Symptom documentation**: What exactly is failing and how?
- [ ] **Scope assessment**: How many users/services are affected?
- [ ] **Timeline reconstruction**: When did this start? What changed?
- [ ] **Log analysis**: Error patterns and frequencies
- [ ] **Dependency checking**: Are related services also failing?
- [ ] **Question**: "What exactly is broken and why?"

### CO17: Orchestration Patterns
- [ ] **Service coordination**: Which services need to work together for recovery?
- [ ] **Rollback procedures**: How to safely undo recent changes?
- [ ] **Traffic management**: Route traffic away from failing components
- [ ] **Resource scaling**: Add capacity to handle increased load
- [ ] **Communication coordination**: Who needs to know what and when?
- [ ] **Question**: "How do we coordinate the recovery?"

### RE06: Feedback Loops
- [ ] **Monitoring alerts**: Are alerts creating alert fatigue?
- [ ] **Retry logic**: Are retries making problems worse?
- [ ] **Auto-scaling**: Is scaling creating oscillation?
- [ ] **User behavior**: Are users making problems worse through retries?
- [ ] **Team response**: Is the response process creating delays?
- [ ] **Question**: "What responses are making this worse?"

### SY19: Meta-Synthesis
- [ ] **Pattern recognition**: What similar incidents have we had?
- [ ] **Prevention effectiveness**: Did previous fixes actually help?
- [ ] **Process improvements**: What in our incident process needs fixing?
- [ ] **Tool assessment**: Are our monitoring/tools adequate?
- [ ] **Team learning**: What did we learn that changes how we work?
- [ ] **Question**: "How can we prevent this type of incident?"

## Daily Standup Integration

### Quick HUMMBL Check
- [ ] **P01**: Question one assumption from yesterday's plan
- [ ] **DE01**: Identify one potential root cause for any blocker
- [ ] **CO01**: Ensure tasks have clear interfaces/dependencies
- [ ] **IN01**: Consider what could go wrong with today's plan
- [ ] **Question**: "What's one insight that changes how we work?"

### Sprint Planning Integration
- [ ] **P18**: Consider sprint goals in system context
- [ ] **DE02**: Map value stream for planned features
- [ ] **CO03**: Design feature rollout pipeline
- [ ] **SY01**: Consider ecosystem impact of sprint goals
- [ ] **Question**: "How does this sprint serve the larger system?"

## Code Review Integration

### Reviewer Checklist
- [ ] **CO04**: Does the interface serve user needs well?
- [ ] **DE19**: Are responsibilities clearly separated?
- [ ] **IN17**: What assumptions might be problematic?
- [ ] **SY17**: Does this resolve any paradoxes in requirements?
- [ ] **Question**: "Does this code make the system better?"

### Author Checklist
- [ ] **P01**: Did I question assumptions in requirements?
- [ ] **DE01**: Did I identify and address root causes?
- [ ] **CO01**: Is the code modular and well-interfaced?
- [ ] **IN01**: Did I consider failure modes?
- [ ] **Question**: "Did I think deeply about this implementation?"

## Tool Integration Ideas

### VS Code Extension
```json
{
  "hummbl.checklists": {
    "debugging": ["P18", "DE06", "IN01", "SY04"],
    "architecture": ["P01", "DE01", "CO01", "SY01"],
    "performance": ["DE02", "P19", "CO03", "RE16"]
  }
}
```

### GitHub Integration
- PR template with HUMMBL checklist
- Automated checklist validation
- Integration with issue tracking

### CLI Tool
```bash
# Start debugging workflow
hummbl workflow start debugging --problem "API timeouts"

# Execute next step
hummbl step next --notes "Found database connection pool exhaustion"

# Complete workflow
hummbl workflow complete --insights "Need circuit breaker pattern"
```

Remember: HUMMBL operators are most powerful when used together in sequences. Start with simple checklists and gradually incorporate more operators as you become comfortable with the mental models.