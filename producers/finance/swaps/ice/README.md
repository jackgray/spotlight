# ICE Swap Data Repository (SDR) Pipeline


## Notes on this pipeline


Spark is indentionally avoided for the sourcing aspect of this pipeline as it is not as performant as asyncio when making network based requests. 