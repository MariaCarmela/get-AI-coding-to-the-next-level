# ReasonCritique Multi-Agent System Architecture

## Overview

The ReasonCritique system is a multi-agent architecture designed to perform structured analysis of technical texts. It follows a modular, parallel workflow to ensure accuracy, completeness, and efficiency in producing verified analyses.

## Architecture Components

### 1. Orchestrator Agent (ReasonCritique)
- **Role**: Central coordinator that manages the analysis workflow
- **Responsibilities**:
  - Reads input text (from file or direct input)
  - Delegates tasks to specialized subagents
  - Collects and integrates outputs
  - Ensures final output format compliance
- **Tools**: `read` (for file input), `agent` (for subagent delegation)
- **Workflow Strategy**: Parallel delegation to generation agents, followed by sequential verification

### 2. Generation Agents (Parallel Execution)
These agents run concurrently to maximize efficiency:

#### Summarizer Agent
- **Role**: Produces concise executive summaries
- **Input**: Full original text
- **Output**: 3-5 sentence summary capturing main purpose, scope, and conclusions
- **Tools**: `read`
- **Constraints**: No themes/insights, only summarization; grounded in original text

#### ThemeInsight Agent
- **Role**: Identifies themes and extracts key insights
- **Input**: Full original text
- **Output**: 
  - 3-6 main themes with descriptions
  - 3-6 key insights with descriptions
- **Tools**: `read`
- **Constraints**: Themes are broad topics; insights are specific findings; all grounded in text

### 3. Verification Agent (Sequential Execution)

#### Critic Agent
- **Role**: Validates and corrects analysis outputs
- **Input**: Original text + outputs from Summarizer and ThemeInsight
- **Output**: Verified/corrected summary, themes, and insights with validation status
- **Tools**: `read`
- **Responsibilities**:
  - Checks accuracy against original text
  - Identifies hallucinations or omissions
  - Ensures consistency between components
  - Provides corrections when needed

## Workflow Execution

1. **Input Processing**: Orchestrator reads the technical text
2. **Parallel Generation**: Summarizer and ThemeInsight process the text concurrently
3. **Sequential Verification**: Critic reviews all outputs against the original
4. **Final Assembly**: Orchestrator composes the structured analysis based on verified components

## Design Rationale

### Parallel vs Sequential Trade-offs
- **Parallel Generation**: Improves performance by running independent analyses simultaneously
- **Sequential Verification**: Ensures quality control without parallel complexity
- **Orchestrator Separation**: Maintains clean separation between coordination and analysis

### Modularity Benefits
- **Scalability**: Easy to add new specialized agents
- **Maintainability**: Clear responsibilities per agent
- **Testability**: Each agent can be tested independently
- **Robustness**: Verification layer catches errors from generation agents

### Tool Minimization
- Only essential tools included (`read` for input access, `agent` for delegation)
- No unnecessary search or external tools to maintain focus on text analysis

## Output Structure

The system produces a standardized Markdown format:

```markdown
## Summary
[Verified executive summary]

## Themes
- Theme 1: [description]
- Theme 2: [description]
- ...

## Key Insights
- Insight 1: [description]
- Insight 2: [description]
- ...
```

## Quality Assurance

- **Grounding**: All outputs must be traceable to the original text
- **Consistency**: Summary, themes, and insights must align
- **Accuracy**: Verification prevents hallucinations and omissions
- **Completeness**: Critic ensures no critical information is missing

## Future Extensions

The modular architecture supports:
- Additional specialized analyzers (e.g., code analysis, security review)
- Different output formats
- Integration with external verification sources
- Performance optimizations through further parallelization