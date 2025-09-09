from integrity_engine import compare_baselines

def test_basic_changes():
    old = {'/a': '1', '/b': '2'}
    new = {'/a': '1', '/b': '3', '/c': '4'}
    assert compare_baselines(old, new) == {
        'MODIFIED': ['/b'],
        'CREATED': ['/c'],
        'DELETED': []
    }

def test_deleted_and_created_only():
    assert compare_baselines({}, {'/new': 'x'}) == {
        'MODIFIED': [],
        'CREATED': ['/new'],
        'DELETED': []
    }
    assert compare_baselines({'/old': 'x'}, {}) == {
        'MODIFIED': [],
        'CREATED': [],
        'DELETED': ['/old']
    }

def test_metadata_values():
    old = {'/f': {'hash': 'a'}}
    new = {'/f': {'hash': 'b'}}
    assert compare_baselines(old, new)['MODIFIED'] == ['/f']

def test_identical_baselines():
    old = {'/a':'1', '/b':'2'}
    new = {'/b':'2', '/a':'1'}
    assert compare_baselines(old, new) == {'MODIFIED': [], 'CREATED': [], 'DELETED': []}
