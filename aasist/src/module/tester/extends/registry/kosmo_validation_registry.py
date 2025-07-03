import asyncio
import re
from typing import Dict, List, Union
from aasist.src.gui.handler import _TEST_LOG_NAME, LogLevel, QueueHandler
from aasist.src.module.tester.extends.context.kosmo_validation_context import (
    KosmoValidationContext,
)
from aasist.src.module.tester.extends.registry.validation_registry import (
    ValidationRegistry,
)
from aasist.src.module.tester.constants import EXTENSION_IRI, IRDI, KOSMO, CHECKLIST
from aas_test_engines.reflect import TypeBase


class KosmoValidationRegistry(ValidationRegistry):
    def __init__(
        self,
        context: KosmoValidationContext,
    ):
        self.context = context
        self.results: Dict[str, bool] = {}
        self.log_handler = QueueHandler(_TEST_LOG_NAME)

    def get_validator(self, name: str):
        return ValidationRegistry.get_validator(name)

    # id 규칙
    async def _id_rule(self, rule: str, constructs: List[TypeBase]):
        from aas_test_engines.data_types import is_any_uri

        self.results[rule] = True
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        for construct in constructs:
            if not hasattr(construct, "id"):
                continue
            id = getattr(construct, "id")
            if not hasattr(id, "raw_value"):
                continue
            is_irdi = re.compile(IRDI).match(id.raw_value)
            if is_irdi:
                continue
            is_iri = is_any_uri(id.raw_value)
            if not is_iri:
                if re.compile(EXTENSION_IRI).match(id.raw_value):
                    continue
                self.log_handler.add(
                    f"""The Id "{construct.id}" violates the Kosmo rules: {construct.__class__.__name__}의 ID {id.raw_value}가 IRI 형식을 준수하지 않습니다.\n\r- 형식이 올바른 경우, 잘못된 공백이 포함되어 있을 수도 있습니다.""",
                    LogLevel.ERROR,
                )
                await asyncio.sleep(0.1)
                self.results[rule] = False

    @ValidationRegistry.validator(KOSMO.aas_id.name)
    async def _aas_id_rule(self, rule: str = KOSMO.aas_id.name):
        await self._id_rule(
            rule, self.context.identifiables["AssetAdministrationShell"]
        )

    @ValidationRegistry.validator(KOSMO.submodel_id.name)
    async def _submodel_id_rule(self, rule: str = KOSMO.submodel_id.name):
        await self._id_rule(rule, self.context.identifiables["Submodel"])

    @ValidationRegistry.validator(KOSMO.cd_id.name)
    async def _smc_id_rule(self, rule: str = KOSMO.cd_id.name):
        await self._id_rule(rule, self.context.identifiables["ConceptDescription"])

    # id short 규칙
    async def _id_short_rule(self, rule: str, constructs: List[TypeBase]):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self._check_kosmo_rule_with_logging(constructs, "check_aasd_117", rule)
        await self._check_kosmo_rule_with_logging(
            constructs, "check_constraint_aasd_002", rule
        )

    @ValidationRegistry.validator(KOSMO.aas_id_short.name)
    async def _aas_id_short_rule(self, rule: str = KOSMO.aas_id_short.name):
        await self._id_short_rule(
            rule, self.context.referables["AssetAdministrationShell"]
        )

    @ValidationRegistry.validator(KOSMO.submodel_id_short.name)
    async def _submodel_id_short_rule(self, rule: str = KOSMO.submodel_id_short.name):
        await self._id_short_rule(rule, self.context.referables["Submodel"])

    @ValidationRegistry.validator(KOSMO.smc_id_short.name)
    async def _smc_id_short_rule(self, rule: str = KOSMO.smc_id_short.name):
        await self._id_short_rule(
            rule, self.context.referables["SubmodelElementCollection"]
        )

    @ValidationRegistry.validator(KOSMO.prop_id_short.name)
    async def _prop_id_short_rule(self, rule: str = KOSMO.prop_id_short.name):
        await self._id_short_rule(rule, self.context.referables["Property"])

    @ValidationRegistry.validator(KOSMO.cd_id_short.name)
    async def _cd_id_short_rule(self, rule: str = KOSMO.cd_id_short.name):
        await self._id_short_rule(rule, self.context.referables["ConceptDescription"])

    @ValidationRegistry.validator(KOSMO.aas_submodel.name)
    async def _submodel_component_rule(self, rule: str = KOSMO.aas_submodel.name):
        require_components = [
            "Identification",
            "TechnicalData",
            "Documentation",
            "OperationalData",
        ]
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        id_shorts = [
            ref.id_short.raw_value for ref in self.context.referables["Submodel"]
        ]
        all_included = set(require_components).issubset(set(id_shorts))
        self.results[rule] = all_included
        if not all_included:
            missing = set(require_components) - set(id_shorts)
            self.log_handler.add(
                f"""The Submodel violates the Kosmo rules:\n\r- 필수 서브모델 {', '.join(missing)}이(가) 누락되었습니다.""",
                LogLevel.ERROR,
            )
            await asyncio.sleep(0.1)
            self.results[rule] = False

    @ValidationRegistry.validator(KOSMO.aas_global_asset_id.name)
    async def _global_asset_id_rule(self, rule: str = KOSMO.aas_global_asset_id.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self._check_kosmo_rule_with_logging(
            self.context.asset_informations,
            "check_aasd_131",
            rule,
        )

    @ValidationRegistry.validator(KOSMO.aas_type.name)
    async def _type_rule(self, rule: str = KOSMO.aas_type.name):
        from aas_test_engines.test_cases.v3_0.model import AssetKind

        self.results[rule] = True
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        for info in self.context.asset_informations:
            if not hasattr(info, "asset_kind"):
                continue
            if info.asset_kind != AssetKind.TYPE:
                self.log_handler.add(
                    f"""The Kind "{info.asset_kind.value}" violates the Kosmo rules: Kind가 Type으로 지정되어야 합니다.""",
                    LogLevel.ERROR,
                )
                await asyncio.sleep(0.1)
                self.results[rule] = False

    @ValidationRegistry.validator(KOSMO.submodel_kind.name)
    async def _kind_rule(self, rule: str = KOSMO.submodel_kind.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self._check_kosmo_rule_with_logging(
            self.context.referables["Submodel"], "check_aasd_129", rule
        )

    @ValidationRegistry.validator(KOSMO.prop_value.name)
    async def _value_rule(self, rule: str = KOSMO.prop_value.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        # TODO

    @ValidationRegistry.validator(KOSMO.cd_definition.name)
    async def _definition_rule(self, rule: str = KOSMO.cd_definition.name):
        self.log_handler.add(f"{CHECKLIST[rule]}", LogLevel.INFO)
        await self._check_kosmo_rule_with_logging(
            self.context.referables["ConceptDescription"],
            "check_aasc_3a_008",
            rule,
        )

    async def _check_kosmo_rule_with_logging(
        self, objects: List[TypeBase], method_name: Union[str, List[str]], rule: KOSMO
    ):
        self.results[rule] = self.results.get(rule, True)
        for obj in objects:
            if hasattr(obj, method_name) is False:
                continue
            message = getattr(obj, method_name)()
            if not message:
                continue
            self.log_handler.add(
                message,
                log_level=LogLevel.ERROR,
            )
            await asyncio.sleep(0.1)
            self.results[rule] = False
