import os
import numpy as np
import cv2
import onnxruntime


from ..model_common import load_onnx, load_openvino


class DET2D106:
    def __init__(self,model_type,model_path,**kwargs):

        self.model_path = model_path
        self.model_type = model_type
        self.lmk_dim=2

        if self.model_type=='onnx':
            self.net = load_onnx.Onnx_session(self.model_path,input_mean=0.0, input_std=1.0,onnx_device='cpu',torch_image=True)
            self.input_shape = self.net.net.get_inputs()[0].shape
            self.input_size = tuple(self.input_shape[2:4][::-1])
            self.output_shape = self.net.net.get_outputs()[0].shape
            self.lmk_num = self.output_shape[1]//self.lmk_dim
        elif self.model_type=='openvino':
            self.net = load_openvino.Openvino(self.model_path,not_norm=True,torch_image=True,device='CPU')
            self.output_shape = self.net.net.outputs['fc1'].shape[1]
            self.lmk_num = self.output_shape//self.lmk_dim

    def get(self,img,face):
        img_size = [img.shape[0],img.shape[1]]
        det_img = img.copy()
        det_img = cv2.resize(det_img,(192,192))
        det_img = det_img.astype(np.float32)
        det_img = det_img.transpose([2, 0, 1])
        det_img = torch.tensor(det_img)
        det_img = torch.unsqueeze(det_img,dim=0)

        output = self.net(det_img)[0]
        output = output.reshape((-1, 2))

        output[:, 0:2] += 1
        output[:, 0:2] *= (img_size[0] // 2)

        face.land = output

        return output
        

    def get_fromImage(self,img):
        img_size = [img.shape[0],img.shape[1]]
        det_img = img.copy()
        det_img = cv2.resize(det_img,(192,192))
        det_img = det_img.astype(np.float32)
        det_img = det_img.transpose([2, 0, 1])
        det_img = torch.tensor(det_img)
        det_img = torch.unsqueeze(det_img,dim=0)

        output = self.net(det_img)[0]
        output = output.reshape((-1, 2))

        output[:, 0:2] += 1
        output[:, 0:2] *= (img_size[0] // 2)

        return output




