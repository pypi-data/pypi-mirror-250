import warnings
warnings.filterwarnings("ignore")

import grpc
import vdb_pb2
import vdb_pb2_grpc
import numpy as np
import scipy
from tqdm import tqdm
import time

class vecml:
  channel = 0
  stub = 0
  host = ''
  port = 0
  MAX_MESSAGE_LENGTH = 1024 * 1024 * 1024
  step = 25
  api_key = 'empty';

  def init(api_key, region):
    if region == 'us-west':
      vecml.host = '35.247.90.126'
    else:
      print('Unsupported region [{}]. Current choices are [us-west].'.format(region))
      return;
    vecml.api_key = api_key;
    channel = grpc.insecure_channel(vecml.host + ':80',
      options=[
        ('grpc.max_send_message_length', vecml.MAX_MESSAGE_LENGTH),
        ('grpc.max_receive_message_length', vecml.MAX_MESSAGE_LENGTH),
      ], compression=grpc.Compression.Gzip)
    stub = vdb_pb2_grpc.VectorDBStub(channel)
    response = stub.request_port(vdb_pb2.Request(api_key=vecml.api_key))
    vecml.port = response.dest_port
    vecml.address = response.dest_address
    time.sleep(0.500)
    vecml.channel = grpc.insecure_channel(vecml.address + ':' + str(vecml.port),
      options=[
        ('grpc.max_send_message_length', vecml.MAX_MESSAGE_LENGTH),
        ('grpc.max_receive_message_length', vecml.MAX_MESSAGE_LENGTH),
      ], compression=grpc.Compression.Gzip)
    vecml.stub = vdb_pb2_grpc.VectorDBStub(vecml.channel)

  def close():
    vecml.channel.close()
    vecml.channel = 0
    vecml.stub = 0

  def check_init():
    if vecml.stub == 0:
      raise Exception("Shoreline is not initialized. Please run vecml.init.")

  def filter_validation(filter_str):
    return True

  def insert_dense_data(name, data, label=[]):
    if isinstance(label,list) and label == []:
      vecml.insert(name,data,list(range(0, np.array(data).shape[0])))
    else:
      label_dict = [];
      for i in range(len(label)):
        label_dict.append({'label': label[i]})
      vecml.insert(name,data,list(range(0, np.array(data).shape[0])),attributes=label_dict)
  
  def insert_sparse_data(name, data, label=[]):
    if isinstance(data, scipy.sparse.csr_matrix) == False:
      data = scipy.sparse.csr_matrix(data)
    if isinstance(label,list) and label == []:
      vecml.insert_sparse(name,data,list(range(0, data.shape[0])))
    else:
      label_dict = [];
      for i in range(len(label)):
        label_dict.append({'label': label[i]})
      vecml.insert_sparse(name,data,list(range(0, data.shape[0])),attributes=label_dict)

  def insert(name, data, ids, **kwargs):
    vecml.check_init()
    data = np.array(data)
    dim = data.shape[1]
    n_data = len(ids)

    attributes = []
    if 'attributes' in kwargs:
      dicts = kwargs['attributes']
      for d in dicts:
        converted_map = dict()
        for key, value in d.items():
          tmp = vdb_pb2.GeneralType(float_value = float(value),int_value = int(value))
          converted_map[key] = tmp
        attributes.append(vdb_pb2.AttributeRow(attr=converted_map))

    step = max(1, n_data // vecml.step)
    pbar = tqdm(total=n_data)

    for i in range(0, n_data, step):
      begin = i
      end = min(i + step, n_data)
      if len(attributes) != 0:
        response = vecml.stub.insert(vdb_pb2.Request(api_key=vecml.api_key,table_name=name,vectors=vdb_pb2.Vectors(len=end - begin, dim=dim, data=data[begin:end,:].flatten().tolist(), ids=ids[begin:end], attribute_row=attributes[begin:end])))
      else:
        response = vecml.stub.insert(vdb_pb2.Request(api_key=vecml.api_key,table_name=name,vectors=vdb_pb2.Vectors(len=end - begin, dim=dim, data=data[begin:end,:].flatten().tolist(), ids=ids[begin:end])))

      if response.code != 0:
        print("[Warning]: Insertion failed. Error code:", response.code)
        return
      pbar.update(step)
    pbar.close()
  
  def insert_sparse(name, data, ids, **kwargs):
    vecml.check_init()
    n_data = len(ids)
    dim = (1 << 21)

    if isinstance(data, scipy.sparse.csr_matrix) == False:
      data = scipy.sparse.csr_matrix(data)

    attributes = []
    if 'attributes' in kwargs:
      dicts = kwargs['attributes']
      for d in dicts:
        converted_map = dict()
        for key, value in d.items():
          tmp = vdb_pb2.GeneralType(float_value = float(value),int_value = int(value))
          converted_map[key] = tmp
        attributes.append(vdb_pb2.AttributeRow(attr=converted_map))
    
    step = max(1,n_data // vecml.step)
    pbar = tqdm(total=n_data)
    
    for i in range(0, n_data, step):
      begin = i
      end = min(i + step, n_data)
      subdata = data[begin:end,:]
      response = vecml.stub.insert_sparse(vdb_pb2.Request(api_key=vecml.api_key,table_name=name,vectors=vdb_pb2.Vectors(len=end - begin, dim=dim, data=subdata.data.tolist(), offset=subdata.indptr.tolist(), idx=subdata.indices.tolist(), ids=ids[begin:end], attribute_row=attributes[begin:end])))
      if response.code != 0:
        print("[Warning]: Insertion failed. Error code:", response.code)
        return
      pbar.update(step)
    pbar.close()
  
  def create_dense_data(name, dim, **kwargs):
    vecml.check_init()
    index_type = 0
    schema = dict()
    if 'schema' in kwargs:
      if isinstance(kwargs['schema'],dict) == False:
        raise Exception("The schema argument has to be a dict")
        return
      schema = kwargs['schema']
    measure = "none"
    try:
      response = vecml.stub.index(vdb_pb2.Request(api_key=vecml.api_key,table_name=name,similarity=measure,vectors=vdb_pb2.Vectors(dim=dim,schema=schema),index_type=index_type))
    except:
      pass
    return name
  
  def create_sparse_data(name, **kwargs):
    vecml.check_init()
    index_type = 0
    schema = dict()
    dim = (1 << 21)
    if 'schema' in kwargs:
      if isinstance(kwargs['schema'],dict) == False:
        raise Exception("The schema argument has to be a dict")
        return
      schema = kwargs['schema']
    measure = "none"
    try:
      response = vecml.stub.index(vdb_pb2.Request(api_key=vecml.api_key,table_name=name,similarity=measure,vectors=vdb_pb2.Vectors(dim=dim,schema=schema),index_type=1))
    except:
      pass
    return name
  
  def train(name, label_attr, task, **kwargs):
    if task not in ["classification","regression"]:
      raise ValueError('Task must be either "classification" or "regression".')
    valid_split_ratio = 0
    if('valid_split_ratio' in kwargs):
      valid_split_ratio = float(kwargs['valid_split_ratio'])
    valid_data = name
    if('valid_data' in kwargs):
      valid_data = kwargs['valid_data']
    vecml.check_init()
    dummy_str = ''
    model_type = 4
    if task == "regression":
      model_type = 5
    for res_str in vecml.stub.train(vdb_pb2.Request(api_key=vecml.api_key,table_name=name,valid_split_ratio=valid_split_ratio,valid_table_name=valid_data,label_name=label_attr,model_type=model_type)):
      dummy_str += res_str.str
  
  def predict(name, test_data):
    vecml.check_init()
    response = vecml.stub.predict(vdb_pb2.Request(api_key=vecml.api_key,table_name=name,valid_table_name=test_data))
    return np.array(response.label), np.array(response.probability).reshape(len(response.label),-1), [response.accuracy, response.rocauc, response.mse, response.r2, response.mae]

  def delete_data(name):
    vecml.check_init()
    vecml.stub.delete_index(vdb_pb2.Request(api_key=vecml.api_key,table_name=name))
