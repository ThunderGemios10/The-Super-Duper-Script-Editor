################################################################################
### Copyright © 2012 BlackDragonHunt
### 
### This file is part of the Super Duper Script Editor.
### 
### The Super Duper Script Editor is free software: you can redistribute it
### and/or modify it under the terms of the GNU General Public License as
### published by the Free Software Foundation, either version 3 of the License,
### or (at your option) any later version.
### 
### The Super Duper Script Editor is distributed in the hope that it will be
### useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.
### 
### You should have received a copy of the GNU General Public License
### along with the Super Duper Script Editor.
### If not, see <http://www.gnu.org/licenses/>.
################################################################################

import os.path
import sqlite3
import threading
import time
from collections import deque

import common

class SimilarityDB():
  def __init__(self):
    self.similarities = {}
    self.queue = deque([])
    
    self.queue_lock = threading.Lock()
    self.similarities_lock = threading.Lock()
    self.db_lock = threading.Lock()
    
    self.thread = threading.Thread(target = self.process_queue)
    # Do not allow this thread to prevent the program from closing
    # since I'm a retard and haven't come up with a decent way to
    # kill the thread when the main window is closed.
    self.thread.daemon = True
    
    self.conn = sqlite3.connect(common.editor_config.similarity_db, check_same_thread = False)
    self.conn.row_factory = sqlite3.Row
    self.c = self.conn.cursor()
    
    self.running = True
    
    self.thread.start()
  
  def __del__(self):
    self.c.close()
    self.running = False
  
  def process_queue(self):
    
    while True:
      if self.running == False:
        return
      
      self.queue_lock.acquire()
      if len(self.queue) == 0:
        self.queue_lock.release()
        time.sleep(1)
        continue
      self.queue_lock.release()
      
      self.queue_lock.acquire()
      queued = self.queue.pop()
      self.queue_lock.release()
      
      #####
      self.similarities_lock.acquire()
      if queued in self.similarities:
        self.similarities_lock.release()
        continue
      self.similarities_lock.release()
      
      sim = self.find_similar(queued)
      
      self.similarities_lock.acquire()
      self.similarities[queued] = sim
      self.similarities_lock.release()
      #####
  
  def find_similar(self, filename):
  
    filename = os.path.normpath(os.path.normcase(filename))
    
    #####
    self.db_lock.acquire()
    
    self.c.execute('''SELECT * FROM similarity
                      WHERE file1 = ? OR file2 = ?''',
                  (filename, filename))
    
    sim = []
    
    for row in self.c:
      file = row['file1']
      if file == filename:
        file = row['file2']
      
      sim.append(file)
        
    self.db_lock.release()
    #####
    
    return sim
  
  def add_similar(self, file1, file2, percent = 100):
    self.add_similar_files([file1], [file2], percent)
  
  def add_similar_files(self, file_list1, file_list2, percent):
    
    self.db_lock.acquire()
    self.similarities_lock.acquire()
    
    for file1 in file_list1:
      file1 = os.path.normpath(os.path.normcase(file1))
      
      for file2 in file_list2:
        file2 = os.path.normpath(os.path.normcase(file2))
        
        if file1 == file2:
          continue
        
        self.c.execute('''SELECT * FROM similarity
                          WHERE ((file1 = ? AND file2 = ?)
                          OR (file1 = ? AND file2 = ?))
                       ''', (file2, file1, file1, file2))
        # Only add if we don't have the entry normal or reversed.
        if self.c.fetchone() == None:
          self.c.execute('''INSERT OR IGNORE INTO similarity
                            VALUES(?, ?, ?)
                         ''', (file1, file2, percent))
        
        # Make sure we have up-to-date info.
        if file1 in self.similarities:
          del self.similarities[file1]
        
        if file2 in self.similarities:
          del self.similarities[file2]
        
        #self.queue_query_at_top(file1)
        #self.queue_query_at_top(file2)
    
    self.conn.commit()
    
    self.similarities_lock.release()
    self.db_lock.release()
  
  def remove_similar(self, file1, file2):
    self.remove_similar_files([file1], [file2])
  
  def remove_similar_files(self, file_list1, file_list2):
    
    if file_list1 == None or len(file_list1) == 0 or file_list2 == None or len(file_list2) == 0:
      return
    
    self.db_lock.acquire()
    self.similarities_lock.acquire()
    
    for file1 in file_list1:
    
      file1 = os.path.normpath(os.path.normcase(file1))
      
      # Make sure we have up-to-date info.
      if file1 in self.similarities:
        del self.similarities[file1]
      #self.queue_query_at_top(file1)
      
      for file2 in file_list2:
        file2 = os.path.normpath(os.path.normcase(file2))
      
        self.c.execute('''DELETE FROM similarity
                          WHERE ((file1 = ? AND file2 = ?)
                          OR (file1 = ? AND file2 = ?))
                       ''', (file2, file1, file1, file2))
        
        if file2 in self.similarities:
          del self.similarities[file2]
        #self.queue_query_at_top(file2)
    
    self.conn.commit()
    
    self.similarities_lock.release()
    self.db_lock.release()
  
  def get_similarities(self, filename):
    
    sim = []
    
    #####
    self.similarities_lock.acquire()
      
    if filename in self.similarities:
      sim = self.similarities[filename]
      self.similarities_lock.release()
      return sim
    
    sim = self.find_similar(filename)
    self.similarities[filename] = sim
    
    self.similarities_lock.release()
    #####
    
    return sim
  
  def queue_query(self, filename):
    
    self.queue_lock.acquire()
    self.queue.appendleft(filename)
    self.queue_lock.release()
  
  def queue_query_at_top(self, filename):
    
    self.queue_lock.acquire()
    self.queue.append(filename)
    self.queue_lock.release()
  
  def clear(self):
    #self.thread.pause()
    
    self.queue_lock.acquire()
    self.queue = []
    self.queue_lock.release()
    
    self.similarities_lock.acquire()
    self.similarities = {}
    self.similarities_lock.release()
    
    #self.thread.start()

### EOF ###