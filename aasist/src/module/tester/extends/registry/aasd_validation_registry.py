from aasist.src.gui.handler import LogLevel
from aasist.src.module.tester.constants import CHECKLIST, IDTA
from aasist.src.module.tester.extends.context.aasd_validation_context import (
    AasdValidationContext,
)
from aasist.src.module.tester.extends.registry.validation_registry import (
    ValidationRegistry,
)


class AasdValidationRegistry(ValidationRegistry):
    def __init__(self, context: AasdValidationContext):
        super().__init__()
        self.context = context
        self.results = {}

    @ValidationRegistry.validator(IDTA.aasd_002.name)
    async def _aasd_002(self, rule: str = IDTA.aasd_002.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.parents_store.get("Referable", []),
            "check_constraints_aasd_002",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_005.name)
    async def _aasd_005(self, rule: str = IDTA.aasd_005.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("AdministrativeInformation", []),
            "check_constraint_aasd_005",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_006.name)
    async def _aasd_006(self, rule: str = IDTA.aasd_006.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("Qualifier", []),
            "check_aasd_006",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_007.name)
    async def _aasd_007(self, rule: str = IDTA.aasd_007.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("Property", []),
            "check_aasd_007",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_014.name)
    async def _aasd_014(self, rule: str = IDTA.aasd_014.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("Entity", []),
            "check_aasd_014",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_020.name)
    async def _aasd_020(self, rule: str = IDTA.aasd_020.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("Qualifier", []),
            "check_aasd_020",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_090.name)
    async def _aasd_090(self, rule: str = IDTA.aasd_090.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.parents_store.get("DataElement", []),
            "check_aasd_090",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_107.name)
    async def _aasd_107(self, rule: str = IDTA.aasd_107.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("SubmodelElementList", []),
            "check_aasd_107",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_109.name)
    async def _aasd_109(self, rule: str = IDTA.aasd_109.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("SubmodelElementList", []),
            "check_aasd_109",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_114.name)
    async def _aasd_114(self, rule: str = IDTA.aasd_114.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("SubmodelElementList", []),
            "check_aasd_114",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_116.name)
    async def _aasd_116(self, rule: str = IDTA.aasd_116.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("AssetInformation", []),
            "check_aasd_116",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_117.name)
    async def _aasd_117(self, rule: str = IDTA.aasd_117.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.parents_store.get("AnnotatedRelationshipElement", []),
            "check_aasd_117",
            rule,
        )
        await self.check_rule_with_logging(
            self.context.constraints_store.get("OperationVariable", []),
            "check_aasd_117",
            rule,
        )
        await self.check_rule_with_logging(
            self.context.constraints_store.get("SubmodelElementCollection", []),
            "check_aasd_117",
            rule,
        )
        await self.check_rule_with_logging(
            self.context.constraints_store.get("Submodel", []),
            "check_aasd_117",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_118.name)
    async def _aasd_118(self, rule: str = IDTA.aasd_118.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.parents_store.get("HasSemantics", []),
            "check_aasd_118",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_119.name)
    async def _aasd_119(self, rule: str = IDTA.aasd_119.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("Submodel", []),
            "check_aasd119",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_120.name)
    async def _aasd_120(self, rule: str = IDTA.aasd_120.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("SubmodelElementList", []),
            "check_aasd_120",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_121.name)
    async def _aasd_121(self, rule: str = IDTA.aasd_121.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("Reference", []),
            "check_aasd_121",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_122.name)
    async def _aasd_122(self, rule: str = IDTA.aasd_122.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("Reference", []),
            "check_aasd_122",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_123.name)
    async def _aasd_123(self, rule: str = IDTA.aasd_123.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("Reference", []),
            "check_aasd_123",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_124.name)
    async def _aasd_124(self, rule: str = IDTA.aasd_124.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("Reference", []),
            "check_aasd_124",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_125.name)
    async def _aasd_125(self, rule: str = IDTA.aasd_125.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("Reference", []),
            "check_aasd_125",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_126.name)
    async def _aasd_126(self, rule: str = IDTA.aasd_126.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("Reference", []),
            "check_aasd_126",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_127.name)
    async def _aasd_127(self, rule: str = IDTA.aasd_127.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("Reference", []),
            "check_aasd_127",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_128.name)
    async def _aasd_128(self, rule: str = IDTA.aasd_128.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("Reference", []),
            "check_aasd_128",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_129.name)
    async def _aasd_129(self, rule: str = IDTA.aasd_129.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("Submodel", []),
            "check_aasd_129",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_130.name)
    async def _aasd_130(self, rule: str = IDTA.aasd_130.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("StringFormattedValue", []),
            "__init__",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_131.name)
    async def _aasd_131(self, rule: str = IDTA.aasd_131.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("AssetInformation", []),
            "check_aasd_131",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_133.name)
    async def _aasd_133(self, rule: str = IDTA.aasd_133.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("SpecificAssetId", []),
            "check_aasd_133",
            rule,
        )

    @ValidationRegistry.validator(IDTA.aasd_134.name)
    async def _aasd_134(self, rule: str = IDTA.aasd_134.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self.check_rule_with_logging(
            self.context.constraints_store.get("Operation", []),
            "check_aasd_134",
            rule,
        )
