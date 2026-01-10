from core.types import ISDK
from util.utils import create_logger_with_prefix
from ...constants.appId import APP_VERSION
from ...proto.generated.manager import GetDeviceInfoResultResponse
from ...utils import assert_or_throw_invalid_result, OperationHelper
from ...utils import logger as rootlogger

logger = create_logger_with_prefix(rootlogger, "GetDeviceInfo")


async def get_device_info(sdk: ISDK) -> GetDeviceInfoResultResponse:
    logger.info("Started")
    await sdk.check_app_compatibility(APP_VERSION)
    print("check_app_compatibility completed########################")
    helper = OperationHelper(sdk, "get_device_info", "get_device_info")
    print("helper created########################")
    await helper.send_query({"initiate": {}})
    print("send_query completed########################")
    result = await helper.wait_for_result()
    print("wait_for_result completed########################")
    logger.verbose("GetDeviceInfoResponse", {"result": result})
    assert_or_throw_invalid_result(result.result)
    print("assert_or_throw_invalid_result completed########################")
    logger.info("Completed")
    print("Completed########################")
    return result.result
