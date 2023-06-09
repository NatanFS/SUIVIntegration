from api.models import Equipment, FipeData, Part, PriceHistory, RevisionPlan, SUIVRequest, SuivData, TechnicalSpecsGroup, Vehicle, SummaryVehicle
from api.serializers import FipeDataSerializer, PartSerializer, SuivDataSerializer, VehicleSerializer


def generate_vehicle_info_json(vehicle):
    # Serializa dados em JSON
    vehicle_data = VehicleSerializer(vehicle).data
    fipe_data_collection = FipeDataSerializer(
        vehicle.fipe_data.all(), many=True).data
    suiv_data_collection = SuivDataSerializer(
        vehicle.suiv_data.all(), many=True).data

    data = {
        **vehicle_data,
        "fipeDataCollection": fipe_data_collection,
        "suivDataCollection": suiv_data_collection,
    }

    return data


def generate_basic_pack_info(parts):
    return PartSerializer(parts, many=True).data


def register_suiv_request(endpoint, inputs):
    SUIVRequest.objects.create(endpoint=endpoint, inputs=inputs)


def save_summary_data_object(summary, fipe_id):
    fd_kwargs = {
        'fipe_id': fipe_id,
        'text': summary['text'],
        'image_url': summary['imageUrl'],
        'maker_logo_url': summary['makerLogoUrl'],
    }
    return SummaryVehicle.objects.create(**fd_kwargs)


def save_technical_specs_groups(technical_specs_groups, plate):
    technical_specs_groups_objects = []
    for technical_specs_group in technical_specs_groups:
        fd_kwargs = {
            'plate': plate,
            'description': technical_specs_group['description'],
            'specs': technical_specs_group['specs'],
        }
        technical_specs_groups_objects.append(TechnicalSpecsGroup(**fd_kwargs))
    return TechnicalSpecsGroup.objects.bulk_create(technical_specs_groups_objects)

def save_revision_plans(revision_plans, version_id, year):
    revision_plans_objects = []
    for revision_plan in revision_plans:
        fd_kwargs = {
            'version_id': version_id,
            'year': year,
            'kilometers': revision_plan['kilometers'],
            'months': revision_plan['months'],
            'parcels': revision_plan['parcels'],
            'duration_minutes': revision_plan['durationMinutes'],
            'full_price': revision_plan['fullPrice'],
            'parcel_price': revision_plan['parcelPrice'],
            'changed_parts': revision_plan['changedParts'],
            'inspections': revision_plan['inspections'],
        }
        revision_plans_objects.append(RevisionPlan(**fd_kwargs))
    return RevisionPlan.objects.bulk_create(revision_plans_objects)

def save_equipments(equipments, fipe_id, year):
    equipments_objects = []
    for equipment in equipments:
        fd_kwargs = {
            'fipe_id': fipe_id,
            'year': year,
            'description': equipment['description'],
            'is_series': equipment['isSeries'],
        }
        equipments_objects.append(Equipment(**fd_kwargs))
    return Equipment.objects.bulk_create(equipments_objects)

def save_parts_data_object(parts_data, year, fipeId):
    parts_objects = []
    for part in parts_data:
        fd_kwargs = {
            'year': year,
            'fipe_id': fipeId,
            'nickname_id': part['nicknameId'],
            'nickname_description': part['nicknameDescription'],
            'complement': part['complement'],
            'part_number': part['partNumber'],
            'is_genuine': part['isGenuine'],
            'value': part['value'],
            'aftermarket_maker_description': part['aftermarketMakerDescription']
        }
        parts_objects.append(Part(**fd_kwargs))
    return Part.objects.bulk_create(parts_objects)


def save_suiv_data(data):
    fipe_data_collection = data.get('fipeDataCollection', [])
    suiv_data_collection = data.get('suivDataCollection', [])
    vehicle_data = {k: v for k, v in data.items() if k not in [
        'fipeDataCollection', 'suivDataCollection']}

    # Instancia veículo
    vehicle = save_vehicle_data_object(vehicle_data)

    # Intancia objetos FipeData
    save_fipe_data_objects(fipe_data_collection, vehicle)

    # Intancia objetos PriceHistory
    save_price_history_data_objects(fipe_data_collection, vehicle)

    # Intancia objetos SuivData
    save_suiv_data_objects(suiv_data_collection, vehicle)

    return vehicle


def save_fipe_data_objects(fipe_data_collection, vehicle):
    fipe_data_objects = []
    for fipe_data in fipe_data_collection:
        fd_kwargs = {
            'year': fipe_data['year'],
            'fipe_id': fipe_data['fipeId'],
            'maker_description': fipe_data['makerDescription'],
            'model_description': fipe_data['modelDescription'],
            'version_description': fipe_data['versionDescription'],
            'fuel': fipe_data['fuel'],
            'current_value': fipe_data['currentValue'],
            'vehicle': vehicle
        }
        fipe_data_objects.append(FipeData(**fd_kwargs))
    return FipeData.objects.bulk_create(fipe_data_objects)


def save_price_history_data_objects(fipe_data_collection, vehicle):
    price_history_objects = []
    for fipe_data in fipe_data_collection:
        fipe_data_obj = FipeData.objects.get(fipe_id=fipe_data['fipeId'], vehicle=vehicle)
        for price_history in fipe_data['priceHistory']:
            ph_kwargs = {
                'month_update': price_history['monthUpdate'],
                'year_update': price_history['yearUpdate'],
                'value': price_history['value'],
                'is_prediction': price_history['isPrediction'],
                'fipe_data': fipe_data_obj,
            }
            price_history_objects.append(PriceHistory(**ph_kwargs))
    return PriceHistory.objects.bulk_create(price_history_objects)


def save_suiv_data_objects(suiv_data_collection, vehicle):
    suiv_data_objects = []
    for suiv_data in suiv_data_collection:
        sd_kwargs = {
            'fipe_id': suiv_data['fipeId'],
            'version_id': suiv_data['versionId'],
            'version_description': suiv_data['versionDescription'],
            'model_id': suiv_data['modelId'],
            'model_description': suiv_data['modelDescription'],
            'maker_id': suiv_data['makerId'],
            'maker_description': suiv_data['makerDescription'],
            'vehicle': vehicle
        }
        suiv_data_objects.append(SuivData(**sd_kwargs))
    return SuivData.objects.bulk_create(suiv_data_objects)


def save_vehicle_data_object(vehicle_data):
    vehicle_kwargs = {
        'plate': vehicle_data['plate'],
        'year_model': vehicle_data['yearModel'],
        'year_fab': vehicle_data['yearFab'],
        'fuel': vehicle_data['fuel'],
        'chassis': vehicle_data['chassis'],
        'type': vehicle_data['type'],
        'species': vehicle_data['species'],
        'bodywork': vehicle_data['bodywork'],
        'power': vehicle_data['power'],
        'is_national': vehicle_data['isNational'],
        'axis_count': vehicle_data['axisCount'],
        'total_gross_weight': vehicle_data['totalGrossWeight'],
        'maximum_traction_capacity': vehicle_data['maximumTractionCapacity'],
        'gear_box_number': vehicle_data['maximumTractionCapacity'],
        'back_axis_count': vehicle_data['backAxisCount'],
        'aux_axis_count': vehicle_data['auxAxisCount'],
        'engine_number': vehicle_data['engineNumber'],
        'maker': vehicle_data['maker'],
        'maker_id': vehicle_data['makerId'],
        'description': vehicle_data['description'],
        'fipe_id': vehicle_data['fipeId'],
        'seat_count': vehicle_data['seatCount']
    }

    vehicle = Vehicle(**vehicle_kwargs)
    vehicle.save()
    return vehicle
