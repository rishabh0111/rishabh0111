## Hi, I'm Rishabh

AI engineer in Gurugram. I ship LLM systems to production, along with the
backends and infrastructure under them, and I measure them before I trust
them. I trained in information security, so I ask how something breaks
before I ask when it ships.

**Now:** AI Engineer at Kleeto, where I've shipped 4 AI systems since May 2026:

- **HR assistant:** an AI agent across the HR platform for 500+ employees,
  grounded in 500,000 documents, with 85%+ eval-verified task completion
  and no successful prompt injection
- **Document verification:** GPT-4o checks on 5,500 onboarding documents a
  month, 82% accepted automatically; the model reads, code decides
- **TheMask:** masks government ID numbers before archiving, so a server
  breach reveals nothing (30,000 documents so far)
- **Kleeto AI Slides:** a real-time voice presenter that answers questions
  only from the company's own documents, piloting with 3 customers

That work is private. What follows is public, and every number in it can be
re-run from the repo.

### Projects

| Project | What it proves |
| --- | --- |
| **Nivara Desk** · [AI](https://github.com/rishabh0111/nivara-ai) · [API](https://github.com/rishabh0111/nivara-api-nestjs) · [Web](https://github.com/rishabh0111/nivara-web-nextjs) · [Live](https://nivara-web-nextjs.vercel.app/dashboard) | A multi-tenant AI helpdesk. The right call on 93.6% of 600 recorded tickets, 0 successful prompt injections in CI, and an eval harness that replays for $0. Python, TypeScript, Qdrant, Postgres row-level security |
| **[Nostro](https://github.com/rishabh0111/nostro-ledger)** | A double-entry ledger in Java 21 and Spring Boot where the database refuses unbalanced, duplicate and cross-tenant writes. 3 services over Kafka and gRPC, 211 tests on every push |
| **[LinkPulse](https://github.com/rishabh0111/linkpulse)** | A small app run like a production platform: Terraform, Kubernetes, ArgoCD, Prometheus. 12 hours on AWS EKS against real DynamoDB for $3.32, which found 13 defects no local run could |
| **[Webhook Delivery Engine](https://github.com/rishabh0111/webhook-delivery-engine)** · [Live](https://webhook-delivery-engine-on21.onrender.com/dashboard) | At-least-once delivery that lost 0 of 50,000 events through a Redis wipe mid-load, after its own benchmark found the bug that left 23,536 undelivered |

### Writing

I write up what I build, including what broke.
All posts are at **[rishabh0111.github.io/blogs](https://rishabh0111.github.io/blogs/)**:

- [A production-grade ledger in Java 21 where money can't go missing](https://rishabh0111.github.io/blogs/multitenant-double-entry-ledger/)
- [A DevOps platform built end to end, then broken on purpose on real AWS](https://rishabh0111.github.io/blogs/production-grade-devops-platform/)
- [Evals for an LLM agent](https://rishabh0111.github.io/blogs/evals-for-an-llm-agent/)
- [Postgres row-level security, and the leak a pooler builds](https://rishabh0111.github.io/blogs/postgres-rls-multitenancy/)
- A ten-part System Design series and a 19-part DSA series

### Stack

**AI:** LLM agents, RAG, MCP, LangGraph, evals, guardrails · Anthropic Claude, OpenAI, Gemini<br>
**Backend:** Python / FastAPI · TypeScript / Node.js / NestJS · Java / Spring Boot · Kafka · gRPC · Redis<br>
**Data:** PostgreSQL · MySQL · MongoDB · DynamoDB · Qdrant<br>
**Infrastructure:** AWS · Docker · Kubernetes · Terraform · ArgoCD · Prometheus · GitHub Actions<br>
**Security:** B.E. Information Security · CEH v11 · OWASP Top 10 for LLM Applications

### Contact

[Portfolio](https://rishabh0111.github.io/) · [LinkedIn](https://linkedin.com/in/rishabh0111) · [rishabhsharma8912@gmail.com](mailto:rishabhsharma8912@gmail.com)
