# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Useful common utility functions."""

import collections
import re


DataSetName = collections.namedtuple('DataSetName', ['project_id', 'dataset_id'])
TableName = collections.namedtuple('TableName', ['project_id', 'dataset_id', 'table_id'])

# Absolute project-qualified name pattern: <project>:<dataset>
_ABS_DATASET_NAME_PATTERN = r'^([a-z0-9\-_\.:]+)\:([a-zA-Z0-9_]+)$'

# Relative name pattern: <dataset>
_REL_DATASET_NAME_PATTERN = r'^([a-zA-Z0-9_]+)$'

# Absolute project-qualified name pattern: <project>:<dataset>.<table>
_ABS_TABLE_NAME_PATTERN = r'^([a-z0-9\-_\.:]+)\:([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)$'

# Relative name pattern: <dataset>.<table>
_REL_TABLE_NAME_PATTERN = r'^([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)$'

# Table-only name pattern: <table>
_TABLE_NAME_PATTERN = r'^([a-zA-Z0-9_]+)$'


def parse_dataset_name(name, project_id=None):
  """Parses a dataset name into its individual parts.

  Args:
    name: the name to parse, or a tuple, dictionary or array containing the parts.
    project_id: the expected project ID. If the name does not contain a project ID,
        this will be used; if the name does contain a project ID and it does not match
        this, an exception will be thrown.
  Returns:
    The DataSetName for the dataset.
  Raises:
    Exception: raised if the name doesn't match the expected formats.
  """
  _project_id = _dataset_id = None
  if isinstance(name, basestring):
    # Try to parse as absolute name first.
    m = re.match(_ABS_DATASET_NAME_PATTERN, name, re.IGNORECASE)
    if m is not None:
      _project_id, _dataset_id = m.groups()
    else:
      # Next try to match as a relative name implicitly scoped within current project.
      m = re.match(_REL_DATASET_NAME_PATTERN, name)
      if m is not None:
        groups = m.groups()
        _dataset_id = groups[0]
  elif isinstance(name, dict):
    try:
      _dataset_id = name['dataset_id']
      _project_id = name['project_id']
    except KeyError:
      pass
  else:
    # Try treat as an array or tuple
    if len(name) == 2:
      # Treat as a tuple or array.
      _project_id, _dataset_id = name
    elif len(name) == 1:
      _dataset_id = name[0]
  if not _dataset_id:
    raise Exception('Invalid dataset name: ' + str(name))
  if not _project_id:
    _project_id = project_id

  return DataSetName(_project_id, _dataset_id)


def parse_table_name(name, project_id=None, dataset_id=None):
  """Parses a table name into its individual parts.

  Args:
    name: the name to parse, or a tuple, dictionary or array containing the parts.
    project_id: the expected project ID. If the name does not contain a project ID,
        this will be used; if the name does contain a project ID and it does not match
        this, an exception will be thrown.
    dataset_id: the expected dataset ID. If the name does not contain a dataset ID,
        this will be used; if the name does contain a dataset ID and it does not match
        this, an exception will be thrown.
  Returns:
    A tuple consisting of the full name and individual name parts.
  Raises:
    Exception: raised if the name doesn't match the expected formats.
  """
  _project_id = _dataset_id = _table_id = None
  if isinstance(name, basestring):
    # Try to parse as absolute name first.
    m = re.match(_ABS_TABLE_NAME_PATTERN, name, re.IGNORECASE)
    if m is not None:
      _project_id, _dataset_id, _table_id = m.groups()
    else:
      # Next try to match as a relative name implicitly scoped within current project.
      m = re.match(_REL_TABLE_NAME_PATTERN, name)
      if m is not None:
        groups = m.groups()
        _project_id, _dataset_id, _table_id = project_id, groups[0], groups[1]
      else:
        # Finally try to match as a table name only.
        m = re.match(_TABLE_NAME_PATTERN, name)
        if m is not None:
          groups = m.groups()
          _project_id, _dataset_id, _table_id = project_id, dataset_id, groups[0]
  elif isinstance(name, dict):
    try:
      _table_id = name['table_id']
      _dataset_id = name['dataset_id']
      _project_id = name['project_id']
    except KeyError:
      pass
  else:
    # Try treat as an array or tuple
    if len(name) == 3:
      _project_id, _dataset_id, _table_id = name
    elif len(name) == 2:
      _dataset_id, _table_id = name
  if not _table_id:
    raise Exception('Invalid table name: ' + str(name))
  if not _project_id:
    _project_id = project_id
  if not _dataset_id:
    _dataset_id = dataset_id

  return TableName(_project_id, _dataset_id, _table_id)