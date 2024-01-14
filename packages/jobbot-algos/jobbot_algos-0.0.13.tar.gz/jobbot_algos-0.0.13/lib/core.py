#!/usr/bin/env python
# coding: utf-8

# # 1. Set default log level to 'INFO':

# In[11]:


# export 
from loguru import logger
import sys

logger.remove()
logger.add(sink=sys.stderr, level='INFO')

