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
    aasd_020 = auto()
    # aasd_021 = auto()
    # aasd_022 = auto()
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
    aasd_128 = auto()
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
    aasc_3a_010 = auto()
    # aasc_3c_050 = auto()

    @classmethod
    def from_string(cls, value: str) -> "IDTA | None":
        return cls.__members__.get(value)


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
    IDTA.standard.name: "IDTA # 1. 표준 검사",
    IDTA.optional.name: "IDTA # 2. 느슨한 표준 검사",
    IDTA.all_aasd.name: "IDTA # 3. Part 1. 제약조건 전체 검사",
    IDTA.aasd_002.name: "IDTA # 3-1. 제약조건 AASd-002 검사",
    IDTA.aasd_005.name: "IDTA # 3-2. 제약조건 AASd-005 검사",
    IDTA.aasd_006.name: "IDTA # 3-3. 제약조건 AASd-006 검사",
    IDTA.aasd_007.name: "IDTA # 3-4. 제약조건 AASd-007 검사",
    # IDTA.aasd_012.name: "IDTA # 3-5. 제약조건 AASd-012 검사",
    IDTA.aasd_014.name: "IDTA # 3-6. 제약조건 AASd-014 검사",
    IDTA.aasd_020.name: "IDTA # 3-7. 제약조건 AASd-020 검사",
    # IDTA.aasd_021.name: "IDTA # 3-8. 제약조건 AASd-021 검사",
    # IDTA.aasd_022.name: "IDTA # 3-9. 제약조건 AASd-022 검사",
    # IDTA.aasd_077.name: "IDTA # 3-10. 제약조건 AASd-077 검사",
    IDTA.aasd_090.name: "IDTA # 3-11. 제약조건 AASd-090 검사",
    IDTA.aasd_107.name: "IDTA # 3-12. 제약조건 AASd-107 검사",
    # IDTA.aasd_108.name: "IDTA # 3-13. 제약조건 AASd-108 검사",
    IDTA.aasd_109.name: "IDTA # 3-14. 제약조건 AASd-109 검사",
    IDTA.aasd_114.name: "IDTA # 3-15. 제약조건 AASd-114 검사",
    # IDTA.aasd_115.name: "IDTA # 3-16. 제약조건 AASd-115 검사",
    IDTA.aasd_116.name: "IDTA # 3-17. 제약조건 AASd-116 검사",
    IDTA.aasd_117.name: "IDTA # 3-18. 제약조건 AASd-117 검사",
    IDTA.aasd_118.name: "IDTA # 3-19. 제약조건 AASd-118 검사",
    IDTA.aasd_119.name: "IDTA # 3-20. 제약조건 AASd-119 검사",
    IDTA.aasd_120.name: "IDTA # 3-21. 제약조건 AASd-120 검사",
    IDTA.aasd_121.name: "IDTA # 3-22. 제약조건 AASd-121 검사",
    IDTA.aasd_122.name: "IDTA # 3-23. 제약조건 AASd-122 검사",
    IDTA.aasd_123.name: "IDTA # 3-24. 제약조건 AASd-123 검사",
    IDTA.aasd_124.name: "IDTA # 3-25. 제약조건 AASd-124 검사",
    IDTA.aasd_125.name: "IDTA # 3-26. 제약조건 AASd-125 검사",
    IDTA.aasd_126.name: "IDTA # 3-27. 제약조건 AASd-126 검사",
    IDTA.aasd_127.name: "IDTA # 3-28. 제약조건 AASd-127 검사",
    IDTA.aasd_128.name: "IDTA # 3-29. 제약조건 AASd-128 검사",
    IDTA.aasd_129.name: "IDTA # 3-30. 제약조건 AASd-129 검사",
    IDTA.aasd_130.name: "IDTA # 3-31. 제약조건 AASd-130 검사",
    IDTA.aasd_131.name: "IDTA # 3-32. 제약조건 AASd-131 검사",
    IDTA.aasd_133.name: "IDTA # 3-33. 제약조건 AASd-133 검사",
    IDTA.aasd_134.name: "IDTA # 3-34. 제약조건 AASd-134 검사",
    IDTA.all_aasc_3a.name: "IDTA # 4. Part 3. 제약조건 전체 검사",
    IDTA.aasc_3a_002.name: "IDTA # 4-1. 제약조건 AASc-3a-002 검사",
    # IDTA.aasc_3a_003.name: "IDTA # 4-2. 제약조건 AASc-3a-003 검사",
    IDTA.aasc_3a_004.name: "IDTA # 4-3. 제약조건 AASc-3a-004 검사",
    IDTA.aasc_3a_005.name: "IDTA # 4-4. 제약조건 AASc-3a-005 검사",
    IDTA.aasc_3a_006.name: "IDTA # 4-5. 제약조건 AASc-3a-006 검사",
    IDTA.aasc_3a_007.name: "IDTA # 4-6. 제약조건 AASc-3a-007 검사",
    IDTA.aasc_3a_008.name: "IDTA # 4-7. 제약조건 AASc-3a-008 검사",
    IDTA.aasc_3a_009.name: "IDTA # 4-8. 제약조건 AASc-3a-009 검사",
    IDTA.aasc_3a_010.name: "IDTA # 4-9. 제약조건 AASc-3a-010 검사",
    # IDTA.aasc_3c_050.name: "IDTA # 4-10. 제약조건 AASc-3c-050 검사",
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
