# External skills

Skills worth having that live in someone else's repo. They are not copied here:
install them from their source when a project needs them, so updates come from
upstream. See [README.md](README.md) for how `npx skills` works.

## Skill creator (Anthropic)

For writing, testing and tuning skills. Used to build the ones in this repo.

```bash
# Claude Code: the official plugin
claude plugin install skill-creator@claude-plugins-official

# Any other agent
npx skills add anthropics/skills -s skill-creator
```

## Azure and Entra (Microsoft)

Source: [`microsoft/azure-skills`](https://github.com/microsoft/azure-skills) (`skills/<name>`).
Install per project, not globally — there are 28, and their descriptions would
crowd every session in every agent.

```bash
npx skills add microsoft/azure-skills -s azure-prepare -s azure-validate -s azure-deploy
npx skills add microsoft/azure-skills --list    # see what's there
```

| Skill | What it's for |
|---|---|
| `azure-app-onboard` | End-to-end: from an idea or existing app to a running Azure deployment with cost estimates |
| `azure-app-onboard-prereq` | Is this code ready to deploy to Azure? (before any infra work) |
| `azure-prepare` | Generate `azure.yaml`, Bicep/Terraform and Dockerfiles for `azd` |
| `azure-validate` | Pre-deployment validation |
| `azure-deploy` | Run `azd up` / deploy for an already-prepared app |
| `python-appservice-deploy` | Deploy Flask/Django/FastAPI to App Service Linux |
| `azure-enterprise-infra-planner` | Architect and provision enterprise infrastructure from a workload description |
| `azure-kubernetes` | Plan and create production AKS clusters |
| `airunway-aks-setup` | AI Runway on AKS, from bare cluster to a served model |
| `azure-compute` | VM / VMSS |
| `azure-storage` | Blob, Files, Queue, Table, Data Lake |
| `azure-messaging` | Troubleshoot Event Hubs / Service Bus SDKs |
| `azure-kusto` | KQL against Azure Data Explorer |
| `azure-ai` | AI Search, Speech, OpenAI, Document Intelligence |
| `azure-aigateway` | API Management as an AI gateway for models, MCP tools and agents |
| `microsoft-foundry` | Build, deploy, evaluate and fine-tune Foundry agents and models |
| `appinsights-instrumentation` | Instrument web apps with Application Insights |
| `azure-diagnostics` | Debug production issues (AppLens, Monitor, resource health) |
| `azure-reliability` | Reliability posture of Functions / App Service |
| `azure-compliance` | Compliance and security audits (azqr, Key Vault expiry) |
| `azure-cost` | Query, forecast and reduce costs |
| `azure-quotas` | Quotas and usage |
| `azure-upgrade` | Move between plans/tiers/SKUs, or modernize Azure SDK use |
| `azure-cloud-migrate` | Assess and migrate workloads from other clouds |
| `azure-resource-lookup` | Find resources across subscriptions and groups |
| `azure-resource-visualizer` | Mermaid architecture diagrams of a resource group |
| `entra-app-registration` | App registrations, OAuth 2.0, MSAL |
| `entra-agent-id` | Entra Agent Identity blueprints and per-instance identities |
