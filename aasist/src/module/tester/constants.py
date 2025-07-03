from enum import Enum, auto


class IDTA(Enum):
    standard = auto()
    optional = auto()
    all_aasd = auto()
    all_aasc_3a = auto()
    aasd_002 = auto()
    aasd_005 = auto()
    aasd_006 = auto()
    aasd_007 = auto()
    # aasd_012 = auto()
    aasd_014 = auto()
    # aasd_020 = auto()
    # aasd_021 = auto()
    aasd_022 = auto()
    # aasd_077 = auto()
    aasd_090 = auto()
    aasd_107 = auto()
    # aasd_108 = auto()
    aasd_109 = auto()
    aasd_114 = auto()
    # aasd_115 = auto()
    aasd_116 = auto()
    aasd_117 = auto()
    aasd_118 = auto()
    aasd_119 = auto()
    aasd_120 = auto()
    aasd_121 = auto()
    aasd_122 = auto()
    aasd_123 = auto()
    aasd_124 = auto()
    aasd_125 = auto()
    aasd_126 = auto()
    aasd_127 = auto()
    aasd_129 = auto()
    aasd_130 = auto()
    aasd_131 = auto()
    aasd_133 = auto()
    aasd_134 = auto()
    aasc_3a_002 = auto()
    # aasc_3a_003 = auto()
    aasc_3a_004 = auto()
    aasc_3a_005 = auto()
    aasc_3a_006 = auto()
    aasc_3a_007 = auto()
    aasc_3a_008 = auto()
    aasc_3a_009 = auto()
    aasc_3c_010 = auto()
    # aasc_3c_050 = auto()


class KOSMO(Enum):
    aas_thumbnail = auto()
    aas_id_short = auto()
    aas_id = auto()
    aas_submodel = auto()
    aas_global_asset_id = auto()
    aas_type = auto()
    submodel_id_short = auto()
    submodel_id = auto()
    submodel_semantic_id = auto()
    submodel_kind = auto()
    smc_id_short = auto()
    smc_cd_mapping = auto()
    prop_id_short = auto()
    prop_cd_mapping = auto()
    prop_value = auto()
    cd_id_short = auto()
    cd_id = auto()
    cd_definition = auto()


CHECKLIST = {
    IDTA.standard: "IDTA # 1. 표준 검사",
    IDTA.optional: "IDTA # 2. 느슨한 표준 검사",
    KOSMO.aas_thumbnail.name: "KOSMO-AAS # 1. Thumbnail 이미지 확인",
    KOSMO.aas_id_short.name: "KOSMO-AAS # 2. idShort 설정/명명 규칙 검사",
    KOSMO.aas_id.name: "KOSMO-AAS # 3. Id 형식 검사",
    KOSMO.aas_submodel.name: "KOSMO-AAS # 4. Submodel 구성 검사",
    KOSMO.aas_global_asset_id.name: "KOSMO-AAS # 5. globalAssetId 검사",
    KOSMO.aas_type.name: "KOSMO-AAS # 6. Type 유형 검사",
    KOSMO.submodel_id_short.name: "KOSMO-Submodel # 1. idShort 설정/명명 규칙 검사",
    KOSMO.submodel_id.name: "KOSMO-Submodel # 2. Id 형식 검사",
    KOSMO.submodel_semantic_id.name: "KOSMO-Submodel # 3. semanticId 설정/명명 규칙 검사",
    KOSMO.submodel_kind.name: "KOSMO-Submodel # 4. Kind 유형 검사",
    KOSMO.smc_id_short.name: "KOSMO-SMC # 1. idShort 설정/명명 규칙 검사",
    KOSMO.smc_cd_mapping.name: "KOSMO-SMC # 2. ConceptDescription mapping 확인",
    KOSMO.prop_value.name: "KOSMO-Property # 1. Value 값 존재 여부 확인",
    KOSMO.prop_id_short.name: "KOSMO-Property # 2. idShort 설정/명명 규칙 검사",
    KOSMO.prop_cd_mapping.name: "KOSMO-Property # 3. ConceptDescription mapping 확인",
    KOSMO.cd_id.name: "KOSMO-CD # 1. Id 형식 검사",
    KOSMO.cd_id_short.name: "KOSMO-CD # 2. idShort 설정/명명 규칙 검사",
    KOSMO.cd_definition.name: "KOSMO-CD # 3. definition 설정 검사",
}

IRDI = r"^(?:\d{4}-\d+#\d{2}-[A-Z]{3}\d{3}#\d{3}(?:/\d{4}-\d+#\d{2}-[A-Z]{3}\d{3}#\d{3}\*\d+(?:---[A-F0-9]{8})?)?|\d{4}/\d+///\d+(?:_\d+)?#[A-Z]{3}\d{3}#\d{3})$"
EXTENSION_IRI = r"^https?://[a-zA-Z0-9.-]+/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+/\d+/\d+(?:/[a-zA-Z0-9_-]+)*/?$"
