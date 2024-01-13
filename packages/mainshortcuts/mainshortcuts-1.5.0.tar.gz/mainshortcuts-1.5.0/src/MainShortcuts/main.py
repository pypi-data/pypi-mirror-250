# MainShortcuts by MainPlay YT
# https://t.me/MainPlay_YT
import json as _json
import MainShortcuts.addon as _a
import os as _os
import platform as _platform
import shutil as _shutil
import subprocess as _subprocess
import sys as _sys
# Универсальные команды
class m_proc: # Операции с текущим или другими процессами
  args=_sys.argv # Аргументы запуска программы
  pid=_os.getpid() # PID текущего процесса
  def run(args): # Запустить процесс ("nano example.txt" -> ["nano","example.txt"])
    p=_subprocess.Popen(args,stdout=_subprocess.PIPE)
    code=p.wait()
    out,err=p.communicate()
    if isinstance(out,bytes):
      out=out.decode("utf-8")
    elif not isinstance(out,str):
      out=str(out)
    if isinstance(err,bytes):
      err=err.decode("utf-8")
    elif not isinstance(err,str):
      err=str(err)
    return {"code":code,"output":out,"error":err,"c":code,"o":out,"e":err}
class m_path: # Операции с путями к файлам/папкам
  sep=_os.sep # Разделитель в пути файла
  separator=sep
  def exists(path): # Объект существует?
    return _os.path.exists(path)
  def merge(array): # Собрать путь к объекту из массива
    return m_path.sep.join(array)
  def split(path): # Разложить путь к объекту на массив
    return path.split(m_path.sep)
  def info(path,listdir=False,listlinks=False): # Информация о пути
    info={
      "dir":None, # Папка, в которой находится объект
      "dirs":None, # Рекурсивный список папок (если аргумент listdir=True)
      "exists":None, # Существует ли объект? | True/False
      "ext":None, # Расширение файла, даже если это папка
      "files":None, # Рекурсивный список файлов (если аргумент listdir=True)
      "fullname":None, # Полное название объекта (включая расширение)
      "fullpath":None, # Полный путь к объекту
      "link":None, # Это ссылка или оригинал? | True/False
      "name":None, # Название файла без расширения, даже если это папка
      "path":None, # Полученный путь к объекту
      "realpath":None, # Путь к оригиналу, если указана ссылка
      "size":None, # Размер. Для получения размера папки укажите аргумент listdir=True
      "split":[], # Путь, разделённый на массив
      "type":None # Тип объекта | "file"/"dir"
      }
    info["path"]=path
    info["split"]=m_path.split(path)
    info["dir"]=m_path.merge(info["split"][:-1])
    info["fullname"]=info["split"][-1]
    if "." in info["fullname"]:
      info["ext"]=info["fullname"].split(".")[-1]
      info["name"]=".".join(info["fullname"].split(".")[:-1])
    else:
      info["ext"]=None
      info["name"]=info["fullname"]
    info["exists"]=m_path.exists(path)
    if info["exists"]:
      info["fullpath"]=_os.path.abspath(path)
      info["link"]=_os.path.islink(path)
      if info["link"]:
        info["realpath"]=_os.path.realpath(path)
      if _os.path.isfile(path):
        info["size"]=_os.path.getsize(path)
        info["type"]="file"
      elif _os.path.isdir(path):
        info["type"]="dir"
        if listdir:
          tmp=_a.listdir(path,listlinks)
          info["dirs"]=tmp["d"]
          info["files"]=tmp["f"]
          info["size"]=tmp["s"]
      else:
        info["type"]="unknown"
    return info
  def delete(path): # Удалить
    info=m_path.info(path)
    if info["exists"]:
      if info["type"]=="file":
        _os.remove(path)
      elif info["type"]=="dir":
        _os.rmdir(path)
      else:
        raise Exception("Unknown type: "+info["type"])
  rm=delete
  # del=m_path.delete
  def copy(fr,to): # Копировать
    type=m_path.info(fr)["type"]
    if type=="file":
      _shutil.copy(fr,to)
    elif type=="dir":
      _shutil.copytree(fr,to)
    else:
      raise Exception("Unknown type: "+type)
  cp=copy
  def move(fr,to): # Переместить
    _shutil.move(fr,to)
  mv=move
  def rename(fr,to): # Переименовать
    _os.rename(fr,to)
  rn=rename
  def link(fr,to,force=False): # Сделать символическую ссылку
    if m_path.exists(to) and force:
      m_path.delete(to)
    _os.symlink(fr,to)
  ln=link
  def format(path,replace_to="_",replace_errors=True): # Форматировать путь к файлу (изменить разделитель, удалить недопустимые символы)
    for i in ["/","\\"]:
      path=path.replace(i,m_path.sep)
    if replace_errors:
      for i in ["\n",":","*","?","\"","<",">","|","+","%","!","@"]:
        path=path.replace(i,replace_to)
    return path
class m_os: # Операции с системой
  platform=_platform.system() # Тип ОС
  type=platform
def exit(code=0): # Закрытие программы с кодом
  _sys.exit(code)
class m_file: # Операции с файлами
  def read(path,encoding="utf-8"): # Прочитать текстовый файл
    if m_path.info(path)["type"]=="file":
      with open(path,"r",encoding=encoding) as f:
        text=f.read()
    else:
      text=""
    return text
  def write(path,text="",encoding="utf-8",force=False): # Записать текстовый файл
    if m_path.info(path)["type"]=="dir" and force:
      _os.remove(path)
    with open(path,"w",encoding=encoding) as f:
      f.write(f"{text}")
    return True
  def open(path): # Открыть содержимое файла
    if _os.path.exists(path):
      with open(path,"rb") as f:
        content=f.read()
    else:
      content=None
    return content
  def save(path,content,force=False): # Сохранить содержимое файла
    if m_path.info(path)["type"]=="dir" and force:
      _os.remove(path)
    with open(path,"wb") as f:
      f.write(content)
    return True
  def delete(path):
    typt=m_path.info(path)["type"]
    if typt=="file":
      _os.remove(path)
    else:
      raise Exception("Unknown type: "+typt)
  def copy(fr,to,force=False):
    type=m_path.info(fr)["type"]
    if type=="file":
      if m_path.exists(to) and force:
        m_path.delete(to)
      _shutil.copy(fr,to)
    else:
      raise Exception("Unknown type: "+type)
  def move(fr,to,force=False):
    type=m_path.info(fr)["type"]
    if type=="file":
      if m_path.exists(to) and force:
        m_path.delete(to)
      _shutil.move(fr,to)
    else:
      raise Exception("Unknown type: "+type)
  def rename(fr,to,force=False):
    type=m_path.info(fr)["type"]
    if type=="file":
      if m_path.exists(to) and force:
        m_path.delete(to)
      _os.rename(fr,to)
    else:
      raise Exception("Unknown type: "+type)
class m_dir: # Операции с папками
  def create(path,force=False): # Создать папку
    if m_path.exists(path):
      type=m_path.info(path)["type"]
      if type=="dir":
        return True
      elif force:
        m_path.delete(path)
      else:
        raise Exception("The object exists and is not a folder")
    _os.makedirs(path)
    return True
  def delete(path):
    type=m_path.info(path)["type"]
    if type=="dir":
      _os.rmdir(path)
    else:
      raise Exception("Unknown type: "+type)
  def copy(fr,to,force=False):
    type=m_path.info(fr)["dir"]
    if type=="dir":
      if m_path.info(to)["type"]!="dir" and force:
        try:
          m_path.delete(to)
        except:
          pass
      _shutil.copytree(fr,to)
    else:
      raise Exception("Unknown type: "+type)
  def move(fr,to,force=False):
    type=m_path.info(fr)["dir"]
    if type=="dir":
      if m_path.info(to)["type"]!="dir" and force:
        try:
          m_path.delete(to)
        except:
          pass
      _shutil.move(fr,to)
    else:
      raise Exception("Unknown type: "+type)
  def rename(fr,to,force=False):
    t=m_path.info(fr)["dir"]
    if t=="dir":
      if m_path.info(to)["type"]!="dir" and force:
        try:
          m_path.delete(to)
        except:
          pass
      _os.rename(fr,to)
    else:
      raise Exception("Unknown type: "+t)
  def list(path,files=True,dirs=True,links=None):
    a=_os.listdir(path)
    b=[]
    for i in a:
      info=m_path.info(i)
      if links==None:
        c=True
      elif links==True:
        c=info["link"]
      elif links==False:
        c=not info["link"]
      else:
        raise Exception('"links" can only be True, False or None')
      if c:
        if files and info["type"]=="file":
          b.append(i)
        elif dirs and info["type"]=="dir":
          b.append(i)
    return b
class m_str: # Операции с текстом
  def array2str(a):
    b=[]
    for i in a:
      b.append(str(i))
    return b
  def dict2str(a):
    b={}
    for key,value in a.items():
      b[key]=str(value)
    return b
  class replace:
    def multi(text=None,dict=None): # Мульти-замена {"что заменить":"чем заменить"}
      t=str(text)
      for key,value in dict.items():
        t=t.replace(key,str(value))
      return t
    def all(text=None,fr=None,to=None): # Замена пока заменяемый текст не исчезнет
      t=str(text)
      a=str(fr)
      b=str(to)
      if a in b:
        raise endlessCycle('"{0}" is contained in "{1}", this causes an infinite loop'.format(a,b))
      while a in t:
        t=t.replace(a,b)
      return t
class m_json: # Операции с JSON
  def encode(data,mode="c",indent=2,sort=True): # Данные в текст
    if mode in ["c","compress","min","zip"]: # Сжатый
      t=_json.dumps(data,separators=[",",":"],sort_keys=sort)
    elif mode in ["pretty","p","print","max"]: # Развёрнутый
      t=_json.dumps(data,indent=int(indent),sort_keys=sort)
    else: # Без параметров
      t=_json.dumps(data,sort_keys=sort)
    return t
  def decode(text): # Текст в данные
    return _json.loads(str(text))
  def write(path,data,encoding="utf-8",mode="c",indent=2,sort=True,force=False): # Данные в файл
    if m_path.info(path)["type"]=="dir" and force:
      _os.remove(path)
    with open(path,"w",encoding=encoding) as f:
      f.write(m_json.encode(data,mode=mode,indent=indent,sort=sort))
    return True
  def read(path,encoding="utf-8"): # Данные из файла
    with open(path,"r",encoding=encoding) as f:
      return _json.load(f)
  def sort(data): # Сортировать ключи словарей ({"b":1,"c":2,"a":3} -> {"a":3,"b":1,"c":2})
    return m_json.decode(m_json.encode(data,mode="c",sort=True))
  def rebuild(data,mode="c",indent=2,sort=True): # Перестроить JSON в тексте
    return m_json.encode(m_json.decode(data),mode=mode,indent=indent,sort=sort)
  def rewrite(path,encoding="utf-8",mode="c",indent=2,sort=True): # Перестроить JSON в файле
    return m_json.write(path,m_json.read(path,encoding=encoding),encoding=encoding,mode=mode,indent=indent,sort=sort)
# Команды для разных ОС
if m_os.platform=="Windows": # Windows
  def clear():
    _os.system("cls")
  cls=clear
elif m_os.platform=="Linux": # Linux
  def clear():
    _os.system("clear")
  cls=clear
elif m_os.platform=="Darwin": # MacOS
  pass
else: # Неизвестный тип
  print("MainShortcuts WARN: Unknown OS \""+m_os.platform+"\"")
