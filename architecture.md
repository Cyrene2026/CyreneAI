'''mermaid
flowchart TB
%% =====================
%% Application
%% =====================
subgraph APP["application"]
app_boot["application/bootstrap"]
app_runtime["application/runtime"]
app_chat["application/chat_orchestrator"]
end

%% =====================
%% Core
%% =====================
subgraph CORE["core"]
subgraph CORE_SCHEMA["core/schema"]
schema_chat["schema/chat"]
schema_context["schema/context"]
schema_message["schema/message"]
schema_provider["schema/provider"]
schema_skill["schema/skill"]
schema_tool["schema/tool"]
end

    subgraph CORE_ERRORS["core/errors"]
      errors_base["errors/base"]
      errors_context["errors/context"]
      errors_provider["errors/provider"]
      errors_skill["errors/skill"]
      errors_tool["errors/tool"]
    end

    subgraph CORE_CONTEXT["core/context"]
      context_protocol["context/protocol"]
      context_policy["context/policy"]
      context_builder["context/builder"]
      context_manager["context/manager"]
    end

    subgraph CORE_PROVIDER["core/provider"]
      provider_protocol["provider/protocol"]
      provider_factory["provider/factory"]
      provider_registry["provider/registry"]
      provider_manager["provider/manager"]
    end

    subgraph CORE_TOOL["core/tool"]
      tool_protocol["tool/protocol"]
      tool_registry["tool/registry"]
      tool_manager["tool/manager"]
    end

    subgraph CORE_SKILL["core/skill"]
      skill_protocol["skill/protocol"]
      skill_policy["skill/policy"]
      skill_selector["skill/selector"]
      skill_registry["skill/registry"]
      skill_manager["skill/manager"]
    end

end

%% =====================
%% Infra
%% =====================
subgraph INFRA["infra"]
provider_catalog["provider_catalog"]

    subgraph INFRA_BOOT["infra/bootstrap"]
      provider_regs["bootstrap/registrations/providers"]
    end

    subgraph PROVIDER_ADAPTERS["infra/adapters/providers"]
      openai_compat["openai_compatible"]
      openai_resp["openai_responses"]
      anthropic["anthropic"]
      google_genai["google_genai"]
    end

    subgraph TOOL_ADAPTERS["infra/adapters/tools"]
      tools_common["tools/common"]
      tool_python["python_callable"]
      tool_http["http"]
      tool_subprocess["subprocess"]
    end

    subgraph SKILL_ADAPTERS["infra/adapters/skills"]
      skill_fs["filesystem"]
    end

    subgraph DATABASE["infra/database"]
      db_sqlalchemy["database/sqlalchemy"]
      db_sqlite["database/sqlite"]
    end

end

%% =====================
%% Application edges
%% =====================
app_boot --> app_runtime
app_boot --> provider_factory
app_boot --> provider_registry
app_boot --> provider_manager
app_boot --> context_builder
app_boot --> context_manager
app_boot --> context_protocol
app_boot --> skill_registry
app_boot --> skill_manager
app_boot --> tool_registry
app_boot --> tool_manager
app_boot --> tool_protocol
app_boot --> schema_provider
app_boot --> provider_regs
app_boot --> skill_fs
app_boot --> db_sqlite

app_runtime --> provider_manager
app_runtime --> context_manager
app_runtime --> context_protocol
app_runtime --> skill_manager
app_runtime --> tool_manager
app_runtime --> tool_protocol

app_chat --> app_runtime
app_chat --> context_protocol
app_chat --> provider_protocol
app_chat --> errors_base
app_chat --> schema_chat
app_chat --> schema_context
app_chat --> schema_message
app_chat --> schema_skill
app_chat --> schema_tool

%% =====================
%% Core schema edges
%% =====================
schema_chat --> schema_message
schema_chat --> schema_tool
schema_context --> schema_message

%% =====================
%% Core errors edges
%% =====================
errors_context --> errors_base
errors_provider --> errors_base
errors_skill --> errors_base
errors_tool --> errors_base

%% =====================
%% Core context edges
%% =====================
context_protocol --> schema_context
context_protocol --> schema_message
context_policy --> errors_context
context_policy --> schema_context
context_builder --> context_protocol
context_builder --> context_policy
context_builder --> schema_context
context_builder --> schema_message
context_manager --> context_protocol
context_manager --> schema_context

%% =====================
%% Core provider edges
%% =====================
provider_protocol --> schema_chat
provider_protocol --> schema_provider
provider_factory --> provider_protocol
provider_factory --> schema_provider
provider_factory --> errors_base
provider_factory --> errors_provider
provider_registry --> schema_provider
provider_registry --> errors_base
provider_registry --> errors_provider
provider_manager --> provider_protocol
provider_manager --> schema_provider
provider_manager --> errors_base

%% =====================
%% Core tool edges
%% =====================
tool_protocol --> schema_tool
tool_registry --> tool_protocol
tool_registry --> schema_tool
tool_registry --> errors_base
tool_registry --> errors_tool
tool_manager --> tool_protocol
tool_manager --> schema_tool

%% =====================
%% Core skill edges
%% =====================
skill_protocol --> schema_skill
skill_policy --> schema_skill
skill_selector --> skill_policy
skill_selector --> schema_skill
skill_registry --> schema_skill
skill_registry --> errors_base
skill_registry --> errors_skill
skill_manager --> skill_protocol
skill_manager --> skill_policy
skill_manager --> skill_selector
skill_manager --> schema_skill

%% =====================
%% Provider adapters
%% =====================
openai_compat --> provider_protocol
openai_compat --> errors_provider
openai_compat --> schema_chat
openai_compat --> schema_message
openai_compat --> schema_provider
openai_compat --> schema_tool

openai_resp --> provider_protocol
openai_resp --> errors_provider
openai_resp --> schema_chat
openai_resp --> schema_message
openai_resp --> schema_provider
openai_resp --> schema_tool
openai_resp -.shared reuse.-> openai_compat

anthropic --> provider_protocol
anthropic --> errors_provider
anthropic --> schema_chat
anthropic --> schema_message
anthropic --> schema_provider
anthropic --> schema_tool

google_genai --> provider_protocol
google_genai --> errors_provider
google_genai --> schema_chat
google_genai --> schema_message
google_genai --> schema_provider
google_genai --> schema_tool

%% =====================
%% Tool adapters
%% =====================
tools_common --> errors_tool
tools_common --> schema_tool
tool_python --> tools_common
tool_python --> errors_tool
tool_python --> schema_tool
tool_http --> tools_common
tool_http --> errors_tool
tool_http --> schema_tool
tool_subprocess --> tools_common
tool_subprocess --> errors_tool
tool_subprocess --> schema_tool

%% =====================
%% Skill adapters
%% =====================
skill_fs --> errors_skill
skill_fs --> schema_skill

%% =====================
%% Database
%% =====================
db_sqlite --> db_sqlalchemy
db_sqlalchemy --> context_protocol
db_sqlalchemy --> errors_context
db_sqlalchemy --> schema_context

%% =====================
%% Bootstrap / catalog
%% =====================
provider_regs --> provider_factory
provider_regs --> provider_registry
provider_regs --> provider_protocol
provider_regs --> schema_provider
provider_regs --> provider_catalog
provider_regs --> openai_compat
provider_regs --> openai_resp
provider_regs --> anthropic
provider_regs --> google_genai

provider_catalog --> schema_provider

%% =====================
%% Styling
%% =====================
classDef app fill:#e8f1ff,stroke:#3267c8,color:#111;
classDef core fill:#eef9f0,stroke:#2f8f46,color:#111;
classDef infra fill:#fff4e6,stroke:#d18419,color:#111;
classDef note fill:#f7f7f7,stroke:#999,color:#111;

class app_boot,app_runtime,app_chat app;
class schema_chat,schema_context,schema_message,schema_provider,schema_skill,schema_tool,errors_base,errors_context,errors_provider,errors_skill,errors_tool,context_protocol,context_policy,context_builder,context_manager,provider_protocol,provider_factory,provider_registry,provider_manager,tool_protocol,tool_registry,tool_manager,skill_protocol,skill_policy,skill_selector,skill_registry,skill_manager core;
class provider_catalog,provider_regs,openai_compat,openai_resp,anthropic,google_genai,tools_common,tool_python,tool_http,tool_subprocess,skill_fs,db_sqlalchemy,db_sqlite infra;
'''
