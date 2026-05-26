from __future__ import annotations

from cyrenebot.core.schema.skill import (
    SkillInstructionBundle,
    SkillSelection,
    SkillSelectionRequest,
)
from cyrenebot.core.skill.policy import build_skill_instruction_bundle
from cyrenebot.core.skill.selector import RuleBasedSkillSelector
from cyrenebot.core.skill.skill_protocol import (
    SkillRegistryProtocol,
    SkillSelectorProtocol,
)


class SkillManager:
    """
    技能管理器
    """

    def __init__(
        self,
        registry: SkillRegistryProtocol,
        selector: SkillSelectorProtocol | None = None,
    ) -> None:
        self._registry = registry
        self._selector = selector or RuleBasedSkillSelector()

    def select(self, request: SkillSelectionRequest) -> list[SkillSelection]:
        """
        选择技能
        """
        return self._selector.select(
            request,
            self._registry.list_definitions(),
        )

    def build_instruction_bundle(
        self,
        request: SkillSelectionRequest,
    ) -> SkillInstructionBundle:
        """
        构造技能提示词集合
        """
        return build_skill_instruction_bundle(self.select(request))
