import pytest
import os
import configparser
import sqlite3

def test_run_sim():

    from infSim.sim import run_sim
    from infSim.settings import make_settings_file
    from infSim.db import create_db

    ## DUMMY DATA ##

    dummy_nodes = list()
    dummy_nodes.append((1,0,1))
    dummy_nodes.append((2,2,0))
    dummy_nodes.append((3,0,1))
    dummy_nodes.append((4,3,0))
    dummy_nodes.append((5,2,0))
    dummy_nodes.append((6,2,0))


    dummy_edges = list()
    dummy_edges.append((1,2))
    dummy_edges.append((1,4))
    dummy_edges.append((1,5))
    dummy_edges.append((2,1))
    dummy_edges.append((2,3))
    dummy_edges.append((2,4))
    dummy_edges.append((2,6))
    dummy_edges.append((3,2))
    dummy_edges.append((3,4))
    dummy_edges.append((4,1))
    dummy_edges.append((4,2))
    dummy_edges.append((4,3))
    dummy_edges.append((5,1))
    dummy_edges.append((5,6))
    dummy_edges.append((6,2))
    dummy_edges.append((6,5))

    dummy_active = list()
    dummy_active.append((1,0))
    dummy_active.append((3,0))

    ## TEST SETUP - Lambda One ##
    directory_name = os.getcwd()
    
    params = dict(lambda_val=1)
    make_settings_file(directory_name, params)

    config = configparser.ConfigParser()
    config.read(directory_name + '/settings.ini')
    conn = sqlite3.connect(config['FILES']['DB'])
    conn.row_factory = sqlite3.Row
    
    create_db(conn)

    conn.executemany('INSERT INTO nodes VALUES (?, ?, ?)', dummy_nodes)
    conn.executemany('INSERT INTO edges VALUES (?, ?)', dummy_edges)
    conn.executemany('INSERT INTO activeNodes VALUES (?, ?)', dummy_active)

    conn.commit()

    run_sim(config, conn)

    influenced_nodes = conn.execute('SELECT nodeID FROM nodes WHERE inf=1')

    influenced_count = 0
    for node in influenced_nodes:

        if node['nodeID'] == 5:

            pytest.fail('Node 5 Should Not Be Influenced')
        
        if node['nodeID'] == 6:

            pytest.fail('Node 6 Should Not Be Influenced')
        
        if node['nodeID'] == 4:

            pytest.fail('Node 4 Should Only Be Influenced When Lambda > 1')
        
        influenced_count += 1
    
    assert influenced_count == 3
    
    active_nodes = conn.execute('SELECT * FROM activeNodes')

    active_count=0
    for node in active_nodes:

        if node['nodeID'] == 5:

            pytest.fail('Node 5 Should Not Have Been Activated')
        
        if node['nodeID'] == 6:

            pytest.fail('Node 6 Should Not Have Been Activated')
        
        if node['nodeID'] == 4:

            pytest.fail('Node 4 Should Only Be Activated When Lambda > 1')
        
        if node['nodeID'] == 1:

            if node['round'] != 0:

                pytest.fail('Node 1 Should Only Be Active First Round')
        
        if node['nodeID'] == 3:

            if node['round'] != 0:

                pytest.fail('Node 3 Should Only Be Active First Round')        

        if node['nodeID'] == 2:

            if node['round'] != 1:

                pytest.fail('Node 2 Should Only Be Active Second Round')
        
        active_count += 1
    
    assert active_count == 3

    conn.close()
    os.remove(config['FILES']['DB'])
    os.remove('settings.ini')

    ## TEST SETUP - Lambda Two ##
    directory_name = os.getcwd()
    
    params = dict(lambda_val=2)
    make_settings_file(directory_name, params)

    config = configparser.ConfigParser()
    config.read(directory_name + '/settings.ini')
    conn = sqlite3.connect(config['FILES']['DB'])
    conn.row_factory = sqlite3.Row
    
    create_db(conn)

    conn.executemany('INSERT INTO nodes VALUES (?, ?, ?)', dummy_nodes)
    conn.executemany('INSERT INTO edges VALUES (?, ?)', dummy_edges)
    conn.executemany('INSERT INTO activeNodes VALUES (?, ?)', dummy_active)

    conn.commit()

    run_sim(config, conn)

    influenced_nodes = conn.execute('SELECT nodeID FROM nodes WHERE inf=1')

    influenced_count = 0
    for node in influenced_nodes:

        if node['nodeID'] == 5:

            pytest.fail('Node 5 Should Not Be Influenced')
        
        if node['nodeID'] == 6:

            pytest.fail('Node 6 Should Not Be Influenced')
        
        influenced_count += 1
    
    assert influenced_count == 4
    
    active_nodes = conn.execute('SELECT * FROM activeNodes')

    active_count=0
    for node in active_nodes:

        if node['nodeID'] == 5:

            pytest.fail('Node 5 Should Not Have Been Activated')
        
        if node['nodeID'] == 6:

            pytest.fail('Node 6 Should Not Have Been Activated')
        
        if node['nodeID'] == 4:

            if node['round'] != 2 and node['round'] !=3:

                pytest.fail('Node 4 Should Only Be Activated Third and Fourth Round')
        
        if node['nodeID'] == 1:

            if node['round'] != 0 and node['round'] != 1:

                pytest.fail('Node 1 Should Only Be Active First and Second Round')
        
        if node['nodeID'] == 3:

            if node['round'] != 0 and node['round'] != 1:

                pytest.fail('Node 3 Should Only Be Active First and Second Round')        

        if node['nodeID'] == 2:

            if node['round'] != 1 and node['round'] != 2:

                pytest.fail('Node 2 Should Only Be Active Second and Third Round')
        
        active_count += 1
    
    assert active_count == 8

    conn.close()
    os.remove(config['FILES']['DB'])
    os.remove('settings.ini')
    os.remove('simulation-details.txt')




