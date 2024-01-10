import time
import math


def get_traj_data(lAllVehi, simu_time, start_time, proj, p2m, move):
    traj_data = {
        "timestamp": str(int(time.time() * 1000)),
        "simu_time": simu_time,
        'start_sim_time': start_time,
        "count": len(lAllVehi),
        "objs": [],
    }
    
    for vehi in lAllVehi:
        if not vehi:
            continue

        x = p2m(vehi.pos().x()) + move["x_move"]
        y = -p2m(vehi.pos().y()) + move["y_move"]
        if math.isnan(x) or math.isnan(y):
            continue

        lon, lat = proj(x, y, inverse=True)

        in_link = vehi.roadIsLink()
        lane = vehi.lane()
        euler = vehi.vehicleDriving().euler()
        if not in_link or not lane or not euler:
            continue
        
        veh_data = {
            "id": vehi.id(),
            'roadId': vehi.roadId(),
            'inLink': in_link,
            'laneCount': in_link and lane.link().laneCount(),
            'laneNumber': in_link and lane.number(),
            'laneTypeName': in_link and lane.actionType(),
            'typeCode': vehi.vehicleTypeCode(),
            'angle': vehi.angle(),
            'speed': p2m(vehi.currSpeed()),
            'size': [p2m(vehi.length()), 2, 2],
            'color': "",
            'x': x,
            'y': y,
            'z': vehi.v3z(),
            'longitude': lon,
            'latitude': lat,
            'eulerX': euler.x(),
            'eulerZ': euler.y(),
            'eulerY': euler.z(),
        }

        traj_data['objs'].append(veh_data)

    traj_data["count"] = len(traj_data["objs"])

    return traj_data

