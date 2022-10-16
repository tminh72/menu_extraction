import threading
import cv2
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from post_process import *
from craft_text_detector import Craft
import numpy as np
from fuzzywuzzy import process
from symspellpy import Verbosity, SymSpell
import json
from mmocr.utils.ocr import MMOCR
import time
class Extractor:
   def __init__(self):
      self.config = Cfg.load_config_from_file('./config/vgg-transformer.yml')
      self.config['weights'] = './vietocr/weights/transformerocr.pth'
      self.config['cnn']['pretrained'] = False
      self.config['device'] = 'cpu'
      self.config['predictor']['beamsearch'] = False
      # self.reader_craf = Craft(weight_path_craft_net = './craft_text_detector/weights/craft_mlt_25k.pth', 
      #                   weight_path_refine_net = './craft_text_detector/weights/craft_refiner_CTW1500.pth',crop_type="poly", cuda=False)
      self.recog_model = Predictor(self.config)
      self.init_fuzzy_dictionary()
      self.init_dict_food_name()
      self.detect_model = MMOCR(recog=None,
                           det='FCE_CTW_DCNv2', det_ckpt='fcenet_r50dcnv2_fpn_1500e_ctw1500_20211022-e326d7ec.pth',
                           det_config='fcenet_r50dcnv2_fpn_1500e_ctw1500.py'
                          )
      self.time_infer = 0
                          
   def init_dict_food_name(self):
    with open('./food_name_en.json', encoding = 'utf') as json_file:
        self.dict_food_name = json.load(json_file)['dict_food_name']

   def load_img(self, img_path):
      self.img_path = img_path
      self.results = []
      self.words = []

   def init_fuzzy_dictionary(self):
    self.sym_spell = SymSpell(max_dictionary_edit_distance=6, prefix_length=7)
    dictionary_path = 'food_dictionary.txt'
    self.sym_spell.load_dictionary(dictionary_path, 0, 1, separator="$", encoding='utf-8')

   def rect_centers(self,rect):
    rect_center= []
    for r in rect:
        x_center = r[0] + r[2]/2
        y_center = r[1] + r[3]/2
        rect_center.append((x_center, y_center))
    return rect_center

   def mapping_one_line(self,rect):
    # rect = [(), (), ...]
    res = []  
    rect_center_coor = self.rect_centers(rect)
    i = 0 
    check = [None for _ in range(len(rect))]
    while i < len(rect):
        if check[i] is None:
            check[i] = True
            curr = []
            k = i + 1
            y_min = rect[i][1]
            y_max = rect[i][1] + rect[i][3]
            curr.append(i)
            while k < len(rect):
                if rect_center_coor[k][1] < y_max and rect_center_coor[k][1] > y_min:
                    curr.append(k)
                    check[k] = True
                k += 1
            res.append(curr)
        i += 1    
    return res 

   def extract_bounding_box(self):
      # if isinstance(self.img_path, str):
      #     ## Detect + OCR ##
      #     image_path = self.img_path
      #     image = cv2.imread(image_path)
      #     self.img = image
      #     result = self.reader_craf.detect_text(image)['polys']
      #     pts =  [np.array(res).astype(np.int32) for res in result]
      #     rect = [cv2.boundingRect(pt) for pt in pts]
      # elif type(self.img_path) == np.ndarray:
      #     image = self.img_path
      #     self.img = self.img_path
      #     result = self.reader_craf.detect_text(image)['polys']
      #     pts =  [np.array(res).astype(np.int32) for res in result]
      #     rect = [cv2.boundingRect(pt) for pt in pts]
      # return rect
      if isinstance(self.img_path, str):
          ## Detect + OCR ##
          image_path = self.img_path
          image = cv2.imread(image_path)
          self.img = image
          output = self.detect_model.readtext(self.img_path)
          rect = [cv2.boundingRect(np.array(pt, dtype="int")[:-1].reshape(-1,2)) for pt in output[0]['boundary_result']]
      elif type(self.img_path) == np.ndarray:
          ## Detect + OCR ##
          image = self.img_path
          self.img = self.img_path
          output = self.detect_model.readtext(self.img_path)
          rect = [cv2.boundingRect(np.array(pt, dtype="int")[:-1].reshape(-1,2)) for pt in output[0]['boundary_result']]
      return rect

   def extract_bounding_box_pairs(self, rect: list):
      return self.mapping_one_line(rect) # result is a list whose element is a list of 
                              # bounding boxes' indexes that are on the same line
   def vietocr_processing(self, rect: list, index: list):
      # Loop over each groups
      for ind_bbxes in index:
         ocr_ls = []
         # Loop over each box
         try:
            for ind_bbx in ind_bbxes:
               bbox = rect[ind_bbx]
               bbox_x = bbox[0] - 5 if bbox[0] > 5 else bbox [0] 
               bbox_y = bbox[1] - 5 if bbox[1] > 5 else bbox[1]
               bbox_x_max = bbox[0] + bbox[2] + 5 if bbox[0] > 5 else bbox[0] + bbox[2]
               bbox_y_max = bbox[1] + bbox[3] + 5 if bbox[1] > 5 else bbox[1] + bbox[3]
               bbox = self.img[bbox_y:bbox_y_max, bbox_x:bbox_x_max]
               word = self.recog_model.predict(bbox)
               ocr_ls.append(word)
         except Exception as e:
               print(e)
               continue
         self.pairing(ocr_ls)
         

   def translator(self, food_name_vi):
    if food_name_vi.upper() in self.dict_food_name.keys():
          return self.dict_food_name.__getitem__(food_name_vi.upper())
    return food_name_vi

   def pairing(self, line: list):
      if len(line) == 1:
         res = one_bbx_1line(line, self.fuzzy_check, self.translator)

         if res:
            self.results.append(res)
      elif len(line) == 2:
         res = two_bbx_1line(line, self.fuzzy_check, self.translator)
         if res:
            self.results.append(res)
      else:
         res = many_bbx_1line(line, self.fuzzy_check, self.translator)
         if res:
            if len(res) == 1:
               self.results.append(res)
            else:
               self.results.extend(res)

   def run(self):
      self.time_infer = time.time()
      rect = self.extract_bounding_box()
      ind = self.extract_bounding_box_pairs(rect)
      self.vietocr_processing(rect, ind)

   def fuzzy_check(self, term: str):
      suggestions = self.sym_spell.lookup(term, Verbosity.ALL, max_edit_distance=6, include_unknown=True)
      ls = []
      for suggestion in suggestions:
         ls.append(suggestion.term)
      res = process.extract(term, ls)
      return res[0][0]


if __name__ == '__main__':
  extractor = Extractor()
  extractor.load_img('D:\AI\AI_Hackathon_QAI\AI_Hackathon_Problem1\Data_Menu\\015.jpeg')
  extractor.run()
  print(extractor.results)

  