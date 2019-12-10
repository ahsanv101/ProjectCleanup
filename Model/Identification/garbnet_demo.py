##import os
##import caffe
##from pylab import *
##from PIL import Image
##import numpy as np
##import cv2
##

import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db

def listener(event):
    #print(event.event_type)  # can be 'put' or 'patch'

    # print(event.path)  # relative to the reference, it seems
    try:
        url = event.data['imageUrl'].split('/')[7].split('?')[0].replace('%2F', '/')
        print(event.path)

        #bucket = storage.bucket()
        #blob = bucket.get_blob(url)
       # file = url.split('/')[1]
      # blob.download_to_filename('input/'+file)

    except KeyError:
        print("All is Well. Try next time\n")
    # j = {'description': '', 'imageUrl': 'https://firebasestorage.googleapis.com/v0/b/ionicimageupload-977ea.appspot.com/o/teachers_uploads%2F1575902554178.jpg?alt=media&token=472c506b-7b54-4f86-a265-ae54f3d65734', 'name': 'No Name'}
    # print(j['imageUrl'])


cred = credentials.Certificate('ServiceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'ionicimageupload-977ea.appspot.com',
    'databaseURL': 'https://ionicimageupload-977ea.firebaseio.com/'
})
#bucket = storage.bucket()
#blob = bucket.get_blob('teachers_uploads/1575899407118.png')
#blob.download_to_filename('input/1575899407118.png')


# Get a database reference to our posts
ref = db.reference().listen(listener)
# Read the data at the posts reference (this is a blocking operation)
j = []
#j = ref
# print(ref)


# As an admin, the app has access to read and write all data, regradless of Security Rules
#ref = db.reference('restricted_access/secret_document')
#print(ref.get())




def gatherImages(folder,imageNames=None):
    images = []
    names = []
    files = os.listdir(folder)
    total = len(files)
    print('Total %d images in folder %s' % (total,folder))
    for i in os.listdir(folder):
        try:
            if imageNames is None or i in imageNames:
                example_image = folder+'/'+i
                input_image = Image.open(example_image)
                images.append(input_image)
                names.append(i)
        except:
            pass

    return images,names

def resizeForFCN(image,size):
    w,h = image.size
    if w<h:
        return image.resize((int(227*size),int((227*h*size)/w))) #227x227 is input for regular CNN
    else:
        return image.resize((int((227*w*size)/h),int(227*size)))
    
def getSegmentedImage(test_image, probMap,thresh):
    kernel = np.ones((6,6),np.uint8)
    wt,ht = test_image.size
    out_bn = np.zeros((ht,wt),dtype=uint8)
    
    for h in range(probMap.shape[0]):
                for k in range(probMap.shape[1]):
                    if probMap[h,k] > thresh:
                        x1 = h*62 #stride 2 at fc6_gb_conv equivalent to 62 pixels stride in input
                        y1 = k*62
                        for hoff in range(x1,227+x1):
                            if hoff < out_bn.shape[0]:
                                for koff in range(y1,227+y1):
                                    if koff < out_bn.shape[1]:
                                        out_bn[hoff,koff] = 255
    edge = cv2.Canny(out_bn,200,250)
    box = cv2.dilate(edge,kernel,iterations = 3)
    
    or_im_ar = np.array(test_image)
    or_im_ar[:,:,1] = (or_im_ar[:,:,1] | box)
    or_im_ar[:,:,2] = or_im_ar[:,:,2] * box + or_im_ar[:,:,2]
    or_im_ar[:,:,0] = or_im_ar[:,:,0] * box + or_im_ar[:,:,0]
    
    return Image.fromarray(or_im_ar)
    
    
def getPredictionsFor(images,names,size,thresh,output_folder):
    for i in range(len(images)):
        try:
            test_image = resizeForFCN(images[i],size)
            
            in_ = np.array(test_image,dtype = np.float32)
            in_ = in_[:,:,::-1]
            in_ -= np.array(mean.mean(1).mean(1))
            in_ = in_.transpose((2,0,1))

            net.blobs['data'].reshape(1,*in_.shape)
            net.blobs['data'].data[...] = in_
            net.forward()
            
            probMap =net.blobs['prob'].data[0,1]
            print (names[i]+'...',)
            if len(np.where(probMap>thresh)[0]) > 0:
                print ('Garbage!')
            else:
                print ('Not Garbage!')
            
            out_ = getSegmentedImage(test_image, probMap,thresh)
            out_.save(output_folder + '/output_' + names[i])
        except:
            pass

##
##mean_filename='SpotGarbage_GarbNet/garbnet_mean.binaryproto'
##deploy_filename = 'SpotGarbage_GarbNet/deploy_garbnet.prototxt'
##caffemodel_file = 'SpotGarbage_GarbNet/garbnet_fcn.caffemodel'
##
##proto_data = open(mean_filename, "rb").read()
##a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
##mean  = caffe.io.blobproto_to_array(a)[0]
##
##net = caffe.Net(deploy_filename,caffemodel_file,caffe.TEST)
##
###specify 'input' folder containing images for prediction
##images,names = gatherImages('input')
###specify 'output' folder to store segmented predictions
##getPredictionsFor(images,names,4,0.999,'output')
