import pytest
import os
import configparser
import sqlite3


def test_thresholds():

    from infSim.initiate import thresholds
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

    dummy_nodes = [(i+1,0,0) for i in range(4)]
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

    conn.executemany('INSERT INTO nodes VALUES (?, ?, ?)', dummy_nodes)
    conn.executemany('INSERT INTO edges VALUES (?, ?)', dummy_edges)

    conn.commit()

    thresholds(config, conn)

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


def test_incentivize():

    from infSim.settings import make_settings_file
    from infSim.db import create_db
    from infSim.initiate import incentivize

    ## TEST SETUP ##

    directory_name = os.getcwd()
    params = dict(thresh_prop=1, incentive_prop=0.2)
    make_settings_file(directory_name, directory_name, params)

    settings_config = configparser.ConfigParser()
    results_config = configparser.ConfigParser()
    settings_config.read(directory_name + '/settings.ini')
    results_config['RESULTS'] = dict()
    conn = sqlite3.connect(settings_config['FILES']['DB'])
    conn.row_factory = sqlite3.Row
    
    create_db(conn) 

    dummy_nodes = list()
    dummy_nodes.append((1,5,0)) 
    dummy_nodes.append((2,5,0))
    dummy_nodes.append((3,4,0))
    dummy_nodes.append((4,1,0))

    conn.executemany('INSERT INTO nodes VALUES (?, ?, ?)', dummy_nodes)

    conn.commit()

    target_set = conn.execute('SELECT * FROM nodes WHERE nodeID in (1,3,4)')
    incentivize(settings_config, results_config, conn, target_set)

    nodes = conn.execute('SELECT * FROM nodes')
    node_count = 0
    for row in nodes:

        if row['nodeID'] == 1:

            '''TEST: incentive calculation results in an int'''
            assert row['threshold'] == 1
        
        if row['nodeID'] == 2:

            '''TEST: not part of target set'''
            assert row['threshold'] == 5

        if row['nodeID'] == 3:

            '''TEST: incentive calculation non int is taken as floor 
                     this is important otherwise we will never have thresholds 0 to start
                     the simulation'''
            assert row['threshold'] == 0
            assert row['inf'] == 1

        if row['nodeID'] == 4:

            assert row['threshold'] == 0
            assert row['inf'] == 1   
        
        node_count += 1
    
    assert node_count == 4

    '''TEST: incentives added correctly'''
    assert results_config['RESULTS']['incentive_total'] == '9'

    active_nodes = conn.execute('SELECT * FROM activeNodes')

    active_count = 0
    for node in active_nodes:

        if node['nodeID'] == 1:

            pytest.fail('Node 1 should not be active. It was only partially incentivized')

        if node['nodeID'] == 2:

            pytest.fail('Node 2 should not be active. It was not incentivized')

        assert node['round'] == 0

        active_count += 1
    
    assert active_count == 2

    conn.close()
    os.remove(settings_config['FILES']['DB'])
    os.remove('settings.ini')
    os.remove('target-set.csv')



def test_select_random_target_set():

    from infSim.settings import make_settings_file
    from infSim.db import create_db
    from infSim.initiate import select_random_target_set

    ## TEST SETUP ##

    directory_name = os.getcwd()
    params = dict( target_set_prop = 0.1)
    make_settings_file(directory_name, directory_name, params)

    settings_config = configparser.ConfigParser()
    settings_config.read(directory_name + '/settings.ini')
    conn = sqlite3.connect(settings_config['FILES']['DB'])
    conn.row_factory = sqlite3.Row
    
    create_db(conn)

    dummy_nodes = [(i+1,1,1) for i in range(10000)]

    conn.executemany('INSERT INTO nodes VALUES (?, ?, ?)', dummy_nodes)

    conn.commit()

    test_random_target_set = select_random_target_set(settings_config, conn).fetchall()

    assert len(test_random_target_set) == 1000
    
    conn.close()
    os.remove(settings_config['FILES']['DB'])
    os.remove('settings.ini')

