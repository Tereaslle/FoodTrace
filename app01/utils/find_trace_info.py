from app01 import models


def find_trace_info(msg):
    food_info_queryset = models.MaterialInfo.objects.filter(product_batch=msg).all()
    trace_info_dict = {}
    index = 1
    if food_info_queryset:
        for obj in food_info_queryset:
            singlefood_queryset = models.FlowRecord.objects.filter(batchID=obj.material_batch.batchID).all()
            for obj_flowrecord in singlefood_queryset:
                dict = {}
                dict['flowID'] = obj_flowrecord.flowID
                dict['foodID'] = obj_flowrecord.foodID.foodID
                dict['food_name'] = obj_flowrecord.foodID.name
                dict['batchID'] = obj_flowrecord.batchID.batchID
                dict['quality'] = obj_flowrecord.batchID.quality
                dict['userID'] = obj_flowrecord.userID.userID
                dict['user_name'] = obj_flowrecord.userID.name
                dict['user_enterprise'] = obj_flowrecord.userID.enterpriseID.name
                dict['deviceID'] = obj_flowrecord.deviceID.deviceID
                dict['device_name'] = obj_flowrecord.deviceID.name
                dict['target_enterpriseID'] = obj_flowrecord.enterpriseID.enterpriseID
                dict['target_enterprise_name'] = obj_flowrecord.enterpriseID.name
                dict['record_datetime'] = obj_flowrecord.record_datetime.strftime('%Y-%m-%d %H:%M:%S')
                # print(dict)
                trace_info_dict[str(index)] = dict
                index += 1
            # print(obj.material.name)
            # print(obj.material_batch.batchID)
            # print(obj.material.__dict__)
    # 最后找到本产品的溯源信息
    singlefood_queryset = models.FlowRecord.objects.filter(batchID=msg).all()
    if singlefood_queryset:
        for obj_flowrecord in singlefood_queryset:
            dict = {}
            dict['flowID'] = obj_flowrecord.flowID
            dict['foodID'] = obj_flowrecord.foodID.foodID
            dict['food_name'] = obj_flowrecord.foodID.name
            dict['batchID'] = obj_flowrecord.batchID.batchID
            dict['quality'] = obj_flowrecord.batchID.quality
            dict['userID'] = obj_flowrecord.userID.userID
            dict['user_name'] = obj_flowrecord.userID.name
            dict['user_enterprise'] = obj_flowrecord.userID.enterpriseID.name
            dict['deviceID'] = obj_flowrecord.deviceID.deviceID
            dict['device_name'] = obj_flowrecord.deviceID.name
            dict['target_enterpriseID'] = obj_flowrecord.enterpriseID.enterpriseID
            dict['target_enterprise_name'] = obj_flowrecord.enterpriseID.name
            dict['record_datetime'] = obj_flowrecord.record_datetime.strftime('%Y-%m-%d %H:%M:%S')
            trace_info_dict[str(index)] = dict
            index += 1
    return trace_info_dict
