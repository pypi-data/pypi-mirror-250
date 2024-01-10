import scipy.io as scio
import pandas as pd
import numpy as np

class IO:
    """数据保存和加载
    """
    def save_excel(self, fp:str, *data, header=False, index=False):
        """保存为.excel
        """
        dataset = []
        for dat in data:
            dataset.append(pd.DataFrame(dat))
        with pd.ExcelWriter(fp) as xlsx:
            for i,data in enumerate(dataset):
                data.to_excel(xlsx,'Sheet%d'%(i+1),header=header,index=index)

    def load_excel(self, fp:str, sheet:str="Sheet1", header=None):
        """加载excel, 返回numpy类型数据
        """
        # 读取excell数据
        return pd.read_excel(fp,sheet_name=sheet,header=header).to_numpy()  

    def save_npz(self, fp:str, *data:dict):
        """保存为.npz
        """
        dataset = {}
        for dat in data:
            dataset.update(dat)
        np.savez(fp, **dataset)
 
    def load_npz(self, fp, **argkeys):
        """加载npz格式数据, 返回numpy类型数据
        """
        return np.load(fp, **argkeys)

    def save_csv(self, fp:str, *dataFrame:dict):
        """保存为.csv
        """
        data = pd.DataFrame(data)
        data.to_csv(fp) 

    def load_csv(self, fp:str):
        """加载.csv文件, 返回numpy类型数据
        """
        return pd.read_csv(fp).to_numpy()

    def svae_txt(self, fp:str, data:dict):
        """保存为.txt
        """
        data = pd.DataFrame(data)
        np.savetxt(fp, data)
   
    def load_txt(self, fp:str, sep=None, header=None, index=None):
        """加载txt文件, 返回numpy类型数据
        """
        return pd.read_csv(fp, sep=sep, header=header, index_col=index).to_numpy()
    
    def save_mat(self, fp:str, mdict:dict={}):
        """保存为.mat文件
        """
        scio.savemat(fp, mdict)

    def load_mat(self, fp:str, keys:dict={}, default=None):
        """加载.mat文件
        """
        mdict = scio.loadmat(fp)
        output = []
        for key in keys:
            output.append(mdict.get(key, default))
        return output

    def user_save_npz_2d(self, fp:str, train_p=None, train_x=None, train_y=None, test_p=None, test_x=None, test_y=None):
        """用户数据保存2D (npz数据格式)
        """
        np.savez(fp,train_p=train_p,train_x=train_x,train_y=train_y,
                                test_p=test_p,test_x=test_x,test_y=test_y)

    def user_load_npz_2d(self, fp:str):
        """用户数据加载2D (npz数据格式), 返回numpy类型数据
        """
        with np.load(fp) as f:
            train_p,train_x,train_y = f['train_p'],f['train_x'],f['train_y']
            test_p,test_x,test_y = f['test_p'],f['test_x'],f['test_y']
        return (train_p,train_x,train_y), (test_p,test_x,test_y)

    def user_save_npz_3d(self, fp:str, train_p=None, train_x=None, train_y=None, train_z=None, test_p=None, test_x=None, test_y=None, test_z=None):
        """用户数据保存3D (npz数据格式)
        """
        # 数据保存.npz
        np.savez(fp, train_p=train_p, train_x=train_x, train_y=train_y, train_z=train_z,
                            test_p=test_p, test_x=test_x, test_y=test_y, test_z=test_z)

    def user_load_npz_3d(self, fp:str):
        """用户数据加载3D (npz数据格式), 返回numpy类型数据
        """
        with np.load(fp) as f:
            train_p, train_x, train_y, train_z = f['train_p'], f['train_x'], f['train_y'], f['train_z']
            test_p, test_x, test_y, test_z = f['test_p'], f['test_x'], f['test_y'], f['test_z']
        return (train_p,train_x,train_y,train_z), (test_p,test_x,test_y,test_z)

    def dataset_save_npz(self, fp:str, train_inputs=None, train_outputs=None, test_inputs=None, test_outputs=None):
        """保存数据集
        加载: dataset_load_npz(fp)
        """
        np.savez(fp, train_inputs=train_inputs, train_outputs=train_outputs, 
                        test_inputs=test_inputs, test_outputs=test_outputs)

    def dataset_load_npz(self, fp:str):
        """加载数据集, 返回numpy类型数据
        """
        with np.load(fp, allow_pickle=True) as f:
            train_inputs, train_outputs = f['train_inputs'], f['train_outputs'] 
            test_inputs, test_outputs = f['test_inputs'], f['test_outputs']
        return (train_inputs, train_outputs), (test_inputs, test_outputs)

