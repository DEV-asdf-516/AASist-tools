from aasist.src.gui.handler import LogLevel
from aasist.src.module.tester.constants import CHECKLIST, IDTA
from aasist.src.module.tester.extends.context.aasc_3a_validation_context import (
    Aasc3aValidationContext,
)
from aasist.src.module.tester.extends.registry.validation_registry import (
    ValidationRegistry,
)


class Aasc3aValidationRegistry(ValidationRegistry):
    def __init__(self, context: Aasc3aValidationContext):
        super().__init__()
        self.context = context
        self.results: dict[str, bool] = {}

    @ValidationRegistry.validator(IDTA.aasc_3a_002.name)
    async def _aasc_3a_002(self, rule: str = IDTA.aasc_3a_002.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store["DataSpecificationIec61360"],
            "check_aasc_3a_002",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasc_3a_009.name)
    async def _aasc_3a_009(self, rule: str = IDTA.aasc_3a_009.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store["DataSpecificationIec61360"],
            "check_aasc_3a_009",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasc_3a_010.name)
    async def _aasc_3a_010(self, rule: str = IDTA.aasc_3a_010.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store["DataSpecificationIec61360"],
            "check_aasc_3a_010",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasc_3a_004.name)
    async def _aasc_3a_004(self, rule: str = IDTA.aasc_3a_004.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store["ConceptDescription"],
            "check_aasc_3a_004",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasc_3a_005.name)
    async def _aasc_3a_005(self, rule: str = IDTA.aasc_3a_005.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store["ConceptDescription"],
            "check_aasc_3a_005",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasc_3a_006.name)
    async def _aasc_3a_006(self, rule: str = IDTA.aasc_3a_006.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store["ConceptDescription"],
            "check_aasc_3a_006",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasc_3a_007.name)
    async def _aasc_3a_007(self, rule: str = IDTA.aasc_3a_007.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store["ConceptDescription"],
            "check_aasc_3a_007",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasc_3a_008.name)
    async def _aasc_3a_008(self, rule: str = IDTA.aasc_3a_008.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store["ConceptDescription"],
            "check_aasc_3a_008",
            rule,
        )
