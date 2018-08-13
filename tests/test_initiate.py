import pytest
import os
import configparser
import sqlite3

def test_thresholds_random():

    from infSim.initiate import thresholds_random
    from infSim.settings import make_settings_file
    from infSim.db import create_db

    ## TEST SETUP ##

    directory_name = os.getcwd()
    # Paramaters except threshold proportion don't matter because test doesn't use them
    params=dict(thresh_prop=0)
    make_settings_file(directory_name, directory_name, params)

    config = configparser.ConfigParser()
    config.read(directory_name + '/settings.ini')
    conn = sqlite3.connect(config['FILES']['DB'])
    conn.row_factory = sqlite3.Row
    
    create_db(conn) 

    dummy_nodes = [(i+1,0,0,0) for i in range(4)]
    '''
    Test: Min threshold is 1
    Test: Threshold is in range of number of neighbours
    Test: All threshs are set
    '''
    dummy_edges = ([(1,2),
                    (2,1),
                    (2,3),
                    (2,4),
                    (3,2),
                    (3,4),
                    (4,2),
                    (4,3)])

    conn.executemany('INSERT INTO nodes VALUES (?, ?, ?, ?)', dummy_nodes)
    conn.executemany('INSERT INTO edges VALUES (?, ?)', dummy_edges)

    conn.commit()

    thresholds_random(config, conn)

    updated_nodes = conn.execute('SELECT threshold, nodeID FROM nodes')

    row_count = 0
    for row in updated_nodes:

        if row['nodeID'] == 1:

            assert row['threshold'] == 1
        
        if row['nodeID'] == 2:

            assert row['threshold'] in [1,2,3]
        
        if row['nodeID'] == 3:

            assert row['threshold'] in [1,2]
        
        if row['nodeID'] == 4:

            assert row['threshold'] in [1,2]
        
        row_count += 1
    
    assert row_count == 4
    
    conn.close()
    os.remove(config['FILES']['DB'])
    os.remove('settings.ini')

def test_thresholds_proportion():

    from infSim.initiate import thresholds_proportion
    from infSim.settings import make_settings_file
    from infSim.db import create_db

    ## TEST SETUP ##

    directory_name = os.getcwd()
    # Paramaters except threshold proportion don't matter because test doesn't use them
    params=dict(thresh_prop=0.5)
    make_settings_file(directory_name, directory_name, params)

    config = configparser.ConfigParser()
    config.read(directory_name + '/settings.ini')
    conn = sqlite3.connect(config['FILES']['DB'])
    conn.row_factory = sqlite3.Row
    
    create_db(conn) 

    dummy_nodes = [(i+1,0,0,0) for i in range(4)]
    '''
    Test: Min threshold is 1
    Test: Non-integer set to ceiling
    Test: All threshs are set
    Test: Integer is set to integer  
    '''
    dummy_edges = ([(1,2),
                    (2,1),
                    (2,3),
                    (2,4),
                    (3,2),
                    (3,4),
                    (4,2),
                    (4,3)])

    conn.executemany('INSERT INTO nodes VALUES (?, ?, ?, ?)', dummy_nodes)
    conn.executemany('INSERT INTO edges VALUES (?, ?)', dummy_edges)

    conn.commit()

    thresholds_proportion(config, conn)

    updated_nodes = conn.execute('SELECT threshold, nodeID FROM nodes')

    row_count = 0
    for row in updated_nodes:

        if row['nodeID'] == 1:

            assert row['threshold'] == 1
        
        if row['nodeID'] == 2:

            assert row['threshold'] == 2
        
        if row['nodeID'] == 3:

            assert row['threshold'] == 1
        
        if row['nodeID'] == 4:

            assert row['threshold'] == 1
        
        row_count += 1
    
    assert row_count == 4
    
    conn.close()
    os.remove(config['FILES']['DB'])
    os.remove('settings.ini')



def test_incentivize_full():

    from infSim.settings import make_settings_file
    from infSim.db import create_db
    from infSim.initiate import incentivize

    ## TEST SETUP ##

    directory_name = os.getcwd()
    params = dict(thresh_prop=1, budget=5)
    make_settings_file(directory_name, directory_name, params)

    settings_config = configparser.ConfigParser()
    results_config = configparser.ConfigParser()
    settings_config.read(directory_name + '/settings.ini')
    results_config['RESULTS'] = dict()
    conn = sqlite3.connect(settings_config['FILES']['DB'])
    conn.row_factory = sqlite3.Row
    
    create_db(conn) 

    dummy_nodes = list()
    dummy_nodes.append((1,5,0,0)) 
    dummy_nodes.append((2,5,0,0))
    dummy_nodes.append((3,4,0,0))
    dummy_nodes.append((4,2,0,0))

    dummy_edges = list()
    dummy_edges.append((1,2))
    dummy_edges.append((1,3))
    dummy_edges.append((1,4))
    dummy_edges.append((2,1))
    dummy_edges.append((2,3))
    dummy_edges.append((3,1))
    dummy_edges.append((3,2))
    dummy_edges.append((4,1))

    conn.executemany('INSERT INTO nodes VALUES (?, ?, ?, ?)', dummy_nodes)
    conn.executemany('INSERT INTO edges VALUES (?,?)', dummy_edges)

    conn.commit()

    incentivize(settings_config, results_config, conn)

    nodes_influenced = conn.execute('SELECT * FROM nodes WHERE inf=1')

    influenced_ids = list()
    for node in nodes_influenced:

        assert node['threshold'] == 0
        influenced_ids.append(node['nodeID'])

    assert len(influenced_ids) == 1

    nodes_activated = conn.execute('SELECT * FROM activeNodes')

    activeNodes = 0
    for activeNode in nodes_activated:

        assert activeNode['round'] == 0
        assert activeNode['nodeID'] in influenced_ids

        if activeNode['nodeID'] == 1:

            assert activeNode['power'] == 3.0

        if activeNode['nodeID'] == 2 or activeNode['nodeID'] == 3:

            assert activeNode['power'] == 2.0

        if activeNode['nodeID'] == 4:

            assert activeNode['power'] == 1.0
        
        activeNodes = activeNodes + 1
    
    assert activeNodes == len(influenced_ids)

    conn.close()
    os.remove(settings_config['FILES']['DB'])
    os.remove('settings.ini')
    os.remove('target-set.csv')       

def test_incentivize_partial():

    from infSim.settings import make_settings_file
    from infSim.db import create_db
    from infSim.initiate import incentivize

    ## TEST SETUP ##

    directory_name = os.getcwd()
    params = dict(thresh_prop=1, budget=3, incentive_prop=.5)
    make_settings_file(directory_name, directory_name, params)

    settings_config = configparser.ConfigParser()
    results_config = configparser.ConfigParser()
    settings_config.read(directory_name + '/settings.ini')
    results_config['RESULTS'] = dict()
    conn = sqlite3.connect(settings_config['FILES']['DB'])
    conn.row_factory = sqlite3.Row
    
    create_db(conn) 

    dummy_nodes = list()
    dummy_nodes.append((1,5,0,0)) 
    dummy_nodes.append((2,5,0,0))
    dummy_nodes.append((3,1,0,0))
    dummy_nodes.append((4,1,0,0))

    dummy_edges = list()
    dummy_edges.append((1,2))
    dummy_edges.append((1,3))
    dummy_edges.append((1,4))
    dummy_edges.append((2,1))
    dummy_edges.append((2,3))
    dummy_edges.append((3,1))
    dummy_edges.append((3,2))
    dummy_edges.append((4,1))

    conn.executemany('INSERT INTO nodes VALUES (?, ?, ?, ?)', dummy_nodes)
    conn.executemany('INSERT INTO edges VALUES (?,?)', dummy_edges)

    conn.commit()

    incentivize(settings_config, results_config, conn)

    nodes_influenced = conn.execute('SELECT * FROM nodes WHERE inf=1')

    influenced_ids = list()
    for node in nodes_influenced:

        assert node['threshold'] == 0
        influenced_ids.append(node['nodeID'])

    assert len(influenced_ids) == 2

    nodes_activated = conn.execute('SELECT * FROM activeNodes')

    activeNodes = 0
    for activeNode in nodes_activated:

        assert activeNode['round'] == 0
        assert activeNode['nodeID'] in influenced_ids

        if activeNode['nodeID'] == 1:

            assert activeNode['power'] == 3.0

        if activeNode['nodeID'] == 2 or activeNode['nodeID'] == 3:

            assert activeNode['power'] == 2.0

        if activeNode['nodeID'] == 4:

            assert activeNode['power'] == 1.0
        
        activeNodes = activeNodes + 1
    
    assert activeNodes == len(influenced_ids)

    conn.close()
    os.remove(settings_config['FILES']['DB'])
    os.remove('settings.ini')
    #os.remove('target-set.csv')     


def test_lambda_value_degree():

    from infSim.initiate import lambda_value_degree
    from infSim.settings import make_settings_file
    from infSim.db import create_db

    ## TEST SETUP ##

    directory_name = os.getcwd()
    params = dict()
    make_settings_file(directory_name, directory_name, params)

    settings_config = configparser.ConfigParser()
    settings_config.read(directory_name + '/settings.ini')
    conn = sqlite3.connect(settings_config['FILES']['DB'])
    conn.row_factory = sqlite3.Row
    
    create_db(conn)

    dummy_nodes = list()
    dummy_nodes.append((1,5,0,0)) 
    dummy_nodes.append((2,5,0,0))
    dummy_nodes.append((3,4,0,0))
    dummy_nodes.append((4,1,0,0))

    dummy_edges = list()
    dummy_edges.append((1,2))
    dummy_edges.append((2,1))
    dummy_edges.append((1,3))
    dummy_edges.append((3,1))

    lambda_value_degree(settings_config,conn)

    updated_nodes_query = conn.execute('SELECT * FROM nodes')

    for node in updated_nodes_query:

        if node['nodeID'] == 1:

            assert node['lambda'] == 2

        if node['nodeID'] ==  2:

            assert node['lambda'] == 1
        
        if node['nodeID'] == 3:

            assert node['lambda'] == 1

        if node['nodeID'] == 4:

            assert node['lambda'] == 0

    conn.close()
    os.remove(settings_config['FILES']['DB'])
    os.remove('settings.ini')