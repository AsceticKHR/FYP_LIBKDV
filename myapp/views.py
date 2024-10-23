from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from keplergl import KeplerGl
from libkdv import kdv
import pandas as pd
import geopandas as gpd


@api_view(['POST'])
def upload_file(request):

    file = request.FILES['file']
    if not file:
        return Response({'error': 'No file provided'}, status=400)
    print("Reading CSV file.")
    NewYork = pd.read_csv(file)



    if NewYork.size == 0:
        return Response({'error': 'Uploaded file is empty'}, status=400)
    print("Computing KDV...")
    kdv_NewYork = kdv(NewYork, GPS=True, KDV_type='KDV', row_pixels=1280, col_pixels=960)

    bandwidths_NewYork = list(range(100, 1901, 200))
    print("Concatenating results...")
    result_NewYork = []
    for band in bandwidths_NewYork:
        kdv_NewYork.bandwidth = band
        result_NewYork.append(kdv_NewYork.compute())

    all_result_NewYork = result_NewYork[0]
    all_result_NewYork['bw'] = 0
    for i, result in enumerate(result_NewYork[1:]):
        result['bw'] = i + 1
        all_result_NewYork = pd.concat([all_result_NewYork, result])


    print("Generating KeplerGl map...")  # 输出生成地图的消息
    # 创建 KeplerGl 地图
    config_NewYork_bands = {'version': 'v1', 'config': {'visState': {'filters': [
        {'dataId': ['unnamed'], 'id': '1z1xy9sp', 'name': ['bw'], 'type': 'range', 'value': [7.88, 8.3],
         'enlarged': False, 'plotType': 'histogram', 'animationWindow': 'free', 'yAxis': None, 'speed': 1}], 'layers': [
        {'id': '5e707zf', 'type': 'point', 'config': {'dataId': 'unnamed', 'label': 'Point', 'color': [130, 154, 227],
                                                      'highlightColor': [252, 242, 26, 255],
                                                      'columns': {'lat': 'lat', 'lng': 'lon', 'altitude': None},
                                                      'isVisible': True,
                                                      'visConfig': {'radius': 10, 'fixedRadius': False, 'opacity': 0.8,
                                                                    'outline': False, 'thickness': 2,
                                                                    'strokeColor': None,
                                                                    'colorRange': {'name': 'Custom Palette',
                                                                                   'type': 'custom',
                                                                                   'category': 'Custom',
                                                                                   'colors': ['#0000ff', '#007fff',
                                                                                              '#00ffff', '#00ff80',
                                                                                              '#00ff00', '#80ff00',
                                                                                              '#ffff00', '#ff8000',
                                                                                              '#ff0000', '#ff0000',
                                                                                              '#ff0000', '#ff0000']},
                                                                    'strokeColorRange': {'name': 'Global Warming',
                                                                                         'type': 'sequential',
                                                                                         'category': 'Uber',
                                                                                         'colors': ['#5A1846',
                                                                                                    '#900C3F',
                                                                                                    '#C70039',
                                                                                                    '#E3611C',
                                                                                                    '#F1920E',
                                                                                                    '#FFC300']},
                                                                    'radiusRange': [0, 50], 'filled': True},
                                                      'hidden': False, 'textLabel': [
                {'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start',
                 'alignment': 'center'}]},
         'visualChannels': {'colorField': {'name': 'val', 'type': 'real'}, 'colorScale': 'quantize',
                            'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None,
                            'sizeScale': 'linear'}}], 'interactionConfig': {
        'tooltip': {'fieldsToShow': {'unnamed': [{'name': 'val', 'format': None}, {'name': 'bw', 'format': None}]},
                    'compareMode': False, 'compareType': 'absolute', 'enabled': True},
        'brush': {'size': 0.5, 'enabled': False}, 'geocoder': {'enabled': False}, 'coordinate': {'enabled': False}},
                                                                     'layerBlending': 'normal', 'splitMaps': [],
                                                                     'animationConfig': {'currentTime': None,
                                                                                         'speed': 1}},
                                                        'mapState': {'bearing': 0, 'dragRotate': False,
                                                                     'latitude': 40.20444200178999,
                                                                     'longitude': -74.47239475038594, 'pitch': 0,
                                                                     'zoom': 8.38221371779276, 'isSplit': False},
                                                        'mapStyle': {'styleType': 'dark', 'topLayerGroups': {},
                                                                     'visibleLayerGroups': {'label': True, 'road': True,
                                                                                            'border': False,
                                                                                            'building': True,
                                                                                            'water': True, 'land': True,
                                                                                            '3d building': False},
                                                                     'threeDBuildingColor': [9.665468314072013,
                                                                                             17.18305478057247,
                                                                                             31.1442867897876],
                                                                     'mapStyles': {},
                                                                     'showMapboxLogo': False
                                                                     }}}

    map_NewYork = KeplerGl(height=1000, config=config_NewYork_bands)


    # 直接添加 DataFrame 数据
    map_NewYork.add_data(data=all_result_NewYork, name='NewYork Data')
    print("Saving map to HTML...")
    kdv_map_html = map_NewYork._repr_html_()  # 直接获取 HTML 内容

    return HttpResponse(kdv_map_html)
    # 返回 HTML 内

# @api_view(['POST'])
# def upload_file(request):
#     uploaded_file = request.FILES['file']
#     file_name = uploaded_file.name
#
#     # 处理上传的文件（保存到数据库、执行分析等操作）
#
#     response_data = {
#         'message': 'File uploaded and processed successfully',
#         'file_name': file_name
#     }
#
#     return JsonResponse(response_data)

# Create your views here.
def index(request):
    return render(request, 'index.html')