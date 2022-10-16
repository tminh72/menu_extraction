# STEP 1: Pull python image
FROM python:3.7

# STEP 2,3: CREATE WORK DIR AND COPY FILE TO WORK DIR
WORKDIR /app
COPY . /app

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
# STEP 4,5,6: INSTALL NECESSARY PACKAGE
RUN pip install --upgrade pip
RUN pip install gdown

RUN pip install torch==1.11.0
RUN pip install torchvision>=0.8.1,!=0.13.0

RUN pip install -U openmim
RUN mim install mmcv-full


RUN pip install -r requirements.txt
# STEP 8: RUN COMMAND
CMD ["python", "./api.py"]







