from ..hub import ModelType, NetworkType, must_exists

LCM_SCHEDULER_LIST = {
    NetworkType.SD_1_5: [
        must_exists("LCM", NetworkType.SD_1_5, ModelType.Lora),
    ],
    NetworkType.SDXL_1_0: [
        must_exists("LCM", NetworkType.SDXL_1_0, ModelType.Lora),
    ]
}
