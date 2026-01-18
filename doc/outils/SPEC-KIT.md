https://github.com/github/spec-kit

🌱 Spec Kit
Build high-quality software faster.
An open source toolkit that allows you to focus on product scenarios and predictable outcomes instead of vibe coding every piece from scratch.

Release GitHub stars License Documentation

Table of Contents
🤔 What is Spec-Driven Development?
⚡ Get Started
📽️ Video Overview
🤖 Supported AI Agents
🔧 Specify CLI Reference
📚 Core Philosophy
🌟 Development Phases
🎯 Experimental Goals
🔧 Prerequisites
📖 Learn More
📋 Detailed Process
🔍 Troubleshooting
👥 Maintainers
💬 Support
🙏 Acknowledgements
📄 License
🤔 What is Spec-Driven Development?
Spec-Driven Development flips the script on traditional software development. For decades, code has been king — specifications were just scaffolding we built and discarded once the "real work" of coding began. Spec-Driven Development changes this: specifications become executable, directly generating working implementations rather than just guiding them.

⚡ Get Started
1. Install Specify CLI
Choose your preferred installation method:

Option 1: Persistent Installation (Recommended)
Install once and use everywhere:

uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
Then use the tool directly:

specify init <PROJECT_NAME>
specify check
To upgrade Specify, see the Upgrade Guide for detailed instructions. Quick upgrade:

uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git
Option 2: One-time Usage
Run directly without installing:

uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>
Benefits of persistent installation:

Tool stays installed and available in PATH
No need to create shell aliases
Better tool management with uv tool list, uv tool upgrade, uv tool uninstall
Cleaner shell configuration
2. Establish project principles
Launch your AI assistant in the project directory. The /speckit.* commands are available in the assistant.

Use the /speckit.constitution command to create your project's governing principles and development guidelines that will guide all subsequent development.

/speckit.constitution Create principles focused on code quality, testing standards, user experience consistency, and performance requirements
3. Create the spec
Use the /speckit.specify command to describe what you want to build. Focus on the what and why, not the tech stack.

/speckit.specify Build an application that can help me organize my photos in separate photo albums. Albums are grouped by date and can be re-organized by dragging and dropping on the main page. Albums are never in other nested albums. Within each album, photos are previewed in a tile-like interface.
4. (Optional) Clarify ambiguous areas
If your specification contains vague areas or undefined technical decisions, use /speckit.clarify before creating the plan. This command asks structured questions to identify and reduce risks.

/speckit.clarify
5. Create a technical implementation plan
Use the /speckit.plan command to provide your tech stack and architecture choices.

/speckit.plan The application uses Vite with minimal number of libraries. Use vanilla HTML, CSS, and JavaScript as much as possible. Images are not uploaded anywhere and metadata is stored in a local SQLite database.
6. Break down into tasks
Use /speckit.tasks to create an actionable task list from your implementation plan.

/speckit.tasks
7. (Optional) Analyze consistency
Before implementing, verify that all artifacts are consistent and aligned. Use /speckit.analyze to generate a cross-artifact consistency and coverage analysis report.

/speckit.analyze
8. (Optional) Generate quality checklist
Create a checklist to validate quality before implementation. Use /speckit.checklist to generate personalized checklists for different aspects (tests, security, accessibility, etc.).

/speckit.checklist Generate a checklist for tests, security, and accessibility
9. Execute implementation
Use /speckit.implement to execute all tasks and build your feature according to the plan.

/speckit.implement

Recommended Workflow:
Constitution → Specification → [Clarification] → Plan → Tasks → [Analysis] → [Checklist] → Implementation
For detailed step-by-step instructions, see our comprehensive guide.

📽️ Video Overview
Want to see Spec Kit in action? Watch our video overview!

Spec Kit video header

🤖 Supported AI Agents
Agent	Support	Notes
Claude Code	✅
GitHub Copilot	✅
Gemini CLI	✅
Cursor	✅
Qwen Code	✅
opencode	✅
Windsurf	✅
Kilo Code	✅
Auggie CLI	✅
CodeBuddy CLI	✅
Roo Code	✅
Codex CLI	✅
Amazon Q Developer CLI	⚠️	Amazon Q Developer CLI does not support custom arguments for slash commands.
Amp	✅
SHAI (OVHcloud)	✅
🔧 Specify CLI Reference
The specify command supports the following options:

Commands
Command	Description
init	Initialize a new Specify project from the latest template
check	Check for installed tools (git, claude, gemini, code/code-insiders, cursor-agent, windsurf, qwen, opencode, codex, shai)
specify init Arguments & Options
Argument/Option	Type	Description
<project-name>	Argument	Name for your new project directory (optional if using --here, or use . for current directory)
--ai	Option	AI assistant to use: claude, gemini, copilot, cursor-agent, qwen, opencode, codex, windsurf, kilocode, auggie, roo, codebuddy, amp, shai, or q
--script	Option	Script variant to use: sh (bash/zsh) or ps (PowerShell)
--ignore-agent-tools	Flag	Skip checks for AI agent tools like Claude Code
--no-git	Flag	Skip git repository initialization
--here	Flag	Initialize project in the current directory instead of creating a new one
--force	Flag	Force merge/overwrite when initializing in current directory (skip confirmation)
--skip-tls	Flag	Skip SSL/TLS verification (not recommended)
--debug	Flag	Enable detailed debug output for troubleshooting
--github-token	Option	GitHub token for API requests (or set GH_TOKEN/GITHUB_TOKEN env variable)
Examples
# Basic project initialization
specify init my-project

# Initialize with specific AI assistant
specify init my-project --ai claude

# Initialize with Cursor support
specify init my-project --ai cursor-agent

# Initialize with Windsurf support
specify init my-project --ai windsurf

# Initialize with Amp support
specify init my-project --ai amp

# Initialize with SHAI support
specify init my-project --ai shai

# Initialize with PowerShell scripts (Windows/cross-platform)
specify init my-project --ai copilot --script ps

# Initialize in current directory
specify init . --ai copilot
# or use the --here flag
specify init --here --ai copilot

# Force merge into current (non-empty) directory without confirmation
specify init . --force --ai copilot
# or
specify init --here --force --ai copilot

# Skip git initialization
specify init my-project --ai gemini --no-git

# Enable debug output for troubleshooting
specify init my-project --ai claude --debug

# Use GitHub token for API requests (helpful for corporate environments)
specify init my-project --ai claude --github-token ghp_your_token_here

# Check system requirements
specify check
Available Slash Commands
After running specify init, your AI coding agent will have access to these slash commands for structured development:

Core Commands
Essential commands for the Spec-Driven Development workflow:

Command	Description
/speckit.constitution	Create or update project governing principles and development guidelines
/speckit.specify	Define what you want to build (requirements and user stories)
/speckit.plan	Create technical implementation plans with your chosen tech stack
/speckit.tasks	Generate actionable task lists for implementation
/speckit.implement	Execute all tasks to build the feature according to the plan
Optional Commands
Additional commands for enhanced quality and validation:

These commands improve quality and robustness by identifying ambiguous areas, verifying consistency, and generating validation checklists.

Command	Description	When to Use	Example
/speckit.clarify	Ask structured questions to identify and reduce risks related to ambiguous or underspecified areas. Helps de-risk before technical planning. Formerly known as /quizme.	Recommended before /speckit.plan if your specification contains vague areas or undefined technical decisions	/speckit.clarify (no arguments - automatic analysis)
/speckit.analyze	Cross-artifact consistency & coverage analysis between all artifacts (constitution, specification, plan, tasks). Generates an alignment report to ensure everything is consistent.	After /speckit.tasks, before /speckit.implement to validate that the plan and tasks align with the specification	/speckit.analyze
/speckit.checklist	Generate custom quality checklists that validate requirements completeness, clarity, and consistency. Can be used for different aspects (tests, security, accessibility, etc.). Like "unit tests for English" - generates domain-specific validation checklists.	At any time for validation, particularly after /speckit.plan or before implementation	/speckit.checklist Generate a checklist for unit tests and accessibility

Details on /speckit.clarify:
This command is particularly useful when:
- Your specification contains vague or ambiguous terms
- Important technical decisions have not been made
- You need to clarify constraints or non-functional requirements
- The project scope is not clearly defined

The command automatically analyzes your specification and asks targeted questions to clarify ambiguous areas.

Details on /speckit.analyze:
This command verifies:
- Consistency between constitution and specification
- Alignment of technical plan with requirements
- Complete coverage of features in tasks
- Potential inconsistencies between different artifacts

Generates a detailed report that can reveal issues before implementation.

Details on /speckit.checklist:
This command generates personalized checklists for different aspects:
- Tests (unit, integration, E2E)
- Code quality
- Security
- Accessibility (WCAG)
- Performance
- Documentation

Examples:
/speckit.checklist
/speckit.checklist Generate a checklist for tests and security
/speckit.checklist Checklist for WCAG 2.1 AA accessibility
Environment Variables
Variable	Description
SPECIFY_FEATURE	Override feature detection for non-Git repositories. Set to the feature directory name (e.g., 001-photo-albums) to work on a specific feature when not using Git branches.
**Must be set in the context of the agent you're working with prior to using /speckit.plan or follow-up commands.
📚 Core Philosophy
Spec-Driven Development is a structured process that emphasizes:

Intent-driven development where specifications define the "what" before the "how"
Rich specification creation using guardrails and organizational principles
Multi-step refinement rather than one-shot code generation from prompts
Heavy reliance on advanced AI model capabilities for specification interpretation
🌟 Development Phases
Phase	Focus	Key Activities
0-to-1 Development ("Greenfield")	Generate from scratch
Start with high-level requirements
Generate specifications
Plan implementation steps
Build production-ready applications
Creative Exploration	Parallel implementations
Explore diverse solutions
Support multiple technology stacks & architectures
Experiment with UX patterns
Iterative Enhancement ("Brownfield")	Brownfield modernization
Add features iteratively
Modernize legacy systems
Adapt processes
🎯 Experimental Goals
Our research and experimentation focus on:

Technology independence
Create applications using diverse technology stacks
Validate the hypothesis that Spec-Driven Development is a process not tied to specific technologies, programming languages, or frameworks
Enterprise constraints
Demonstrate mission-critical application development
Incorporate organizational constraints (cloud providers, tech stacks, engineering practices)
Support enterprise design systems and compliance requirements
User-centric development
Build applications for different user cohorts and preferences
Support various development approaches (from vibe-coding to AI-native development)
Creative & iterative processes
Validate the concept of parallel implementation exploration
Provide robust iterative feature development workflows
Extend processes to handle upgrades and modernization tasks
🔧 Prerequisites
Linux/macOS/Windows
Supported AI coding agent.
uv for package management
Python 3.11+
Git
If you encounter issues with an agent, please open an issue so we can refine the integration.

📖 Learn More
Complete Spec-Driven Development Methodology - Deep dive into the full process
Detailed Walkthrough - Step-by-step implementation guide
📋 Detailed Process
Click to expand the detailed step-by-step walkthrough
🔍 Troubleshooting
Git Credential Manager on Linux
If you're having issues with Git authentication on Linux, you can install Git Credential Manager:

#!/usr/bin/env bash
set -e
echo "Downloading Git Credential Manager v2.6.1..."
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
echo "Installing Git Credential Manager..."
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
echo "Configuring Git to use GCM..."
git config --global credential.helper manager
echo "Cleaning up..."
rm gcm-linux_amd64.2.6.1.deb
👥 Maintainers
Den Delimarsky (@localden)
John Lam (@jflam)
💬 Support
For support, please open a GitHub issue. We welcome bug reports, feature requests, and questions about using Spec-Driven Development.

🙏 Acknowledgements
This project is heavily influenced by and based on the work and research of John Lam.

📄 License
This project is licensed under the terms of the MIT open source license. Please refer to the LICENSE file for the full terms.