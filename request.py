import time
import requests
import base64
import os,json,sys
import base64
import cv2
import asyncio




def test(response):
    '''
    args: 
    response is a dictionary including image_name and infers
    print:
    precision = True positive/ label_total
    recall = True positive/ predict_total
    '''
    json_path = os.path.join(r"C:\Users\tuanm\Downloads\Data_Menu_label\Data_Menu_label", response['image_name'].replace('jpeg', 'json'))
    with open(json_path, encoding='utf8') as json_file:     
        data = json.load(json_file)
    # print(f"data: {data}")
    gt_food_name_vi_and_price = {item['food_name_vi']:item["food_price"] for item in data['infers']}
    gt_food_name_vi_and_en = {item['food_name_vi']:item["food_name_en"].upper() for item in data['infers']}
    pred_food_name_vi_and_price = {item['food_name_vi']:item["food_price"] for item in response['infers']}
    pred_food_name_vi_and_en = {item['food_name_vi']:item["food_name_en"].upper() for item in response['infers']}
    # print(f"number of ground truth: {len(gt_food_name_vi_and_price.items())}")
    # print(f"number of prediction: {len(pred_food_name_vi_and_price.items())}")
    print('-------------------------------------------------')
    print(f"Image: {response['image_name']}")
    i = 0
    k = 0
    for food_name, price in pred_food_name_vi_and_price.items():
      if food_name in list(gt_food_name_vi_and_price.keys()):
        if price == gt_food_name_vi_and_price[food_name]:
          i+=1
          if gt_food_name_vi_and_en[food_name]==pred_food_name_vi_and_en[food_name]:
            k+=1
          else:
            print(f"error food_name_en: {pred_food_name_vi_and_en[food_name]}: {food_name}")
        else:
          print(f"food_name : {food_name}, error price: {price}")
      else:
        print(f"error food_name not in menu : {food_name}, price: {price}")
    print(f"precision for food and price: {i}/{len(gt_food_name_vi_and_price.items())}")
    # print(f"recall for food and price: {i}/{len(pred_food_name_vi_and_price.items())}")
    print(f"precision for translate: {k}/{len(gt_food_name_vi_and_price.items())}")
    # print(f"recall for translate: {k}/{len(pred_food_name_vi_and_price.items())}")

async def get_response(img_path):
  
  with open(img_path, "rb") as image_file:
     data = base64.b64encode(image_file.read())
  
  image_name= os.path.basename(img_path)
  response = requests.post(
    url='http://localhost:5000/infer',
    data={
        "image": data,
        "image_name": image_name
    }
  )

  if response.status_code == 200:
    return response.json()

async def send_request():
  path_base = r'D:\AI\AI_Hackathon_QAI\AI_Hackathon_Problem1\Data_Menu'
  for i in range(89,100):
    _str = str(i)
    if i >= 10 and i < 100:
        _str = '0'+str(i)
    elif i < 10:
        _str = '00'+str(i)
    image_path = os.path.join(path_base, _str + '.jpeg')
    try:
      start_one_image = time.time()
      res = await get_response(image_path)
      test(res)
      print(f'Infer one image: {time.time() - start_one_image}')
    except Exception as e :
      print(e)
      pass

if __name__ == '__main__':
  start_infer = time.time()
  loop = asyncio.get_event_loop()
  loop.run_until_complete(send_request())
  print(f'Time infer: {time.time() - start_infer}')


  # img_path = r'D:\AI\AI_Hackathon_QAI\AI_Hackathon_Problem1\Data_Menu\052.jpeg'
  # with open(img_path, "rb") as image_file:
  #    data = base64.b64encode(image_file.read())
  
  # image_name= os.path.basename(img_path)
  # response = requests.post(
  #   url='http://localhost:5000/infer',
  #   data={
  #       "image": data,
  #       "image_name": image_name
  #   }
  # )

  # if response.status_code == 200:
  #   print(response.json())
  #   res = response.json()
  #   test(res)







# DÊRANGMUỐI HONGLLONG