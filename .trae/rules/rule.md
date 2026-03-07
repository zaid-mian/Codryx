Workflow Orchestration
###1. Plan Node Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions) - If something goes sideways, STOP and re-plan immediately - don't keep pushing - Use plan mode for verification steps, not just building - Write detailed specs upfront to reduce ambiguity
##₩ 2. Subagent Strategy
- Use subagents liberally to keep main context window clear - Offload research, exploration, and parallel analysis to subagents For complex problems, throw more compute at it via subagents One tack per subagent for focused executior
###3. Self-Improvement Loop ⁃ After ANY correction from the user: update `tasks/lessons.md with the patterr - Write rules for yourself that prevent the same mistake Ruthlessly iterate on these lessons until mistake rate drops - Review lessons at session start for relevant project
### 4. Verification Before Done - Never mark a task complete without proving it works - Diff behavior between main and your changes when relevant - Ask yourself: "Would a staff engineer approve this?" - Run tests, check logs, demonstrate correctness
### 5. Demand Elegance (Balanced - For non-trivial changes: pause and ask "is there a more elegant way?" - If a fix feels hacky: "Knowing everything I know now, implement the elegant solution" - Skip this for simple, obvious fixes - don't over-engineer - Challenge your own work before presenting it
###6. Autonomous Bug Fizing When given a bug report: just fix it. Don't ask for hand-holding - Point at logs, errors, failing tests - then resolve them Zero context switching required from the user Go fix failing CI tests without being told how
76
Task Management
1. *Plan First*k: Write plan to `tasks/todo.md` with checkable items 2. **Verify Plan**: Check in before starting implementatior 3. *Track Progress*k: Mark items complete as you go 4. *Explain Changes**: High-level summary at each step 5. *Document Results*k: Add review section to `tasks/todo.md 5. *k*Capture Lessons*k: Update `tasks/lessons.md` after corrections
11
## Core Principles
- *Simplicity First₩k: Make every change as simple as possible. Impact minima **No Laziness*k: Find root No temporary fixes. Senior developer standards causes. *Minimat Impact*k: Changes should only touch what's necessary. Avoid introducing new features or dependencies unless absolutely necessary.